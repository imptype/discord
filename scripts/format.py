"""
format.py - Custom formatter for this repo (This was AI-assisted).

First it runs Ruff check to achieve the following:
1. Check for outdated syntax, like Union[int, str] vs int | str.
2. Check for likely bugs and bad patterns (flake8-bugbear), like mutable default arguments.

Then it runs some extra things outside:
1. Enforce 2-space indents.
2. Enforce single quotes (skipping strings with nested quotes).
3. Enforce LF instead of CRLF newline character.
4. Somewhat enforce PascalCase class names.
5. Somewhat enforce snake_case variable and function names.
6. Enforce no double blank lines in a row (skipping strings).
7. Enforce a space between operators like * + (includes = in parameters and assignments)
8. Sort imports by these rules:
   a. Groups first: __future__, then system libs, then 3rd party libs, then local files.
   b. Then "import x" over "from x import y"
   c. Then shortest line first, so "import os" comes before "import sys" before "import asyncio".
   d. Then alphabetical when the lengths match.
   e. Also formats names in "from x import a, b, c" by class, then func, then variable, and alphabetical
   Imports have no blank lines between them, and exactly one blank line after them.
   A comment on an import line like # is preserved, but not counted in the line length.
   A comment or docstring outside an import line, are not touched (they stay in that line index).
9. It also removes the trailing commas (but ignores 1 size tuples). (one, two,) -> (one, two)
It also ensures all tracked text (.gitignore, *.md, *.toml, *.lock,
*.env, *.yml, LICENSE) files use LF and end with 1 newline.
10. For *.toml files (like pyproject.toml) it enforces the same 2-space indent for multi-line arrays
  and inline tables, and removes trailing commas before a closing ] or }.

This is a hybrid because Ruff can either expand or collapse lines, but
not leave them alone! We also could use other Ruff stuff.

Usage (run from the project root):
  uv run python scripts/format.py             fix files in place
  uv run python scripts/format.py --check     report problems, change nothing, exit 1 if any
  uv run python scripts/format.py --diff      show what would change, change nothing
  uv run python scripts/format.py --selftest  run the built-in tests

No pass ever joins or splits lines. Each pass only changes whitespace, quotes and import order.
"""

import io
import os
import re
import ast
import sys
import copy
import fnmatch
import keyword
import tokenize
import sysconfig
import subprocess
from pathlib import Path
from itertools import accumulate
from functools import cache, lru_cache
from bisect import bisect_left, bisect_right

INDENT = 2
NAMING_IGNORE = '# naming: ignore'
MODES = ('', '--check', '--diff', '--selftest')

EXCLUDE_DIRS = {'.git', '.venv', 'venv', 'node_modules', '__pycache__', '.mypy_cache', '.ruff_cache'}
TEXT_GLOBS = ('*.md', '*.toml', '*.lock', '*.env', '*.yml', '*.yaml', '.gitignore', 'LICENSE', 'LICENSE.*')
TEXT_NAME = re.compile('|'.join(fnmatch.translate(os.path.normcase(glob)) for glob in TEXT_GLOBS))

SKIP_TYPES = {
  tokenize.COMMENT,
  tokenize.DEDENT,
  tokenize.ENCODING,
  tokenize.ENDMARKER,
  tokenize.INDENT,
  tokenize.NEWLINE,
  tokenize.NL
}
STR_STARTS = {getattr(tokenize, n) for n in ('FSTRING_START', 'TSTRING_START') if hasattr(tokenize, n)}
STR_ENDS = {getattr(tokenize, n) for n in ('FSTRING_END', 'TSTRING_END') if hasattr(tokenize, n)}

# Operators that always get a space on both sides.
ALWAYS_SPACED = {
  '=', '+=', '-=', '*=', '/=', '//=', '%=', '**=', '@=', '<<=', '>>=', '&=', '|=', '^=',
  ':=', '->', '<', '>', '<=', '>=', '==', '!='
}
# Operators spaced only when used as binary operators (not unary or *args).
BINARY_OPS = {'+', '-', '*', '/', '//', '%', '**', '@', '<<', '>>', '&', '|', '^'}
# Operators that hug the next token when not binary (-x, *args, **kw, ~x, @decorator).
HUG_AFTER = {'+', '-', '*', '**', '~', '@'}
OPENERS = {'(', '[', '{'}
CLOSERS = {')', ']', '}'}

# --- helpers ---

# Every pass is handed the text the previous pass returned, which is usually the very same text
# (a formatted file changes nothing), so whatever only depends on the text is worked out once and
# shared. The results are shared too, so nothing may modify them.
@lru_cache(maxsize = 1)
def tokens_of(src):
  return tuple(tokenize.generate_tokens(io.StringIO(src).readline))

@lru_cache(maxsize = 1)
def source_lines(src):
  return tuple(io.StringIO(src).readlines())

@lru_cache(maxsize = 1)
def parse(src):
  return ast.parse(src)

@lru_cache(maxsize = 1)
def line_starts(src):
  return (0, *accumulate(map(len, source_lines(src))))

def offset(starts, pos):
  return starts[pos[0] - 1] + pos[1]

def splice(src, edits):
  if not edits:
    return src
  parts = []
  done = 0
  for begin, end, text in sorted(edits):
    parts.append(src[done:begin])
    parts.append(text)
    done = end
  parts.append(src[done:])
  return ''.join(parts)

def width(line):
  body = line.lstrip(' \t')
  return len(line[: len(line) - len(body)].expandtabs(8))

@lru_cache(maxsize = 1)
def string_rows(src):
  """Rows that start inside a string, and rows that end inside one."""
  begins_in = set()
  ends_in = set()
  stack = []
  for tok in tokens_of(src):
    if tok.type in STR_STARTS:
      stack.append(tok.start[0])
    elif tok.type in STR_ENDS:
      first = stack.pop()
      begins_in.update(range(first + 1, tok.end[0] + 1))
      ends_in.update(range(first, tok.end[0]))
    elif tok.type == tokenize.STRING:
      begins_in.update(range(tok.start[0] + 1, tok.end[0] + 1))
      ends_in.update(range(tok.start[0], tok.end[0]))
  return frozenset(begins_in), frozenset(ends_in)

# --- pass: quotes ---

def requote(text, strict):
  """Return the string literal using single quotes, or None to leave it alone."""
  stripped = text.lstrip('rRbBuUfFtT')
  prefix = text[: len(text) - len(stripped)]
  if not stripped.startswith('"') or stripped.startswith('"""'):
    return None
  body = stripped[1:-1]
  if "'" in body:
    return None
  if strict and ('\\' in body or '"' in body):
    return None
  if '\\"' in body:
    if 'r' in prefix.lower():
      return None
    body = body.replace('\\"', '"')
  return prefix + "'" + body + "'"

def quote_edit(src, starts, first, last):
  begin = offset(starts, first.start)
  end = offset(starts, last.end)
  text = src[begin:end]
  new = requote(text, first is not last)
  if new is None or new == text:
    return []
  return [(begin, end, new)]

def fix_quotes(src):
  starts = line_starts(src)
  edits = []
  depth = 0
  first = None
  double = False  # whether the outermost f-string opened with a double quote
  for tok in tokens_of(src):
    kind = tok.type
    if kind == tokenize.STRING:
      if depth == 0 and '"' in tok.string[:3]:  # only a double quote right after the prefix can change
        edits += quote_edit(src, starts, tok, tok)
    elif kind in STR_STARTS:
      if depth == 0:
        first = tok
        double = '"' in tok.string[:3]
      depth += 1
    elif kind in STR_ENDS:
      depth -= 1
      if depth == 0 and double:
        edits += quote_edit(src, starts, first, tok)
  return splice(src, edits)

# --- pass: operator and comma spacing ---

def operand_end(tok):
  """True if tok can end an operand, so a following +, -, * is binary."""
  if tok is None:
    return False
  if tok.type in (tokenize.NUMBER, tokenize.STRING) or tok.type in STR_ENDS:
    return True
  if tok.type == tokenize.NAME:
    return not keyword.iskeyword(tok.string) or tok.string in ('True', 'False', 'None')
  return tok.type == tokenize.OP and tok.string in (CLOSERS | {'...'})

def wants(tok, prev):
  """(space before, space after) wanted around tok. None means leave alone."""
  if tok.type != tokenize.OP:
    return None, None
  text = tok.string
  if text == ',':
    return '', ' '
  if text in ALWAYS_SPACED:
    return ' ', ' '
  if text in BINARY_OPS and operand_end(prev):
    return ' ', ' '
  if text in HUG_AFTER and not (prev is not None and prev.string == 'except'):
    return None, ''
  return None, None

def gap(prev, prev_after, cur, cur_before):
  """Wanted whitespace between two adjacent tokens: ' ', '' or None (leave alone)."""
  if prev.string == ',' and cur.string in CLOSERS:
    return None
  if prev_after == '':
    return ''
  if cur_before == '':
    return ''
  if ' ' in (prev_after, cur_before):
    return ' '
  return None

def fix_spacing(src):
  starts = line_starts(src)
  edits = []
  prev = None
  prev_after = None
  adjacent = False
  depth = 0
  for tok in tokens_of(src):
    kind = tok.type
    if kind == tokenize.NEWLINE:
      prev = None
      adjacent = False
      continue
    if kind in SKIP_TYPES:
      adjacent = False
      continue
    if kind in STR_STARTS:
      depth += 1
      if depth > 1:
        adjacent = False
        continue
    elif kind in STR_ENDS:
      depth -= 1
      if depth > 0:
        adjacent = False
        continue
    elif depth > 0:
      adjacent = False
      continue
    if kind == tokenize.OP:
      before, after = wants(tok, prev)
    else:
      before = after = None
    # gap() has nothing to say unless one of the two tokens wants a say in the spacing
    if prev is not None and adjacent and (before is not None or prev_after is not None) and prev.end[0] == tok.start[0]:
      want = gap(prev, prev_after, tok, before)
      if want is not None:
        begin = offset(starts, prev.end)
        end = offset(starts, tok.start)
        current = src[begin:end]
        if current.strip(' \t') == '' and current != want:
          edits.append((begin, end, want))
    prev = tok
    prev_after = after
    adjacent = True
  return splice(src, edits)

# --- pass: trailing commas ---

NO_TUPLE_KEYWORDS = {'import', 'with'}

def fix_trailing_commas(src):
  """Remove a comma that sits right before a closing bracket, unless removing
  it would change the meaning: the sole comma in a parenthesized single-element
  tuple, or in a single-element tuple subscript (a[1,])."""
  starts = line_starts(src)
  stack = []
  prev = None
  str_depth = 0
  edits = []
  for tok in tokens_of(src):
    kind = tok.type
    if kind in STR_STARTS:
      if str_depth == 0 and stack:
        stack[-1]['last_comma'] = None
      str_depth += 1
      prev = tok
      continue
    if kind in STR_ENDS:
      str_depth -= 1
      prev = tok
      continue
    if str_depth > 0:
      continue
    if kind == tokenize.NEWLINE:
      prev = None  # a new statement starts, so a bracket at its start is no call or subscript: (a,) = f()
      continue
    if kind in SKIP_TYPES:
      continue
    if kind == tokenize.OP and tok.string in OPENERS:
      callable_before = prev is not None and (
        (prev.type == tokenize.NAME and not keyword.iskeyword(prev.string)) or
        (prev.type == tokenize.OP and prev.string in CLOSERS) or
        prev.type == tokenize.STRING or prev.type in STR_ENDS
      )
      list_keyword_before = (
        prev is not None and prev.type == tokenize.NAME and
        keyword.iskeyword(prev.string) and prev.string in NO_TUPLE_KEYWORDS
      )
      if stack:
        stack[-1]['last_comma'] = None
      stack.append({
        'bracket': tok.string,
        'tuple_like': tok.string == '(' and not callable_before and not list_keyword_before,
        'subscript': tok.string == '[' and callable_before,
        'commas': 0,
        'last_comma': None
      })
      prev = tok
      continue
    if kind == tokenize.OP and tok.string in CLOSERS and stack:
      frame = stack.pop()
      keep = frame['last_comma'] is not None and frame['commas'] == 1 and (frame['tuple_like'] or frame['subscript'])
      if frame['last_comma'] is not None and not keep:
        comma = frame['last_comma']
        begin = offset(starts, comma.start)
        comma_end = offset(starts, comma.end)
        closer_start = offset(starts, tok.start)
        gap_text = src[comma_end:closer_start]
        end = closer_start if '\n' not in gap_text else comma_end
        edits.append((begin, end, ''))
      if stack:
        stack[-1]['last_comma'] = None
      prev = tok
      continue
    if kind == tokenize.OP and tok.string == ',' and stack:
      stack[-1]['commas'] += 1
      stack[-1]['last_comma'] = tok
      prev = tok
      continue
    if stack:
      stack[-1]['last_comma'] = None
    prev = tok
  return splice(src, edits)

# --- pass: indentation ---

NO_ROW = SKIP_TYPES - {tokenize.COMMENT}

def statements(tokens, lines):
  """List of (first_row, last_row, old_indent, new_indent) for every logical line."""
  found = []
  depth = 0
  current = None
  for tok in tokens:
    if tok.type == tokenize.INDENT:
      depth += 1
    elif tok.type == tokenize.DEDENT:
      depth -= 1
    elif tok.type == tokenize.NEWLINE:
      if current is not None:
        found.append((*current, tok.end[0]))
        current = None
    elif tok.type not in SKIP_TYPES and current is None:
      row = tok.start[0]
      current = (row, width(lines[row - 1]), depth * INDENT)
  return [(first, last, old, new) for first, old, new, last in found]

def comment_indent(row, old, stmts):
  """New indent for a comment-only line, based on the statements around it."""
  # stmts is in file order, so the statements above and below the row are found by bisecting
  above = bisect_left(stmts, row, key = lambda stmt: stmt[1])  # how many end before this row
  below = bisect_right(stmts, row, key = lambda stmt: stmt[0])  # first one that starts after it
  prev = stmts[above - 1] if above else None
  nxt = stmts[below] if below < len(stmts) else None
  for stmt in (nxt, prev):
    if stmt is not None and stmt[2] == old:
      return stmt[3]
  stmt = nxt or prev
  if stmt is None:
    return old
  return max(0, old + stmt[3] - stmt[2])

def ends_line(tokens, i):
  """True if the bracket at tokens[i] is the last thing on its line (a hanging bracket)."""
  after = tokens[i + 1].type if i + 1 < len(tokens) else None
  if after == tokenize.COMMENT and i + 2 < len(tokens):
    after = tokens[i + 2].type
  return after == tokenize.NL

def indent_targets(tokens, lines, stmts, begins_in):
  """New indent for the first token of each row. Returns (targets, covered_rows).
  Inside a hanging bracket (one that ends its line) contents go one INDENT in from the row
  holding the bracket, and a closing bracket goes back to that row. Any other continuation
  line keeps its alignment and is just shifted along with its statement."""
  starts = {first: (last, old, new) for first, last, old, new in stmts}
  covered = set()
  targets = {}
  shifts = {}
  stack = []
  depth = 0
  done = 0
  delta = 0
  for i, tok in enumerate(tokens):
    kind = tok.type
    if kind in STR_ENDS:
      depth -= 1
      continue
    if depth > 0:
      if kind in STR_STARTS:
        depth += 1
      continue
    row = tok.start[0]
    if row > done and kind not in NO_ROW and row not in begins_in:
      done = row
      line = lines[row - 1]
      target = None
      if row in starts:
        last, old, new = starts[row]
        covered.update(range(row, last + 1))
        delta = new - old
        stack = []
        target = new
      elif row in covered:
        if not stack:
          target = max(0, width(line) + delta)
        else:
          base, hanging, moved = stack[-1]
          if hanging:
            closing = kind == tokenize.OP and tok.string in CLOSERS
            target = base if closing else base + INDENT
          else:
            target = max(0, width(line) + moved)
      if target is not None:
        targets[row] = target
        shifts[row] = target - width(line)
    if kind == tokenize.OP and tok.string in OPENERS:
      base = targets.get(row, width(lines[row - 1]))
      stack.append((base, ends_line(tokens, i), shifts.get(row, delta)))
    elif kind == tokenize.OP and tok.string in CLOSERS and stack:
      stack.pop()
    if kind in STR_STARTS:
      depth += 1
  return targets, covered

def fix_indent(src):
  tokens = tokens_of(src)
  lines = source_lines(src)
  begins_in, _ = string_rows(src)
  stmts = statements(tokens, lines)
  targets, covered = indent_targets(tokens, lines, stmts, begins_in)
  out = list(lines)
  for row, target in targets.items():
    out[row - 1] = ' ' * target + lines[row - 1].lstrip(' \t')
  for row, line in enumerate(lines, 1):
    if row in covered or row in begins_in:
      continue
    body = line.lstrip(' \t')
    if body.startswith('#'):
      out[row - 1] = ' ' * comment_indent(row, width(line), stmts) + body
  return ''.join(out)

# --- pass: import order ---

@cache
def is_local(top):
  return Path(top).is_dir() or Path(top + '.py').is_file()

def import_group(node):
  """0 = __future__, 1 = system libs, 2 = 3rd party libs, 3 = local files."""
  if isinstance(node, ast.ImportFrom):
    if node.level:
      return 3
    top = (node.module or '').split('.')[0]
  else:
    top = node.names[0].name.split('.')[0]
  if top == '__future__':
    return 0
  if top in sys.stdlib_module_names:
    return 1
  if top and is_local(top):
    return 3
  return 2

def length_key(text):
  """Shortest first, then alphabetical."""
  return len(text), text.lower(), text

def name_kind(name):
  """0 = class (PascalCase), 1 = func (lowercase/mixed), 2 = variable (ALL_CAPS constant)."""
  bare = name.lstrip('_') or name
  if bare.isupper():
    return 2
  if bare[:1].isupper():
    return 0
  return 1

def import_lines(node, lines):
  """Source lines of an import, and the text it is sorted by. A simple one-line 'from' import
  also gets its names sorted. The tree is shared, so the node is copied rather than changed."""
  chunk = lines[node.lineno - 1 : node.end_lineno]
  simple = len(chunk) == 1 and not any(mark in chunk[0] for mark in '#(;')
  if isinstance(node, ast.ImportFrom) and simple:
    names = sorted(node.names, key = lambda alias: (name_kind(alias.name), alias.name.lower(), alias.name))
    text = ast.unparse(copy.replace(node, names = names))
    return [text + '\n'], text
  return chunk, ast.unparse(node)

def import_runs(tree):
  """Lists of consecutive top-level import statements."""
  runs = [[]]
  for node in tree.body:
    if isinstance(node, (ast.Import, ast.ImportFrom)):
      runs[-1].append(node)
    elif runs[-1]:
      runs.append([])
  return [run for run in runs if run]

def fix_imports(src):
  lines = list(source_lines(src))
  if lines and not lines[-1].endswith('\n'):
    lines[-1] += '\n'
  edits = []
  for run in import_runs(parse(src)):
    first = run[0].lineno
    last = run[-1].end_lineno
    inside = {row for node in run for row in range(node.lineno, node.end_lineno + 1)}
    stray = any(row not in inside and lines[row - 1].strip() for row in range(first, last + 1))
    shared = any(a.end_lineno >= b.lineno for a, b in zip(run, run[1:], strict = False))
    if stray or shared:
      continue
    items = []
    for node in run:
      chunk, text = import_lines(node, lines)
      is_from = isinstance(node, ast.ImportFrom)
      items.append((import_group(node), is_from, *length_key(text), chunk))
    items.sort(key = lambda item: item[:5])
    new = [line for item in items for line in item[5]]
    after = lines[last:]
    blanks = 0
    while blanks < len(after) and not after[blanks].strip():
      blanks += 1
    if blanks < len(after):
      new.append('\n')
      last += blanks
    edits.append((first, last, new))
  for first, last, new in sorted(edits, reverse = True):
    lines[first - 1 : last] = new
  return ''.join(lines)

# --- pass: whitespace and blank lines (Python files) ---

def fix_whitespace(src):
  """Strip trailing spaces, collapse blank-line runs to one, end with a single newline."""
  begins_in, ends_in = string_rows(src)
  out = []
  prev_blank = False
  for row, line in enumerate(source_lines(src), 1):
    body = line.rstrip('\r\n')
    eol = '\n' if line != body else ''
    if row not in ends_in:
      body = body.rstrip(' \t')
    blank = not body.strip() and row not in begins_in and row not in ends_in
    if blank and prev_blank:
      continue
    out.append(body + eol)
    prev_blank = blank
  text = ''.join(out).rstrip()
  if not text:
    return ''
  return text + '\n'

# --- pass: newline normalization (non-Python text files) ---

def normalize_text(text, keep_trailing = False):
  text = text.replace('\r\n', '\n').replace('\r', '\n')
  if not keep_trailing:
    text = '\n'.join(line.rstrip(' \t') for line in text.split('\n'))
  stripped = text.rstrip('\n')
  return stripped + '\n' if stripped else ''

# --- pass: TOML indentation and trailing commas ---

TOML_QUOTES = ('"', "'")

def toml_scan(lines):
  """Walk TOML lines once. Returns (indents, cuts): the wanted indent for each row that
  starts outside a multiline string, and the column spans to delete on each row."""
  indents = {}
  cuts = {}
  stack = []  # one slot per open bracket: (row, col) of a comma waiting for its closer, or None
  quote = None  # delimiter of the multiline string we are inside
  for row, line in enumerate(lines):
    if quote is None:
      body = line.lstrip(' \t')
      if body:
        closing = bool(stack) and body[0] in ']}'
        indents[row] = INDENT * (len(stack) - int(closing))
    col = 0
    while col < len(line):
      char = line[col]
      if quote:
        if quote[0] == '"' and char == '\\':
          col += 2
        elif line.startswith(quote, col):
          quote = None
          col += 3
        else:
          col += 1
        continue
      if char in ' \t':
        col += 1
        continue
      if char == '#':
        break
      if char == ',' and stack:
        stack[-1] = (row, col)
        col += 1
        continue
      if char in ']}' and stack:
        pending = stack.pop()
        if pending:
          pending_row, pending_col = pending
          end = col if pending_row == row else pending_col + 1
          cuts.setdefault(pending_row, []).append((pending_col, end))
        if stack:
          stack[-1] = None
        col += 1
        continue
      if stack:
        stack[-1] = None
      if char in '[{':
        stack.append(None)
        col += 1
      elif char in TOML_QUOTES:
        triple = char * 3
        if line.startswith(triple, col):
          quote = triple
          col += 3
        else:
          col += 1
          while col < len(line) and line[col] != char:
            col += 2 if char == '"' and line[col] == '\\' else 1
          col += 1
      else:
        col += 1
  return indents, cuts

def fix_toml(text):
  """Indent array and inline table contents by INDENT per bracket level (a closing bracket
  goes back one level, everything else starts at column 0) and drop commas right before a
  closing bracket."""
  lines = text.split('\n')
  indents, cuts = toml_scan(lines)
  for row, spans in cuts.items():
    for begin, end in sorted(spans, reverse = True):
      lines[row] = lines[row][:begin] + lines[row][end:]
  for row, indent in indents.items():
    lines[row] = ' ' * indent + lines[row].lstrip(' \t')
  return '\n'.join(lines)

def format_text(path, text):
  text = normalize_text(text, path.suffix == '.md')
  if path.suffix == '.toml':
    text = normalize_text(fix_toml(text))  # again, since removing a comma can leave a trailing space
  return text

# --- pipeline ---

PASSES = [fix_quotes, fix_trailing_commas, fix_spacing, fix_indent, fix_imports, fix_whitespace]

STATEMENT_FIELDS = ('body', 'orelse', 'finalbody', 'handlers', 'cases')

def import_nodes(tree):
  """Every import statement in the tree. Statements only ever sit in these list fields, so
  there is no need to look inside the expressions."""
  todo = [tree]
  while todo:
    node = todo.pop()
    for field in STATEMENT_FIELDS:
      for child in getattr(node, field, ()):
        if isinstance(child, (ast.Import, ast.ImportFrom)):
          yield child
        else:
          todo.append(child)

def canonical(src):
  """AST dump that ignores import order, so the import pass is allowed to reorder them."""
  tree = ast.parse(src)  # not parse(), this tree gets modified
  for node in import_nodes(tree):
    node.names.sort(key = ast.dump)
  body = []
  run = []
  for node in [*tree.body, None]:
    if isinstance(node, (ast.Import, ast.ImportFrom)):
      run.append(node)
      continue
    body += sorted(run, key = ast.dump)
    run = []
    if node is not None:
      body.append(node)
  tree.body = body
  return ast.dump(tree)

def same_tree(old, new):
  try:
    return canonical(old) == canonical(new)
  except SyntaxError:
    return False

def format_source_checked(src):
  """Run every Python pass, checking after each one that the tree is the same. Slow, but it
  can say which pass broke it."""
  try:
    ast.parse(src)
  except SyntaxError as exc:
    return src, f'syntax error: {exc.msg}'
  current = src
  for step in PASSES:
    new = step(current)
    if new != current and not same_tree(current, new):
      return src, f'{step.__name__} changed the AST'
    current = new
  return current, None

def format_source(src):
  """Run every Python pass. Returns (new_src, error); on error the source is unchanged.
  The tree is only compared once, after the last pass. If that fails (or a pass chokes on the
  broken text an earlier one left), the checked version works out which pass is to blame."""
  try:
    parse(src)
  except SyntaxError as exc:
    return src, f'syntax error: {exc.msg}'
  current = src
  try:
    for step in PASSES:
      current = step(current)
  except Exception:  # noqa: BLE001
    return format_source_checked(src)
  if current == src or same_tree(src, current):
    return current, None
  return format_source_checked(src)

# --- naming checks ---

@cache
def ok_name(name):
  """Every _-separated part must be all uppercase or all lowercase."""
  return all(part == part.upper() or part == part.lower() for part in name.split('_'))

NAMED_NODES = {
  ast.ClassDef, ast.FunctionDef, ast.AsyncFunctionDef, ast.arg, ast.Name,
  ast.Attribute, ast.ExceptHandler, ast.MatchAs, ast.MatchStar
}

def check_names(src, path):
  ignored = {n for n, line in enumerate(src.split('\n'), 1) if NAMING_IGNORE in line}
  found = []
  for node in ast.walk(parse(src)):
    if type(node) not in NAMED_NODES:
      continue
    if isinstance(node, ast.ClassDef):
      first = node.name.lstrip('_')[:1]
      if first and not first.isupper():
        found.append((node.lineno, f'class {node.name}: must start with an uppercase letter'))
      continue
    name = None
    row = 0
    if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef)):
      name, row = node.name, node.lineno
    elif isinstance(node, ast.arg):
      name, row = node.arg, node.lineno
    elif isinstance(node, ast.Name) and isinstance(node.ctx, ast.Store):
      name, row = node.id, node.lineno
    elif isinstance(node, ast.Attribute) and isinstance(node.ctx, ast.Store):
      if isinstance(node.value, ast.Name) and node.value.id in ('self', 'cls'):
        name, row = node.attr, node.lineno
    elif isinstance(node, (ast.ExceptHandler, ast.MatchAs, ast.MatchStar)):
      name, row = node.name, node.lineno
    if name and not ok_name(name):
      found.append((row, f'{name}: not snake_case (each _ part must be all upper or all lower)'))
  return [f'{path}:{row}: {msg}' for row, msg in sorted(found) if row not in ignored]

# --- self test ---

CASES = [
  ('quotes', 'x = "a"\ny = "it\'s"\nz = f"{a}"\nw = "say \\"hi\\""\n', "x = 'a'\ny = \"it's\"\nz = f'{a}'\nw = 'say \"hi\"'\n"),
  ('quotes keep triple', 'def f():\n  """Doc."""\n', 'def f():\n  """Doc."""\n'),
  ('operators', 'x=1+2*3\ny=a**-b\n', 'x = 1 + 2 * 3\ny = a ** -b\n'),
  ('unary and star', 'f(*args,**kw)\nz=[-1,+2,~3]\n', 'f(*args, **kw)\nz = [-1, +2, ~3]\n'),
  ('kwargs and defaults', 'def f(a: int=1, *, b=2)->int:\n  return f(a=1,b=-2)\n', 'def f(a: int = 1, *, b = 2) -> int:\n  return f(a = 1, b = -2)\n'),
  ('comma removed', 'x = (1 ,2,)\n', 'x = (1, 2)\n'),
  ('comma single tuple kept', 'y = (1, )\nv = (1,)\n', 'y = (1, )\nv = (1,)\n'),
  ('comma call always removed', 'z = f(1,2,)\n', 'z = f(1, 2)\n'),
  ('comma list always removed', 'w = [1,]\n', 'w = [1]\n'),
  ('comma dict always removed', 'd = {1: 2,}\n', 'd = {1: 2}\n'),
  ('comma subscript tuple kept', 'a[1,]\n', 'a[1,]\n'),
  ('comma unpacking tuple kept', "x = a\n(v,) = f()\ny = [b]\n(w,) = f()\nz = 'c'\n(u,) = f()\n", "x = a\n(v,) = f()\ny = [b]\n(w,) = f()\nz = 'c'\n(u,) = f()\n"),
  ('comma multiline kept across lines', 'x = (\n  1,\n  2,\n)\n', 'x = (\n  1,\n  2\n)\n'),
  ('comma fstring element not eaten', "x = ['a', FENCE, f'{ROOT.name}/']\n", "x = ['a', FENCE, f'{ROOT.name}/']\n"),
  ('fstring untouched', "x = f'{a=}{b+1}'\n", "x = f'{a=}{b+1}'\n"),
  ('except star', 'try:\n  pass\nexcept* E:\n  pass\n', 'try:\n  pass\nexcept* E:\n  pass\n'),
  ('indent', 'if a:\n    b = (1,\n        2)\n    # note\n    c = 1\n', 'if a:\n  b = (1,\n      2)\n  # note\n  c = 1\n'),
  ('hanging layout kept', "if a:\n  await send({'t': 1, 's': 2,\n      'h': [3]})\n", "if a:\n  await send({'t': 1, 's': 2,\n      'h': [3]})\n"),
  ('hanging brackets', 'def f(\n      a,\n      b\n):\n  return g(\n    h(\n        1\n    ),\n    2\n  )\n', 'def f(\n  a,\n  b\n):\n  return g(\n    h(\n      1\n    ),\n    2\n  )\n'),
  ('blank lines', 'a = 1   \n\n\n\nb = 2\n\n\n', 'a = 1\n\nb = 2\n'),
  ('crlf to lf', 'a = 1\r\nb = 2\r\n', 'a = 1\nb = 2\n'),
  ('strings untouched', 's = """\n\n\n  x   \n"""\n', 's = """\n\n\n  x   \n"""\n'),
  ('imports by length', 'import sys\nimport asyncio\nfrom enum import IntEnum\nimport os\n', 'import os\nimport sys\nimport asyncio\nfrom enum import IntEnum\n'),
  ('imports same length alphabetical', 'import re\nimport os\n', 'import os\nimport re\n'),
  ('imports in groups', 'from .x import y\nimport orjson\nimport sys\nimport os\nz = 1\n', 'import os\nimport sys\nimport orjson\nfrom .x import y\n\nz = 1\n'),
  ('imports future stays first', 'from __future__ import annotations\nimport os\n', 'from __future__ import annotations\nimport os\n'),
  ('imports blank lines', 'import sys\n\nimport os\n\n\n\nz = 1\n', 'import os\nimport sys\n\nz = 1\n'),
  ('imports names sorted', 'from enum import IntEnum, auto, Flag as F\n', 'from enum import Flag as F, IntEnum, auto\n'),
  ('imports comment left alone', 'import sys\n# note\nimport os\n', 'import sys\n# note\nimport os\n'),
  ('imports multiline kept', 'import sys\nfrom enum import (\n  IntEnum,\n  auto,\n)\nimport os\n', 'import os\nimport sys\nfrom enum import (\n  IntEnum,\n  auto\n)\n'),
  ('imports not at top', 'def f():\n  import sys\n  import os\n', 'def f():\n  import sys\n  import os\n'),
  ('imports import before from', 'from a import b\nimport numpy_extra\n', 'import numpy_extra\nfrom a import b\n'),
  ('imports lazy', 'lazy import sys\nimport os\nlazy from enum import IntEnum, auto, Flag as F\n', 'import os\nlazy import sys\nlazy from enum import Flag as F, IntEnum, auto\n'),
  ('comments around statements', '# head\nif a:\n    b = 1\n      # between\n    c = 2\n# tail\n', '# head\nif a:\n  b = 1\n    # between\n  c = 2\n# tail\n'),
  ('comments between blocks', 'class A:\n    def f(self):\n        return 1\n        # end of f\n    # between\n\n# top\n', 'class A:\n  def f(self):\n    return 1\n    # end of f\n# between\n\n# top\n'),
  ('comment above a dedent', 'if a:\n    if b:\n        c = 1\n  # odd\n    d = 2\n', 'if a:\n  if b:\n    c = 1\n# odd\n  d = 2\n')
]
NAME_CASES = [
  ('thing = 1\npoint_RTS = 2\nRTS_point = 3\nRTS = 4\nclass ABC: pass\nclass CoolCar: pass\n', 0),
  ('blueThing = 1\n', 1),
  ('class aBC: pass\nclass cOOlCAr: pass\n', 2),
  ('def doThing(selfThing): pass\n', 2),
  ('blueThing = 1  # naming: ignore\n', 0)
]
TEXT_CASES = [
  ('no trailing newline', 'readme body', 'readme body\n'),
  ('crlf', 'a = 1\r\nb = 2', 'a = 1\nb = 2\n'),
  ('many trailing blanks collapse to one newline', 'a\n\n\n\n', 'a\n'),
  ('mid-file blanks kept', 'a\n\nb\n', 'a\n\nb\n'),
  ('empty file stays empty', '', ''),
  ('trailing spaces', '- run: uv build \nname: x\t\n', '- run: uv build\nname: x\n')
]
TOML_CASES = [
  ('toml indent', "a = [\n'x',\n    'y'\n]\n", "a = [\n  'x',\n  'y'\n]\n"),
  ('toml comma multiline', "a = [\n  'x',\n  'y',\n]\n", "a = [\n  'x',\n  'y'\n]\n"),
  ('toml comma one line', "a = ['x', 'y', ]\nb = ['x', 'y',]\n", "a = ['x', 'y']\nb = ['x', 'y']\n"),
  ('toml comment after comma', "a = [\n  'x', # one\n  'y', # two\n]\n", "a = [\n  'x', # one\n  'y' # two\n]\n"),
  ('toml headers and keys', '[tool.x]\n  a = 1\n  [tool.y]\nb = 2\n', '[tool.x]\na = 1\n[tool.y]\nb = 2\n'),
  ('toml strings untouched', "a = '''\n  x,\n   ]\n'''\nb = ['#', 'a,]']\n", "a = '''\n  x,\n   ]\n'''\nb = ['#', 'a,]']\n"),
  ('toml inline table', 'a = {x = [1, 2,], y = 3,}\n', 'a = {x = [1, 2], y = 3}\n')
]

def selftest():
  failures = 0
  for label, before, want in CASES:
    got, error = format_source(before)
    again, _ = format_source(got)
    if error or got != want or again != got:
      failures += 1
      print(f'FAIL {label}: error = {error}\n  want {want!r}\n  got  {got!r}\n  again {again!r}')
  for src, count in NAME_CASES:
    got = check_names(src, 'test')
    if len(got) != count:
      failures += 1
      print(f'FAIL names {src!r}: wanted {count}, got {got}')
  for label, before, want in TEXT_CASES:
    got = normalize_text(before)
    if got != want:
      failures += 1
      print(f'FAIL text {label}: want {want!r}, got {got!r}')
  for label, before, want in TOML_CASES:
    got = format_text(Path('x.toml'), before)
    if got != want or format_text(Path('x.toml'), got) != got:
      failures += 1
      print(f'FAIL {label}: want {want!r}, got {got!r}')
  if 'No newline' not in diff('x', 'a', 'a\n') or '\\r' not in diff('x', 'a\r\n', 'a\n'):
    failures += 1
    print('FAIL diff output')

  def breaks_tree(src):
    return src.replace('1', '2')

  saved = PASSES[:]
  PASSES[:] = [fix_quotes, breaks_tree]
  try:
    got = format_source('x = "a" + 1\n')
  finally:
    PASSES[:] = saved
  want = ('x = "a" + 1\n', 'breaks_tree changed the AST')
  if got != want:
    failures += 1
    print(f'FAIL error names the pass: want {want!r}, got {got!r}')
  total = len(CASES) + len(NAME_CASES) + len(TEXT_CASES) + len(TOML_CASES) + 2  # + the diff and AST checks
  print(f'{total - failures} passed, {failures} failed')
  return 1 if failures else 0

# --- file discovery ---

def find_files():
  """Every *.py file in the repo, and the other text files that should still end with exactly
  one LF. One walk that never goes into EXCLUDE_DIRS, instead of one full walk per pattern."""
  python = []
  text = []
  for folder, dirs, names in os.walk('.'):
    dirs[:] = [name for name in dirs if name not in EXCLUDE_DIRS]
    for name in names:
      lowered = os.path.normcase(name)
      if lowered.endswith('.py'):
        python.append(Path(folder, name))
      elif TEXT_NAME.match(lowered):
        text.append(Path(folder, name))
  return sorted(python), sorted(text)

# --- command line ---

def ruff(*args):
  # run the binary itself when it sits next to Python, 'python -m ruff' just starts another interpreter
  binary = Path(sysconfig.get_path('scripts'), 'ruff.exe' if os.name == 'nt' else 'ruff')
  command = [str(binary)] if binary.is_file() else [sys.executable, '-m', 'ruff']
  return subprocess.run([*command, *args], check = False).returncode

def read(path):
  with path.open(encoding = 'utf-8', newline = '') as file:
    return file.read()

def write(path, text):
  with path.open('w', encoding = 'utf-8', newline = '') as file:
    file.write(text)

@cache
def use_color():
  if not sys.stdout.isatty() or 'NO_COLOR' in os.environ:
    return False
  if os.name == 'nt':
    os.system('')  # enables ANSI colors in the Windows console
  return True

def diff(path, old, new):
  """Unified diff, colored like git when printing to a terminal."""
  import difflib  # only --diff needs it, and on 3.15 importing it costs ~20 ms (it pulls in dataclasses)
  color = use_color()
  before = io.StringIO(old).readlines()
  after = io.StringIO(new).readlines()
  out = []
  for i, line in enumerate(difflib.unified_diff(before, after, str(path), str(path))):
    text = line.rstrip('\n')
    if text.endswith('\r'):
      text = text[:-1] + '\\r'
    code = None
    if i < 2:
      code = '1'
    elif text.startswith('@@'):
      code = '36'
    elif text.startswith('-'):
      code = '31'
    elif text.startswith('+'):
      code = '32'
    out.append(f'\033[{code}m{text}\033[0m' if color and code else text)
    if not line.endswith('\n'):
      out.append('\\ No newline at end of file')
  return '\n'.join(out)

def main(argv):
  mode = argv[0] if argv else ''
  if len(argv) > 1 or mode not in MODES:
    print(__doc__)
    return 2
  if mode == '--selftest':
    return selftest()

  py_files, txt_files = find_files()
  before_py = {p: read(p) for p in py_files}

  if mode == '--check':
    failed = ruff('check', '.') != 0
  elif mode == '--diff':
    failed = ruff('check', '--diff', '.') != 0
  else:
    failed = ruff('check', '--fix', '--show-fixes', '.') != 0

  for path in py_files:
    current = before_py[path] if mode else read(path)
    new, error = format_source(current)
    if error:
      print(f'Skipped {path}: {error}')
      failed = True
      continue
    if mode == '--check' and new != current:
      print(f'Would reformat {path}')
      failed = True
    elif mode == '--diff' and new != current:
      print(diff(path, current, new))
    elif not mode:
      if new != current:
        write(path, new)
      if new != before_py[path]:
        print(f'Reformatted {path}')
    for message in check_names(new if not mode else current, path):
      print(message)
      failed = True

  for path in txt_files:
    try:
      current = read(path)
    except UnicodeDecodeError:
      continue
    new = format_text(path, current)
    if new == current:
      continue
    if mode == '--check':
      print(f'Would fix formatting in {path}')
      failed = True
    elif mode == '--diff':
      print(diff(path, current, new))
    else:
      write(path, new)
      print(f'Fixed formatting in {path}')

  return 1 if failed else 0

if __name__ == '__main__':
  sys.exit(main(sys.argv[1:]))
