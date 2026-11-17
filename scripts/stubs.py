"""
stubs.py - Generates template stub files for the "discord-stubs/" folder (This was AI-assisted).

Every run re-derives each stub from the source, then merges in what you wrote by hand in the old stub:
  - docstring text (the Args / Attributes sections are re-synced with the real signature / attributes)
  - types you filled in where the source has no annotation
  - imports that your hand-written types need

So signatures, bases, attributes, async-ness and decorators always follow the source, and stubs for deleted
modules are deleted.

Only things the root `discord/__init__.py` exports (plus the classes behind exported instances/aliases,
like CommandNamespace behind `command`, plus the mixins mixed into exported classes, like SignalMixin
behind `App` and `Bot`) are documented. Everything else is "light": stubbed so type checking works, but
with no docstring and no TODO. Add names to DOCUMENT_ALSO to opt an internal one in.

Mixin classes keep their class docstring and their other methods' docstrings, but their __init__ never
gets one (the class docstring already says what the mixin adds, e.g. a .loop attribute).

Usage:
  python stubs.py           write the stubs
  python stubs.py --diff    change nothing, show what a normal run would change
  python stubs.py --check   change nothing, exit 1 if stubs are out of date or still have TODOs (for CI)
"""

import re
import ast
import sys
import difflib
import argparse
import builtins
from pathlib import Path
from dataclasses import dataclass, field

ROOT = Path(__file__).resolve().parent.parent
PACKAGE = ROOT / 'discord'
STUBS_DIR = ROOT / 'discord-stubs'
MARKER = '# TODO'
TODO = re.compile(r'\bTODO\b')
SECTION = re.compile(r'^[A-Z][A-Za-z ]*:$')
ENTRY = re.compile(r'^(\s+)(\*{0,2}\w+)(?:\s*\([^)]*\))?\s*:')
IGNORED = {  # never stubbed
  '__repr__', '__str__', '__hash__', '__eq__', '__ne__', '__del__', '__post_init__',
  'lazy_filter'  # the root __init__.py is never filtered, so this one needs listing
}
DOCUMENT_ALSO = set()  # names (classes, functions) that are not exported by the root but should still get docstrings
MIXIN_SUFFIX = 'Mixin'  # classes with this name ending are documented when an exported class (indirectly) inherits them
KEPT_DECORATORS = {'property', 'staticmethod', 'classmethod', 'abstractmethod', 'overload'}
ENUM_BASES = {'Enum', 'IntEnum', 'StrEnum', 'Flag', 'IntFlag'}
BUILTINS = set(dir(builtins))
FALLBACK_IMPORTS = {'Any': 'from typing import Any'}  # for names a placeholder needs that the source never imports

@dataclass
class Member:
  kind: str  # function, class, variable, import
  name: str
  nodes: list  # ast nodes, several for overloads and property setters
  members: dict = field(default_factory = dict)
  imports: tuple = ()  # kind == import: (import line, extra assignment line or None)
  light: bool = False  # internal: stubbed without docstrings
  unpacked: bool = False  # variable assigned through tuple unpacking, its type can't be inferred

@dataclass
class Module:
  definitions: set = field(default_factory = set)  # every global name the module defines
  imports: dict = field(default_factory = dict)  # bound name -> (module it comes from, original name)
  stars: list = field(default_factory = list)  # modules it star imports
  refs: dict = field(default_factory = dict)  # name -> the name it was built from: x = Cls(), x = Cls, x = Cls.attr
  bases: dict = field(default_factory = dict)  # class name -> names of its base classes (Name or pkg.Name only)

# ----- reading the source

def is_dunder(name):
  return name.startswith('__') and name.endswith('__')

def is_public(name):
  return name not in IGNORED and (is_dunder(name) or not name.startswith('_'))

def statements(body):  # flattens if / try blocks
  for node in body:
    match node:
      case ast.If():
        yield from statements(node.body)
        yield from statements(node.orelse)
      case ast.Try():
        for block in (node.body, *(handler.body for handler in node.handlers), node.orelse, node.finalbody):
          yield from statements(block)
      case _:
        yield node

def target_names(target):
  match target:
    case ast.Name(id = name):
      yield name
    case ast.Tuple() | ast.List():
      for element in target.elts:
        yield from target_names(element)
    case ast.Starred(value = value):
      yield from target_names(value)

def self_attributes(target):  # self.a, and every self.x inside self.a, self.b = ...
  match target:
    case ast.Attribute(value = ast.Name(id = 'self'), attr = attr):
      yield attr
    case ast.Tuple() | ast.List():
      for element in target.elts:
        yield from self_attributes(element)
    case ast.Starred(value = value):
      yield from self_attributes(value)

def base_name(base):  # Name or pkg.Name -> Name, anything else (subscripts, calls) is ignored
  match base:
    case ast.Name(id = name) | ast.Attribute(attr = name):
      return name

def reexport(level, module, alias):
  line = f"from {'.' * level}{module or ''} import {alias.name}"
  name = alias.asname or alias.name
  if name == alias.name:
    return f'{line} as {name}', None  # "as" with the same name is what makes a stub re-export it
  return f'{line} as _{alias.name}', f'{name} = _{alias.name}'  # a renamed re-export has no direct form

def collect(body, reexports):
  members = {}

  def add(member):
    existing = members.get(member.name)
    if existing is None:
      members[member.name] = member
    elif existing.kind == member.kind == 'function':
      existing.nodes.extend(member.nodes)

  for node in statements(body):
    match node:
      case ast.FunctionDef() | ast.AsyncFunctionDef() if is_public(node.name):
        add(Member('function', node.name, [node]))
      case ast.ClassDef() if is_public(node.name):
        add(Member('class', node.name, [node], collect_class(node)))
      case ast.TypeAlias(name = ast.Name(id = name)) if is_public(name):
        add(Member('variable', name, [node]))
      case ast.Assign():
        for target in node.targets:
          for name in target_names(target):
            if is_public(name) and not is_dunder(name):
              add(Member('variable', name, [node], unpacked = isinstance(target, (ast.Tuple, ast.List))))
      case ast.AnnAssign(target = ast.Name(id = name)) if is_public(name) and not is_dunder(name):
        add(Member('variable', name, [node]))
      case ast.ImportFrom(level = level) if reexports and level:
        for alias in node.names:
          name = alias.asname or alias.name
          if name != '*' and is_public(name):
            add(Member('import', name, [node], imports = reexport(level, node.module, alias)))
  return members

def init_methods(node):  # __init__ plus every method of the class it calls through self.name(), transitively
  methods = {item.name: item for item in node.body if isinstance(item, (ast.FunctionDef, ast.AsyncFunctionDef))}
  found = {}
  queue = ['__init__']
  while queue:
    name = queue.pop(0)
    method = methods.get(name)
    if method is None or name in found:
      continue
    found[name] = method
    for sub in ast.walk(method):
      match sub:
        case ast.Call(func = ast.Attribute(value = ast.Name(id = 'self'), attr = attr)):
          queue.append(attr)
  return list(found.values())

def collect_class(node):
  members = collect(node.body, False)
  assigns = [
    sub for method in init_methods(node) for sub in ast.walk(method)
    if isinstance(sub, (ast.Assign, ast.AnnAssign))
  ]
  for sub in sorted(assigns, key = lambda sub: sub.lineno):
    for target in sub.targets if isinstance(sub, ast.Assign) else [sub.target]:
      unpacked = isinstance(target, (ast.Tuple, ast.List))
      for attr in self_attributes(target):
        if is_public(attr) and attr not in members:
          members[attr] = Member('variable', attr, [sub], unpacked = unpacked)
  return members

def import_map(tree):
  """bound name -> the import line that provides it, so placeholders can copy the imports their annotations need"""
  found = {}
  for node in statements(tree.body):
    match node:
      case ast.ImportFrom():
        for alias in node.names:
          if alias.name != '*':
            found[alias.asname or alias.name] = (
              f"from {'.' * node.level}{node.module or ''} import {alias.name}"
              + (f' as {alias.asname}' if alias.asname else '')
            )
      case ast.Import():
        for alias in node.names:
          found[alias.asname or alias.name.split('.')[0]] = f'import {alias.name}' + (f' as {alias.asname}' if alias.asname else '')
  return found

def parse_file(path):
  return ast.parse(path.read_text(encoding = 'utf-8'), filename = str(path))

# ----- what the root exports

def module_name(path):  # discord/core/command.py -> core.command, discord/core/__init__.py -> core, discord/__init__.py -> ''
  parts = list(path.relative_to(PACKAGE).with_suffix('').parts)
  if parts[-1] == '__init__':
    parts.pop()
  return '.'.join(parts)

def import_target(module, is_package, node):  # the dotted module a relative import points at
  parts = module.split('.') if module else []
  if not is_package and parts:
    parts.pop()
  if node.level > 1:
    parts = parts[:max(0, len(parts) - (node.level - 1))]
  if node.module:
    parts += node.module.split('.')
  return '.'.join(parts)

def index_module(name, is_package, tree):
  module = Module()
  for node in statements(tree.body):
    match node:
      case ast.ClassDef():
        module.definitions.add(node.name)
        module.bases[node.name] = [base for base in map(base_name, node.bases) if base]  # not "name", it's used below
      case ast.FunctionDef() | ast.AsyncFunctionDef():
        module.definitions.add(node.name)
      case ast.TypeAlias(name = ast.Name(id = alias)):
        module.definitions.add(alias)
      case ast.Assign():
        for target in node.targets:
          module.definitions.update(target_names(target))
        match node.value:  # x = Cls(), x = Cls, x = Cls.attr: remember what x was built from
          case ast.Call(func = ast.Name(id = ref)) | ast.Name(id = ref) | ast.Attribute(value = ast.Name(id = ref)):
            for target in node.targets:
              if isinstance(target, ast.Name):
                module.refs[target.id] = ref
      case ast.AnnAssign(target = ast.Name(id = variable)):
        module.definitions.add(variable)
      case ast.ImportFrom() if node.level:
        target = import_target(name, is_package, node)
        for alias in node.names:
          if alias.name == '*':
            module.stars.append(target)
          else:
            module.imports[alias.asname or alias.name] = (target, alias.name)
  return module

def resolve(modules, name, original, seen = ()):
  """follows a name back to the module that defines it, returns (module, name) or None"""
  module = modules.get(name)
  if module is None or (name, original) in seen:
    return None
  seen = (*seen, (name, original))
  if original in module.definitions:
    return name, original
  if original in module.imports:
    target, target_original = module.imports[original]
    return resolve(modules, target, target_original, seen)
  for target in module.stars:
    if found := resolve(modules, target, original, seen):
      return found
  return None

def imported_by(modules, module):
  """(defining module, name) for every name `module` imports"""
  found = set()
  for target, original in module.imports.values():
    if result := resolve(modules, target, original):
      found.add(result)
  for target in module.stars:
    source = modules.get(target)
    if source is None:
      continue
    for original in {*source.definitions, *source.imports}:
      if result := resolve(modules, target, original):
        found.add(result)
  return found

def imported_anywhere(modules):
  """so a constant that another module re-exports is not mistaken for an internal one"""
  found = set()
  for module in modules.values():
    found |= imported_by(modules, module)
  return found

def mixins_of(modules, found):
  """(defining module, name) for every mixin an exported class inherits, directly or through other classes.
  Classes in between (like AppBase, which App inherits) are walked through but not exported themselves."""
  mixins = set()
  visited = set()
  queue = list(found)
  while queue:
    item = queue.pop()
    if item in visited:
      continue
    visited.add(item)
    target, name = item
    for base in modules[target].bases.get(name, ()):
      result = resolve(modules, target, base)
      if result is None:
        continue
      if result[1].endswith(MIXIN_SUFFIX):
        mixins.add(result)
      queue.append(result)
  return mixins

def exported(modules):
  """(defining module, name) for everything the root __init__.py imports, plus the classes behind exported
  instances and aliases (command = command_namespace, command_namespace = CommandNamespace() exports CommandNamespace),
  plus the mixins mixed into exported classes (App -> AppBase -> SignalMixin -> RegistrarMixin)"""
  found = imported_by(modules, modules[''])
  queue = list(found)
  while queue:
    target, name = queue.pop()
    ref = modules[target].refs.get(name)
    if ref and ref[:1].isupper() and (result := resolve(modules, target, ref)) and result not in found:
      found.add(result)
      queue.append(result)
  found |= mixins_of(modules, found)
  return found

def set_light(member):
  member.light = True
  for inner in member.members.values():
    set_light(inner)

# ----- docstrings

def is_template(text):
  """True if the docstring is untouched generated filler"""
  for line in text.splitlines():
    stripped = line.strip()
    if stripped and not SECTION.match(line) and stripped != 'TODO' and not stripped.endswith(': TODO'):
      return False
  return True

def trim(lines):
  lines = list(lines)
  while lines and not lines[-1].strip():
    lines.pop()
  return lines

def entries_for(lines, names):
  """keeps the existing entry text for names that are still wanted, adds TODO entries for new ones"""
  entries = {}
  current = None
  indent = None
  for line in lines:
    match = ENTRY.match(line)
    if match and (indent is None or len(match[1]) == indent):
      indent = len(match[1])
      current = match[2]
      entries[current] = [line]
    elif current is not None:
      entries[current].append(line)
  default = ' ' * (indent or 2)
  out = []
  for name in names:
    out += trim(entries[name]) if name in entries else [f'{default}{name}: TODO']
  return out

def reconcile(text, wanted):
  """wanted: {section title: names that must be listed}. Rewrites those sections, keeps everything else."""
  preamble, sections = [], []
  for line in text.splitlines():
    if SECTION.match(line):
      sections.append([line[:-1], []])
    elif sections:
      sections[-1][1].append(line)
    else:
      preamble.append(line)
  seen = set()
  kept = []
  for title, lines in sections:
    if title in wanted:
      seen.add(title)
      if wanted[title]:
        kept.append((title, entries_for(lines, wanted[title])))
    else:
      kept.append((title, trim(lines)))
  for title, names in reversed(list(wanted.items())):
    if title not in seen and names:
      kept.insert(0, (title, [f'  {name}: TODO' for name in names]))
  result = trim(preamble)
  for title, lines in kept:
    result += ([''] if result else []) + [f'{title}:', *lines]
  return '\n'.join(result)

def new_doc(sections):
  lines = ['TODO']
  for title, entries in sections:
    lines += ['', f'{title}:', *entries]
  return '\n'.join(lines)

def doc_block(text, indent):
  text = text.replace('\\', '\\\\').replace('"""', '\\"\\"\\"')
  return [f'{indent}"""', *[(indent + line) if line else '' for line in text.splitlines()], f'{indent}"""']

# ----- generating stubs

def old_docstring(node):
  return ast.get_docstring(node) if node is not None else None

def header_marked(node, lines):  # did the old stub's def line carry a "# TODO"?
  end = max(node.body[0].lineno - 1, node.lineno)
  return any(MARKER in line for line in lines[node.lineno - 1:end])

def generics(node):
  return f"[{', '.join(map(ast.unparse, node.type_params))}]" if node.type_params else ''

def decorator_text(decorator):
  match decorator:
    case ast.Name(id = 'cached_property') | ast.Attribute(attr = 'cached_property'):
      return 'property'
    case ast.Name(id = name) if name in KEPT_DECORATORS:
      return name
    case ast.Attribute(attr = 'setter' | 'deleter'):
      return ast.unparse(decorator)

def all_args(args):
  return [*args.posonlyargs, *args.args, *([args.vararg] if args.vararg else []), *args.kwonlyargs, *([args.kwarg] if args.kwarg else [])]

def param_names(args):  # what the Args section lists
  names = [arg.arg for arg in (*args.posonlyargs, *args.args) if arg.arg not in ('self', 'cls')]
  if args.vararg:
    names.append('*' + args.vararg.arg)
  names += [arg.arg for arg in args.kwonlyargs]
  if args.kwarg:
    names.append('**' + args.kwarg.arg)
  return names

def format_args(args, old_annotations):
  """like ast.unparse, but defaults become " = ..." and missing annotations come from the old stub.
  Returns (text, whether a parameter is still unannotated)."""
  missing = False

  def one(arg, has_default, prefix = ''):
    nonlocal missing
    annotation = ast.unparse(arg.annotation) if arg.annotation else old_annotations.get(arg.arg)
    if annotation is None and arg.arg not in ('self', 'cls'):
      missing = True
    text = prefix + arg.arg + (f': {annotation}' if annotation else '')
    return text + ' = ...' if has_default else text

  positional = [*args.posonlyargs, *args.args]
  first_default = len(positional) - len(args.defaults)
  parts = [one(arg, index >= first_default) for index, arg in enumerate(positional)]
  if args.posonlyargs:
    parts.insert(len(args.posonlyargs), '/')
  if args.vararg:
    parts.append(one(args.vararg, False, '*'))
  elif args.kwonlyargs:
    parts.append('*')
  parts += [one(arg, default is not None) for arg, default in zip(args.kwonlyargs, args.kw_defaults, strict = True)]
  if args.kwarg:
    parts.append(one(args.kwarg, False, '**'))
  return ', '.join(parts), missing

def stub_function(node, indent, light, old, old_lines, no_doc = False):
  """no_doc: never write a docstring (used for the __init__ of a mixin class)"""
  old_annotations, old_returns, old_marked, old_doc = {}, None, False, None
  if old is not None:
    old_annotations = {arg.arg: ast.unparse(arg.annotation) for arg in all_args(old.args) if arg.annotation}
    old_returns = ast.unparse(old.returns) if old.returns else None
    old_marked = header_marked(old, old_lines)
    old_doc = old_docstring(old)

  decorators = [text for text in map(decorator_text, node.decorator_list) if text]
  bare = any(text.endswith(('.setter', '.deleter')) or text == 'overload' for text in decorators)
  args, missing = format_args(node.args, old_annotations)

  placeholder = False
  if node.returns is not None:
    returns = ast.unparse(node.returns)
  elif old_returns is not None and not (old_returns == 'Any' and old_marked):
    returns = old_returns  # filled in by hand
  elif node.name == '__init__' or bare:
    returns = 'None'
  else:
    returns, placeholder = 'Any', True  # never leave it out, a missing return is Unknown to a type checker

  doc = None
  if no_doc:
    pass  # a mixin's __init__ has no docstring, the class docstring covers it
  elif not light and not bare:
    names = param_names(node.args)
    if old_doc is not None:
      doc = reconcile(old_doc, {'Args': names})
    else:
      sections = [('Args', [f'  {name}: TODO' for name in names])] if names else []
      if returns != 'None' and 'property' not in decorators:
        sections.append(('Returns', ['  TODO']))
      doc = new_doc(sections)
  elif old_doc is not None and not bare and not is_template(old_doc):
    doc = old_doc  # a real docstring on an internal name is kept as is

  prefix = 'async def' if isinstance(node, ast.AsyncFunctionDef) else 'def'
  header = f'{indent}{prefix} {node.name}{generics(node)}({args}) -> {returns}:'
  todo = f' {MARKER}' if (missing or placeholder) and not light else ''
  lines = [f'{indent}@{text}' for text in decorators]
  if doc is None:
    return [*lines, f'{header} ...{todo}']
  return [*lines, header + todo, *doc_block(doc, indent + '  ')]

def infer(member):
  """('annotation' | 'alias', text) from the assigned value, or None"""
  node = member.nodes[0]
  if member.unpacked:
    return None
  value = getattr(node, 'value', None)
  targets = node.targets if isinstance(node, ast.Assign) else [node.target]
  plain_name = len(targets) == 1 and isinstance(targets[0], ast.Name)
  match value:
    case ast.Call(func = ast.Name(id = 'cast') | ast.Attribute(attr = 'cast'), args = [kind, _]):  # cast(T, x) is typed T
      return 'annotation', ast.unparse(kind)
    case ast.Call(func = ast.Name(id = cls)) if cls[:1].isupper() and cls not in BUILTINS:  # x = Cls(...) is typed Cls
      return 'annotation', cls
    case ast.Name() | ast.Attribute() if plain_name:  # an alias like colour = Color
      return 'alias', ast.unparse(value)
    case ast.Constant(value = int() | float() | str() | bytes() as constant):
      return 'annotation', type(constant).__name__
  return None

def stub_variable(member, indent, old, old_lines):
  node = member.nodes[0]
  if isinstance(node, ast.TypeAlias):
    return [indent + ast.unparse(node)]
  annotation = getattr(node, 'annotation', None)
  if annotation is not None:
    return [f'{indent}{member.name}: {ast.unparse(annotation)}']
  if old is not None and old.kind == 'variable':  # a type filled in by hand survives, a TODO Any does not
    old_node = old.nodes[0]
    old_annotation = getattr(old_node, 'annotation', None)
    if old_annotation is not None:
      text = ast.unparse(old_annotation)
      if not (text == 'Any' and MARKER in old_lines[old_node.lineno - 1]):
        return [f'{indent}{member.name}: {text}']
  match infer(member):
    case ('annotation', text):
      return [f'{indent}{member.name}: {text}']
    case ('alias', text):
      return [f'{indent}{member.name} = {text}']
  return [f'{indent}{member.name}: Any {MARKER}']  # always marked, an Any hides gaps from type checkers

def is_enum(node):
  return any(ast.unparse(base).split('.')[-1] in ENUM_BASES for base in node.bases)

def is_mixin(node):
  return node.name.endswith(MIXIN_SUFFIX)

def stub_class(member, indent, old, old_lines):
  node = member.nodes[0]
  enum = is_enum(node)
  mixin = is_mixin(node)
  old = old if old is not None and old.kind == 'class' else None
  old_members = old.members if old else {}
  bases = [ast.unparse(base) for base in node.bases]
  bases += [f'{k.arg}={ast.unparse(k.value)}' if k.arg else f'**{ast.unparse(k.value)}' for k in node.keywords]

  blocks = []
  ordered = sorted(member.members.items(), key = lambda item: item[1].kind != 'variable')  # attributes first
  for name, inner in ordered:
    if enum and inner.kind == 'variable':
      blocks.append([f'{indent}  {name} = ...'])
    else:
      blocks.append(generate(inner, indent + '  ', old_members.get(name), old_lines, in_mixin = mixin))

  old_doc = old_docstring(old.nodes[0]) if old else None
  attributes = [] if enum else [name for name, inner in member.members.items() if inner.kind == 'variable']
  if member.light:
    doc = old_doc if old_doc is not None and not is_template(old_doc) else None
  elif old_doc is not None:
    doc = reconcile(old_doc, {'Attributes': attributes})
  else:
    doc = new_doc([('Attributes', [f'  {name}: TODO' for name in attributes])] if attributes else [])

  header = f'{indent}class {node.name}{generics(node)}' + (f"({', '.join(bases)})" if bases else '') + ':'
  if doc is None:
    return [header, *join_blocks(blocks, False)] if blocks else [header + ' ...']
  return [header, *doc_block(doc, indent + '  '), *join_blocks(blocks, True)]

def generate(member, indent, old, old_lines, in_mixin = False):
  match member.kind:
    case 'function':
      olds = old.nodes if old is not None and old.kind == 'function' else []
      no_doc = in_mixin and member.name == '__init__'  # mixins keep the class docstring, but not one on __init__
      lines = []
      for index, node in enumerate(member.nodes):
        lines += stub_function(node, indent, member.light, olds[index] if index < len(olds) else None, old_lines, no_doc)
      return lines
    case 'class':
      return stub_class(member, indent, old, old_lines)
    case 'import':
      return [indent + member.imports[0]]
  return stub_variable(member, indent, old, old_lines)

def is_definition(block):
  return block[0].lstrip().startswith(('class ', 'def ', 'async def ', 'type ', '@'))

def is_import(block):
  return block[0].lstrip().startswith(('from ', 'import '))

def join_blocks(blocks, after_content):
  out = []
  previous = None
  for block in blocks:
    if (out or after_content) and (previous is None or is_definition(block) or is_definition(previous) or is_import(block) != is_import(previous)):
      out.append('')
    out.extend(block)
    previous = block
  return out

def bound_names(tree):
  names = set()
  for node in tree.body:
    match node:
      case ast.ClassDef() | ast.FunctionDef() | ast.AsyncFunctionDef():
        names.add(node.name)
      case ast.TypeAlias(name = ast.Name(id = name)) | ast.AnnAssign(target = ast.Name(id = name)):
        names.add(name)
      case ast.Assign():
        names.update(name for target in node.targets for name in target_names(target))
      case ast.Import() | ast.ImportFrom():
        names.update(alias.asname or alias.name.split('.')[0] for alias in node.names)
  for node in ast.walk(tree):
    names.update(param.name for param in getattr(node, 'type_params', None) or ())
  return names

def render(members, source_tree, old_text):
  """returns (stub text, names that need an import by hand)"""
  old_tree, old_lines = None, []
  if old_text is not None:
    try:
      old_tree, old_lines = ast.parse(old_text), old_text.splitlines()
    except SyntaxError:
      pass  # an unreadable old stub is just overwritten
  old_members = collect(old_tree.body, False) if old_tree else {}

  blocks, extras = [], []
  for name, member in members.items():
    if member.kind == 'import':
      blocks.append([member.imports[0]])
      if member.imports[1]:
        extras.append(member.imports[1])
    else:
      blocks.append(generate(member, '', old_members.get(name), old_lines))
  body = join_blocks(blocks, False)
  if extras:
    body += ['', *extras]

  # imports the body needs: the source's own import wins, then one you added to the old stub, then a fallback
  tree = ast.parse('\n'.join(body))
  used = {node.id for node in ast.walk(tree) if isinstance(node, ast.Name) and isinstance(node.ctx, ast.Load)}
  from_source = import_map(source_tree)
  from_old = import_map(old_tree) if old_tree else {}
  lines, unresolved = set(), []
  for name in sorted(used - bound_names(tree) - BUILTINS):
    line = from_source.get(name) or from_old.get(name) or FALLBACK_IMPORTS.get(name)
    if line:
      lines.add(line)
    else:
      unresolved.append(name)
  imports = sorted(lines, key = lambda line: (line.startswith('from .'), line.startswith('from '), len(line), line))
  out = [*imports, '', *body] if imports and body else [*imports, *body]
  return '\n'.join(out) + '\n', unresolved

# ----- main

def main():
  parser = argparse.ArgumentParser(description = 'Keep the discord-stubs/ folder in sync with the discord/ package.')
  parser.add_argument('--check', action = 'store_true', help = 'change nothing, exit 1 if stubs are out of date or have TODOs left')
  parser.add_argument('--diff', action = 'store_true', help = 'change nothing, show what a normal run would change')
  options = parser.parse_args()

  def rel(path):
    return path.relative_to(ROOT).as_posix()

  files = sorted(
    path for path in PACKAGE.rglob('*.py')
    if not any(part == '__pycache__' or part.startswith('.') for part in path.relative_to(PACKAGE).parts)
  )
  if not files:
    print(f'no .py files found in {PACKAGE}')
    return 1

  modules, trees, failed = {}, {}, False
  for path in files:
    try:
      trees[path] = parse_file(path)
    except SyntaxError as error:
      print(f'{rel(path)}:{error.lineno}: could not parse source: {error.msg}')
      failed = True
      continue
    modules[module_name(path)] = index_module(module_name(path), path.name == '__init__.py', trees[path])
  if '' not in modules:
    print(f'could not read {rel(PACKAGE / "__init__.py")}, nothing to export from')
    return 1
  exports = exported(modules)
  shared = imported_anywhere(modules)

  wanted = {}  # stub path -> new text
  notes = []
  for path in trees:
    name = module_name(path)
    members = collect(trees[path].body, path.name == '__init__.py')
    if name:  # the root __init__.py defines what is exported, everything else is internal unless the root exports it
      for member_name, member in list(members.items()):
        if member.kind == 'import' or (name, member_name) in exports or member_name in DOCUMENT_ALSO:
          continue
        is_alias = isinstance(member.nodes[0], ast.TypeAlias)  # signatures can use these, so they stay
        if member.kind == 'variable' and (name, member_name) not in shared and not is_alias:
          del members[member_name]  # an internal constant nothing else imports, never stubbed
        else:
          set_light(member)
    if not members:
      continue
    stub_path = STUBS_DIR / path.relative_to(PACKAGE).with_suffix('.pyi')
    old_text = stub_path.read_text(encoding = 'utf-8') if stub_path.exists() else None
    text, unresolved = render(members, trees[path], old_text)
    wanted[stub_path] = text
    notes += [f'{rel(stub_path)}: needs an import for {n!r} but the source has none, add one by hand' for n in unresolved]

  changes = []  # (stub path, old text or None, new text or None for delete)
  for stub_path, text in wanted.items():
    old_text = stub_path.read_text(encoding = 'utf-8') if stub_path.exists() else None
    if old_text != text:
      changes.append((stub_path, old_text, text))
  for stub_path in sorted(STUBS_DIR.rglob('*.pyi')):
    if stub_path not in wanted:  # its source module is gone
      changes.append((stub_path, stub_path.read_text(encoding = 'utf-8'), None))

  for stub_path, old_text, text in changes:
    verb = 'delete' if text is None else 'create' if old_text is None else 'update'
    if options.diff:
      diff = difflib.unified_diff(
        (old_text or '').splitlines(), (text or '').splitlines(),
        fromfile = f'a/{rel(stub_path)}', tofile = f'b/{rel(stub_path)}', lineterm = ''
      )
      print('\n'.join(diff) or f'{verb} {rel(stub_path)}')
    elif options.check:
      print(f'{rel(stub_path)}: out of date (would {verb})')
    elif text is None:
      stub_path.unlink()
      print(f'{rel(stub_path)}: deleted, its source module no longer exists')
    else:
      stub_path.parent.mkdir(parents = True, exist_ok = True)
      stub_path.write_text(text, encoding = 'utf-8', newline = '\n')
      print(f'{rel(stub_path)}: {verb}d')

  unfinished = 0
  if not options.diff:
    for stub_path, text in wanted.items():
      marked = [number for number, line in enumerate(text.splitlines(), 1) if TODO.search(line)]
      if marked:
        unfinished += 1
        print(f'{rel(stub_path)}:{marked[0]}: {len(marked)} placeholder(s) left to fill in (search for "TODO")')
    for note in notes:
      print(note)
    if not (changes or unfinished or notes or failed):
      print('all stubs are up to date')
  if options.check:
    return int(bool(changes or unfinished or notes or failed))
  return int(failed)

if __name__ == '__main__':
  sys.exit(main())
