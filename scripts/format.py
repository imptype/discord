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
*.env, LICENSE) files use LF and end with 1 newline.

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
import ast
import sys
import difflib
import keyword
import tokenize
import subprocess
from pathlib import Path

INDENT = 2
NAMING_IGNORE = '# naming: ignore'
MODES = ('', '--check', '--diff', '--selftest')

EXCLUDE_DIRS = {'.git', '.venv', 'venv', 'node_modules', '__pycache__', '.mypy_cache', '.ruff_cache'}
TEXT_GLOBS = ('*.md', '*.toml', '*.lock', '*.env', '*.yml', '*.yaml', '.gitignore', 'LICENSE', 'LICENSE.*')

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
CLOSERS = {')', ']', '}'}

# --- helpers ---

def tokens_of(src):
  return list(tokenize.generate_tokens(io.StringIO(src).readline))

def line_starts(src):
  starts = [0]
  for line in io.StringIO(src).readlines():
    starts.append(starts[-1] + len(line))
  return starts

def offset(starts, pos):
  return starts[pos[0] - 1] + pos[1]

def splice(src, edits):
  for begin, end, text in sorted(edits, reverse = True):
    src = src[:begin] + text + src[end:]
  return src

def width(line):
  body = line.lstrip(' \t')
  return len(line[: len(line) - len(body)].expandtabs(8))

def string_rows(tokens):
  """Rows that start inside a string, and rows that end inside one."""
  begins_in = set()
  ends_in = set()
  stack = []
  for tok in tokens:
    if tok.type in STR_STARTS:
      stack.append(tok.start[0])
    elif tok.type in STR_ENDS:
      first = stack.pop()
      begins_in.update(range(first + 1, tok.end[0] + 1))
      ends_in.update(range(first, tok.end[0]))
    elif tok.type == tokenize.STRING:
      begins_in.update(range(tok.start[0] + 1, tok.end[0] + 1))
      ends_in.update(range(tok.start[0], tok.end[0]))
  return begins_in, ends_in

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
  for tok in tokens_of(src):
    if tok.type in STR_STARTS:
      if depth == 0:
        first = tok
      depth += 1
    elif tok.type in STR_ENDS:
      depth -= 1
      if depth == 0:
        edits += quote_edit(src, starts, first, tok)
    elif tok.type == tokenize.STRING and depth == 0:
      edits += quote_edit(src, starts, tok, tok)
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
    before, after = wants(tok, prev)
    if prev is not None and adjacent and prev.end[0] == tok.start[0]:
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
    if kind in SKIP_TYPES:
      continue
    callable_before = prev is not None and (
      (prev.type == tokenize.NAME and not keyword.iskeyword(prev.string)) or
      (prev.type == tokenize.OP and prev.string in CLOSERS) or
      prev.type == tokenize.STRING or prev.type in STR_ENDS
    )
    list_keyword_before = (
      prev is not None and prev.type == tokenize.NAME and
      keyword.iskeyword(prev.string) and prev.string in NO_TUPLE_KEYWORDS
    )
    if kind == tokenize.OP and tok.string in ('(', '[', '{'):
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
  prev = None
  nxt = None
  for stmt in stmts:
    if stmt[1] < row:
      prev = stmt
    elif stmt[0] > row and nxt is None:
      nxt = stmt
  for stmt in (nxt, prev):
    if stmt is not None and stmt[2] == old:
      return stmt[3]
  stmt = nxt or prev
  if stmt is None:
    return old
  return max(0, old + stmt[3] - stmt[2])

def fix_indent(src):
  tokens = tokens_of(src)
  lines = io.StringIO(src).readlines()
  begins_in, _ = string_rows(tokens)
  stmts = statements(tokens, lines)
  covered = set()
  out = list(lines)
  for first, last, old, new in stmts:
    covered.update(range(first, last + 1))
    delta = new - old
    for row in range(first, last + 1):
      line = lines[row - 1]
      body = line.lstrip(' \t')
      if row in begins_in or not body.strip():
        continue
      target = new if row == first else max(0, width(line) + delta)
      out[row - 1] = ' ' * target + body
  for row, line in enumerate(lines, 1):
    if row in covered or row in begins_in:
      continue
    body = line.lstrip(' \t')
    if body.startswith('#'):
      out[row - 1] = ' ' * comment_indent(row, width(line), stmts) + body
  return ''.join(out)

# --- pass: import order ---

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
  if top and (Path(top).is_dir() or Path(top + '.py').is_file()):
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
  """Source lines of an import. A simple one-line 'from' import also gets its names sorted."""
  chunk = lines[node.lineno - 1 : node.end_lineno]
  simple = len(chunk) == 1 and not any(mark in chunk[0] for mark in '#(;')
  if isinstance(node, ast.ImportFrom) and simple:
    node.names.sort(key = lambda alias: (name_kind(alias.name), alias.name.lower(), alias.name))
    chunk = [ast.unparse(node) + '\n']
  return chunk

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
  lines = io.StringIO(src).readlines()
  if lines and not lines[-1].endswith('\n'):
    lines[-1] += '\n'
  edits = []
  for run in import_runs(ast.parse(src)):
    first = run[0].lineno
    last = run[-1].end_lineno
    inside = {row for node in run for row in range(node.lineno, node.end_lineno + 1)}
    stray = any(row not in inside and lines[row - 1].strip() for row in range(first, last + 1))
    shared = any(a.end_lineno >= b.lineno for a, b in zip(run, run[1:], strict = False))
    if stray or shared:
      continue
    items = []
    for node in run:
      chunk = import_lines(node, lines)
      is_from = isinstance(node, ast.ImportFrom)
      items.append((import_group(node), is_from, *length_key(ast.unparse(node)), chunk))
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
  begins_in, ends_in = string_rows(tokens_of(src))
  out = []
  prev_blank = False
  for row, line in enumerate(io.StringIO(src).readlines(), 1):
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

# --- pipeline ---

PASSES = [fix_quotes, fix_trailing_commas, fix_spacing, fix_indent, fix_imports, fix_whitespace]

def canonical(src):
  """AST dump that ignores import order, so the import pass is allowed to reorder them."""
  tree = ast.parse(src)
  for node in ast.walk(tree):
    if isinstance(node, (ast.Import, ast.ImportFrom)):
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

def format_source(src):
  """Run every Python pass. Returns (new_src, error); on error the source is unchanged."""
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

# --- naming checks ---

def ok_name(name):
  """Every _-separated part must be all uppercase or all lowercase."""
  return all(part == part.upper() or part == part.lower() for part in name.split('_'))

def check_names(src, path):
  ignored = {n for n, line in enumerate(src.split('\n'), 1) if NAMING_IGNORE in line}
  found = []
  for node in ast.walk(ast.parse(src)):
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
  ('comma multiline kept across lines', 'x = (\n  1,\n  2,\n)\n', 'x = (\n  1,\n  2\n)\n'),
  ('comma fstring element not eaten', "x = ['a', FENCE, f'{ROOT.name}/']\n", "x = ['a', FENCE, f'{ROOT.name}/']\n"),
  ('fstring untouched', "x = f'{a=}{b+1}'\n", "x = f'{a=}{b+1}'\n"),
  ('except star', 'try:\n  pass\nexcept* E:\n  pass\n', 'try:\n  pass\nexcept* E:\n  pass\n'),
  ('indent', 'if a:\n    b = (1,\n        2)\n    # note\n    c = 1\n', 'if a:\n  b = (1,\n      2)\n  # note\n  c = 1\n'),
  ('hanging layout kept', "if a:\n  await send({'t': 1, 's': 2,\n      'h': [3]})\n", "if a:\n  await send({'t': 1, 's': 2,\n      'h': [3]})\n"),
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
  ('imports import before from', 'from a import b\nimport numpy_extra\n', 'import numpy_extra\nfrom a import b\n')
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
  if 'No newline' not in diff('x', 'a', 'a\n') or '\\r' not in diff('x', 'a\r\n', 'a\n'):
    failures += 1
    print('FAIL diff output')
  total = len(CASES) + len(NAME_CASES) + len(TEXT_CASES)
  print(f'{total - failures} passed, {failures} failed')
  return 1 if failures else 0

# --- file discovery ---

def excluded(path):
  return any(part in EXCLUDE_DIRS for part in path.parts)

def python_files():
  """Every tracked *.py file in the repo, wherever it lives."""
  return sorted(p for p in Path('.').rglob('*.py') if not excluded(p))

def text_files():
  """Non-Python text files that should still end with exactly one LF."""
  found = set()
  for pattern in TEXT_GLOBS:
    found.update(p for p in Path('.').rglob(pattern) if not excluded(p))
  return sorted(found)

# --- command line ---

def ruff(*args):
  return subprocess.run([sys.executable, '-m', 'ruff', *args], check = False).returncode

def read(path):
  with path.open(encoding = 'utf-8', newline = '') as file:
    return file.read()

def write(path, text):
  with path.open('w', encoding = 'utf-8', newline = '') as file:
    file.write(text)

def use_color():
  if not sys.stdout.isatty() or 'NO_COLOR' in os.environ:
    return False
  if os.name == 'nt':
    os.system('')  # enables ANSI colors in the Windows console
  return True

def diff(path, old, new):
  """Unified diff, colored like git when printing to a terminal."""
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

  py_files = python_files()
  txt_files = text_files()
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
    new = normalize_text(current, path.suffix == '.md')
    if new == current:
      continue
    if mode == '--check':
      print(f'Would fix newline in {path}')
      failed = True
    elif mode == '--diff':
      print(diff(path, current, new))
    else:
      write(path, new)
      print(f'Fixed newline in {path}')

  return 1 if failed else 0

if __name__ == '__main__':
  sys.exit(main(sys.argv[1:]))
