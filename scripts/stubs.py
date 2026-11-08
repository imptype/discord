"""
stubs.py - Generates template stub files for the "discord-stubs/" folder (This was AI-assisted).

Usage:
  python stubs.py           create missing stubs, add missing names, remove stale ones
  python stubs.py --diff    change nothing, show what a normal run would change
  python stubs.py --check   change nothing, exit 1 if the stubs are out of date or unfinished (for CI)
"""

import re
import ast
import sys
import copy
import difflib
import argparse
import builtins
from pathlib import Path
from dataclasses import dataclass, field

PACKAGE = Path('discord')
STUBS_DIR = Path('discord-stubs')
MARKER = '# TODO'
IGNORED = { # never stubbed, edit to taste (internal module level constants are skipped automatically, see main)
  '__repr__', '__str__', '__hash__', '__eq__', '__ne__', '__del__', '__post_init__',
  'lazy_filter' # the root __init__.py is never filtered, so this one needs listing
}
KEPT_DECORATORS = {'property', 'staticmethod', 'classmethod', 'abstractmethod', 'overload'}
ENUM_BASES = {'Enum', 'IntEnum', 'StrEnum', 'Flag', 'IntFlag'}
EXPOSED_BASES = set() # extra base class names to treat as public, besides anything ending in Mixin (e.g. {'AppBase'})
TODO = re.compile(r'\bTODO\b')
BUILTINS = set(dir(builtins))
FALLBACK_IMPORTS = { # for names a placeholder needs that the source never imports
  'Any': 'from typing import Any'
}

@dataclass
class Member:
  kind: str # function, class, variable, import
  line: int
  node: ast.AST
  signature: tuple | None = None
  is_async: bool = False
  count: int = 1 # definitions sharing the name (overloads, property setters)
  import_lines: tuple = ()
  members: dict = field(default_factory = dict)
  light: bool = False # internal name, stubbed without docstrings (Any attributes are still marked with a TODO)

@dataclass
class Action:
  kind: str # add or remove
  name: str
  member: Member
  container: Member | None # the stub class it belongs to, None for module level

@dataclass
class Issue:
  line: int
  text: str
  on_stub: bool = False
  action: Action | None = None

@dataclass
class Module:
  is_package: bool
  definitions: set = field(default_factory = set) # every global name the module defines
  imports: dict = field(default_factory = dict) # bound name -> (module it comes from, original name)
  stars: list = field(default_factory = list) # modules it star imports
  refs: dict = field(default_factory = dict) # name -> the name it was built from, for x = Cls(), x = Cls, x = Cls.attr
  bases: dict = field(default_factory = dict) # class name -> names of its base classes

# ----- reading source and stubs

def is_dunder(name):
  return name.startswith('__') and name.endswith('__')

def is_public(name):
  return name not in IGNORED and (is_dunder(name) or not name.startswith('_'))

def statements(body): # flattens if / try blocks
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

def signature_of(args):
  positional = tuple(a.arg for a in (*args.posonlyargs, *args.args))
  kwonly = tuple(a.arg for a in args.kwonlyargs)
  return positional, args.vararg and args.vararg.arg, kwonly, args.kwarg and args.kwarg.arg

def param_names(signature): # what the Args section lists
  positional, vararg, kwonly, kwarg = signature
  return [*(name for name in positional if name not in ('self', 'cls')), *(['*' + vararg] if vararg else []), *kwonly, *(['**' + kwarg] if kwarg else [])]

def format_signature(signature):
  positional, vararg, kwonly, kwarg = signature
  parts = [*positional, *(['*' + vararg] if vararg else ['*'] if kwonly else []), *kwonly, *(['**' + kwarg] if kwarg else [])]
  return '(' + ', '.join(parts) + ')'

def target_names(target):
  match target:
    case ast.Name(id = name):
      yield name
    case ast.Tuple() | ast.List():
      for element in target.elts:
        yield from target_names(element)
    case ast.Starred(value = value):
      yield from target_names(value)

def self_attribute(target):
  match target:
    case ast.Attribute(value = ast.Name(id = 'self'), attr = attr):
      return attr

def base_name(base): # Name or pkg.Name -> Name, anything else (subscripts, calls) is ignored
  match base:
    case ast.Name(id = name) | ast.Attribute(attr = name):
      return name

def reexport(level, module, alias):
  line = f"from {'.' * level}{module or ''} import {alias.name}"
  name = alias.asname or alias.name
  if name == alias.name:
    return (f'{line} as {name}',) # "as" with the same name is what makes a stub re-export it
  return (f'{line} as _{alias.name}', f'{name} = _{alias.name}') # a renamed re-export has no direct form

def collect(body, imports, members):
  def add(name, member):
    existing = members.get(name)
    if existing is None:
      members[name] = member
    elif existing.kind == member.kind == 'function':
      existing.count += 1

  for node in statements(body):
    match node:
      case ast.FunctionDef() | ast.AsyncFunctionDef() if is_public(node.name):
        add(node.name, Member('function', node.lineno, node, signature_of(node.args), isinstance(node, ast.AsyncFunctionDef)))
      case ast.ClassDef() if is_public(node.name):
        add(node.name, Member('class', node.lineno, node, members = collect_class(node)))
      case ast.TypeAlias(name = ast.Name(id = name)) if is_public(name):
        add(name, Member('variable', node.lineno, node))
      case ast.Assign():
        for name in (name for target in node.targets for name in target_names(target)):
          if is_public(name) and not is_dunder(name):
            add(name, Member('variable', node.lineno, node))
      case ast.AnnAssign(target = ast.Name(id = name)) if is_public(name) and not is_dunder(name):
        add(name, Member('variable', node.lineno, node))
      case ast.ImportFrom(level = level) if imports and level:
        for alias in node.names:
          name = alias.asname or alias.name
          if name != '*' and is_public(name):
            add(name, Member('import', node.lineno, node, import_lines = reexport(level, node.module, alias)))
  return members

def init_methods(node): # __init__ plus every method of the class it calls through self.name(), transitively
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
  members = collect(node.body, False, {})
  assigns = [
    sub for method in init_methods(node) for sub in ast.walk(method)
    if isinstance(sub, (ast.Assign, ast.AnnAssign))
  ]
  for sub in sorted(assigns, key = lambda sub: sub.lineno):
    for target in sub.targets if isinstance(sub, ast.Assign) else [sub.target]:
      attr = self_attribute(target)
      if attr and is_public(attr) and attr not in members:
        members[attr] = Member('variable', sub.lineno, sub)
  return members

def attribute_names(members):
  return [name for name, member in members.items() if member.kind == 'variable']

def flatten(members, scope = ''):
  for name, member in members.items():
    yield f'{scope}{name}'
    yield from flatten(member.members, f'{scope}{name}.')

def parse(path):
  text = path.read_text(encoding = 'utf-8')
  return text.splitlines(), ast.parse(text, filename = str(path))

def source_import_map(tree):
  """bound name -> the import line that provides it, so placeholders can copy the imports their annotations need"""
  found = {}
  for node in statements(tree.body):
    match node:
      case ast.ImportFrom():
        for alias in node.names:
          if alias.name != '*':
            found[alias.asname or alias.name] = f"from {'.' * node.level}{node.module or ''} import {alias.name}" + (f' as {alias.asname}' if alias.asname else '')
      case ast.Import():
        for alias in node.names:
          found[alias.asname or alias.name.split('.')[0]] = f'import {alias.name}' + (f' as {alias.asname}' if alias.asname else '')
  return found

def bound_names(tree):
  names = set()
  for node in ast.walk(tree):
    match node:
      case ast.Import() | ast.ImportFrom():
        names.update(alias.asname or alias.name.split('.')[0] for alias in node.names)
      case ast.ClassDef() | ast.FunctionDef() | ast.AsyncFunctionDef():
        names.add(node.name)
      case ast.Assign():
        names.update(name for target in node.targets for name in target_names(target))
      case ast.AnnAssign(target = ast.Name(id = name)):
        names.add(name)
  return names

# ----- what the root exports

def module_name(path): # discord/core/commands.py -> core.commands, discord/core/__init__.py -> core, discord/__init__.py -> ''
  parts = list(path.relative_to(PACKAGE).with_suffix('').parts)
  if parts[-1] == '__init__':
    parts.pop()
  return '.'.join(parts)

def import_target(module, is_package, node): # the dotted module a relative import points at
  parts = module.split('.') if module else []
  if not is_package and parts:
    parts.pop()
  if node.level > 1:
    parts = parts[:max(0, len(parts) - (node.level - 1))]
  if node.module:
    parts += node.module.split('.')
  return '.'.join(parts)

def index_module(name, is_package, tree):
  module = Module(is_package)
  for node in statements(tree.body):
    match node:
      case ast.FunctionDef() | ast.AsyncFunctionDef() | ast.ClassDef():
        module.definitions.add(node.name)
        if isinstance(node, ast.ClassDef):
          module.bases[node.name] = [found for base in node.bases if (found := base_name(base))]
      case ast.TypeAlias(name = ast.Name(id = alias)):
        module.definitions.add(alias)
      case ast.Assign():
        for target in node.targets:
          module.definitions.update(target_names(target))
        match node.value: # x = Cls(), x = Cls, x = Cls.attr: remember what x was built from
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

def index_package(files):
  modules = {}
  parsed = {} # path -> its tree, or the SyntaxError it raised (reported when the file itself is checked)
  for path in files:
    try:
      _, tree = parse(path)
    except SyntaxError as error:
      parsed[path] = error
      continue
    parsed[path] = tree
    name = module_name(path)
    modules[name] = index_module(name, path.name == '__init__.py', tree)
  return modules, parsed

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

def set_light(member):
  member.light = True
  for inner in member.members.values():
    set_light(inner)

def imported_anywhere(modules):
  """(defining module, name) for everything any module in the package imports, so a constant that another
  module or a package __init__.py re-exports is not mistaken for an internal one"""
  found = set()
  for module in modules.values():
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

def is_exposed_base(name):
  return name.endswith('Mixin') or name in EXPOSED_BASES

def exported(modules):
  """(defining module, name) for everything the root __init__.py imports, plus the classes behind exported
  instances and aliases, plus the mixins (see is_exposed_base) anywhere up the base chain of an exported class.
  Other base classes, like API or Handler, are walked through but stay internal."""
  root = modules['']
  found = set()
  for target, original in root.imports.values():
    if result := resolve(modules, target, original):
      found.add(result)
  for target in root.stars:
    source = modules.get(target)
    if source is None:
      continue
    for original in {*source.definitions, *source.imports}:
      if result := resolve(modules, target, original):
        found.add(result)

  # command = command_namespace, command_namespace = CommandNamespace() exports CommandNamespace too
  queue = list(found)
  seen = set(found)
  while queue:
    target, name = queue.pop()
    ref = modules[target].refs.get(name)
    if ref and ref[:1].isupper() and (result := resolve(modules, target, ref)) and result not in seen:
      found.add(result)
      seen.add(result)
      queue.append(result)

    # class Bot(AppBase), class AppBase(CommandMixin, ...): every ancestor is walked, only mixins are exported
    for base in modules[target].bases.get(name, []):
      result = resolve(modules, target, base)
      if result is None or result in seen:
        continue
      seen.add(result)
      if is_exposed_base(result[1]):
        found.add(result)
      queue.append(result)
  return found

# ----- generating placeholders

def names_in(*nodes):
  return {n.id for node in nodes if node is not None for n in ast.walk(node) if isinstance(n, ast.Name)}

def type_param_names(node):
  return {p.name for p in getattr(node, 'type_params', ())}

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

def is_complete(node):
  args = node.args
  params = [*args.posonlyargs, *args.args, *args.kwonlyargs, args.vararg, args.kwarg]
  annotated = all(p.annotation for p in params if p and p.arg not in ('self', 'cls'))
  return annotated and (node.returns is not None or node.name == '__init__')

def doc_lines(indent, sections):
  lines = [f'{indent}"""', f'{indent}TODO']
  for title, entries in sections:
    lines += ['', f'{indent}{title}:', *[f'{indent}  {entry}' for entry in entries]]
  return [*lines, f'{indent}"""']

def is_enum(node):
  return any(ast.unparse(base).split('.')[-1] in ENUM_BASES for base in node.bases)

def format_args(args): # like ast.unparse, but with spaces around the = of defaults
  def one(arg, has_default, prefix = ''):
    text = prefix + arg.arg + (f': {ast.unparse(arg.annotation)}' if arg.annotation else '')
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
  return ', '.join(parts)

def stub_function(node, indent, used, light = False):
  lines = [f'{indent}@{text}' for text in map(decorator_text, node.decorator_list) if text]
  args = copy.deepcopy(node.args)
  args.defaults = [ast.Constant(value = ...) for _ in args.defaults]
  args.kw_defaults = [None if d is None else ast.Constant(value = ...) for d in args.kw_defaults]
  returns = node.returns
  if returns is None: # never leave it out, a missing return is Unknown to a type checker and hides the gap
    is_setter = any(text and text.endswith(('.setter', '.deleter')) for text in map(decorator_text, node.decorator_list))
    returns = ast.Constant(value = None) if node.name == '__init__' or is_setter else ast.Name(id = 'Any')
  used.update(names_in(args, returns, *node.type_params) - type_param_names(node))
  prefix = 'async def' if isinstance(node, ast.AsyncFunctionDef) else 'def'
  arrow = f' -> {ast.unparse(returns)}'
  todo = '' if light or is_complete(node) else f' {MARKER}'
  header = f'{indent}{prefix} {node.name}{generics(node)}({format_args(args)}){arrow}:'
  decorators = [decorator_text(d) for d in node.decorator_list]
  if light or any(text and text.endswith(('.setter', '.deleter')) for text in decorators):
    return [*lines, f'{header} ...{todo}'] # nothing to describe
  sections = []
  if names := param_names(signature_of(node.args)):
    sections.append(('Args', [f'{name}: TODO' for name in names]))
  is_none = isinstance(returns, ast.Constant) and returns.value is None
  if not is_none and 'property' not in decorators:
    sections.append(('Returns', ['TODO']))
  return [*lines, header + todo, *doc_lines(indent + '  ', sections)]

def stub_variable(name, node, indent, used, light = False):
  if isinstance(node, ast.TypeAlias):
    used.update(names_in(node.value, *node.type_params) - type_param_names(node))
    return [indent + ast.unparse(node)]
  annotation = getattr(node, 'annotation', None)
  if annotation is not None:
    used.update(names_in(annotation))
    return [f'{indent}{name}: {ast.unparse(annotation)}']
  value = getattr(node, 'value', None)
  match value:
    case ast.Call(func = ast.Name(id = 'cast') | ast.Attribute(attr = 'cast'), args = [kind, _]): # cast(T, x) is typed T
      used.update(names_in(kind))
      return [f'{indent}{name}: {ast.unparse(kind)}']
    case ast.Call(func = ast.Name(id = cls)) if cls[:1].isupper() and cls not in BUILTINS: # x = Cls(...) is typed Cls
      used.add(cls)
      return [f'{indent}{name}: {cls}']
  target = node.targets[0] if isinstance(node, ast.Assign) else node.target
  match value if isinstance(target, ast.Name) else None: # not self.x = ...
    case ast.Name() | ast.Attribute() as value: # an alias like colour = Color
      used.update(names_in(value))
      return [f'{indent}{name} = {ast.unparse(value)}']
    case ast.Constant(value = int() | float() | str() | bytes() as constant):
      return [f'{indent}{name}: {type(constant).__name__}']
  used.add('Any')
  return [f'{indent}{name}: Any {MARKER}'] # always marked, even in light classes, an Any hides gaps from type checkers

def stub_class(node, members, indent, used, light = False):
  bases = [ast.unparse(base) for base in node.bases]
  bases += [f'{k.arg}={ast.unparse(k.value)}' if k.arg else f'**{ast.unparse(k.value)}' for k in node.keywords]
  enum = is_enum(node)
  inner = names_in(*node.bases, *(k.value for k in node.keywords), *node.type_params)
  blocks = []
  for name, member in members.items():
    if enum and member.kind == 'variable':
      blocks.append([f'{indent}  {name} = ...'])
    else:
      blocks.append(generate(name, member, indent + '  ', inner))
  used.update(inner - type_param_names(node))
  header = f'{indent}class {node.name}{generics(node)}' + (f"({', '.join(bases)})" if bases else '') + ':'
  if light: # an internal class has no docstring
    return [header, *join_blocks(blocks, False)] if blocks else [header + ' ...']
  attributes = [] if enum else attribute_names(members)
  sections = [('Attributes', [f'{name}: TODO' for name in attributes])] if attributes else []
  return [header, *doc_lines(indent + '  ', sections), *join_blocks(blocks, True)]

def generate(name, member, indent, used):
  match member.kind:
    case 'function':
      return stub_function(member.node, indent, used, member.light)
    case 'class':
      return stub_class(member.node, member.members, indent, used, member.light)
    case 'import':
      return [indent + line for line in member.import_lines]
  return stub_variable(name, member.node, indent, used, member.light)

# ----- applying actions to a stub

def is_placeholder(statement):
  return isinstance(statement, ast.Pass) or (isinstance(statement, ast.Expr) and isinstance(statement.value, ast.Constant) and statement.value.value is ...)

def is_inline_placeholder(node, lines): # class A: ...
  first = node.body[0]
  return len(node.body) == 1 and is_placeholder(first) and lines[first.lineno - 1][:first.col_offset].rstrip().endswith(':')

def class_indent(node, lines):
  return ' ' * (node.col_offset + 2 if is_inline_placeholder(node, lines) else node.body[0].col_offset)

def import_position(tree): # after the docstring and __future__ imports
  position = 0
  for index, node in enumerate(tree.body):
    if index == 0 and isinstance(node, ast.Expr) and isinstance(node.value, ast.Constant) and isinstance(node.value.value, str):
      position = node.end_lineno
    elif isinstance(node, ast.ImportFrom) and node.module == '__future__':
      position = node.end_lineno
    else:
      break
  return position

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

def apply_actions(lines, tree, source_tree, source, actions):
  """returns (new lines, names that still need an import by hand)"""
  while lines and not lines[-1].strip():
    lines.pop()
  ops = [] # (position, depth, kind, payload), applied from the bottom up so earlier line numbers stay valid
  used = set()
  module_blocks = []
  class_blocks = {} # id(stub class) -> (stub class, indent, new blocks)
  for action in actions:
    if action.kind == 'remove':
      node = action.member.node
      start = min([d.lineno for d in getattr(node, 'decorator_list', [])] + [node.lineno])
      ops.append((start, 0, 'delete', (start, node.end_lineno)))
    elif action.container is None:
      module_blocks.append(generate(action.name, action.member, '', used))
    else:
      container = action.container
      indent = class_indent(container.node, lines)
      entry = class_blocks.setdefault(id(container), (container, indent, []))
      entry[2].append(generate(action.name, action.member, indent, used))

  # depth breaks ties at the same position: outer blocks go in first so inner blocks end up above them
  if module_blocks:
    new = join_blocks(module_blocks, bool(lines))
    ops.append((len(lines) + 0.5, 0, 'insert', (len(lines), new)))
  for container, indent, blocks in class_blocks.values():
    node = container.node
    first = node.body[0]
    depth = len(indent)
    only_placeholder = len(node.body) == 1 and is_placeholder(first)
    new = join_blocks(blocks, not only_placeholder)
    if only_placeholder:
      if is_inline_placeholder(node, lines):
        header = lines[first.lineno - 1][:first.col_offset].rstrip()
        ops.append((first.lineno, 0, 'replace', (first.lineno, header)))
        ops.append((first.lineno + 0.5, depth, 'insert', (first.lineno, new)))
      else:
        ops.append((first.lineno, 0, 'delete', (first.lineno, first.end_lineno)))
        ops.append((first.lineno - 0.5, depth, 'insert', (first.lineno - 1, new)))
    else:
      ops.append((node.end_lineno + 0.5, depth, 'insert', (node.end_lineno, new)))

  # imports the placeholders need
  available = source_import_map(source_tree)
  import_lines, unresolved = [], []
  for name in sorted(used - BUILTINS - set(source) - bound_names(tree)):
    if name in available:
      import_lines.append(available[name])
    elif name in FALLBACK_IMPORTS:
      import_lines.append(FALLBACK_IMPORTS[name])
    else:
      unresolved.append(name)
  if import_lines:
    position = import_position(tree)
    follow = lines[position] if position < len(lines) else None
    new = import_lines if follow is not None and not follow.strip() else [*import_lines, '']
    ops.append((position + 0.5, 10 ** 6, 'insert', (position, new)))

  for _position, _depth, kind, payload in sorted(ops, key = lambda op: (op[0], -op[1]), reverse = True):
    match kind:
      case 'insert':
        after, new = payload
        lines[after:after] = new
      case 'delete':
        start, end = payload
        del lines[start - 1:end]
      case 'replace':
        number, text = payload
        lines[number - 1] = text
  return lines, unresolved

# ----- comparing

def documented(node, section):
  """names listed under a Google style section (Args, Attributes) of the docstring, None without a docstring"""
  doc = ast.get_docstring(node)
  if doc is None:
    return None
  names, inside, level = [], False, 0
  for line in doc.splitlines():
    if line and not line[0].isspace():
      inside, level = line.rstrip() == f'{section}:', 0
    elif inside and (match := re.match(r'( +)(\*{0,2}\w+)[^:]*:', line)):
      level = level or len(match[1]) # the first entry sets the indent, deeper lines are continuations
      if len(match[1]) == level:
        names.append(match[2])
  return names

def compare_docs(qualified, section, expected, node, issues):
  found = documented(node, section)
  if found is None:
    return
  missing = [name for name in expected if name not in found]
  unknown = [name for name in found if name not in expected]
  if missing or unknown:
    parts = [f"missing {', '.join(missing)}" if missing else '', f"unknown {', '.join(unknown)}" if unknown else '']
    issues.append(Issue(node.lineno, f"{qualified} docstring {section}: {'; '.join(part for part in parts if part)}", on_stub = True))

def compare(source, stub, scope, container, issues):
  for name, member in source.items():
    qualified = f'{scope}{name}'
    other = stub.get(name)
    if other is None:
      issues.append(Issue(member.line, f'{qualified} ({member.kind}) is missing from the stub', action = Action('add', name, member, container)))
    elif 'import' in (member.kind, other.kind):
      continue
    elif (member.kind == 'class') != (other.kind == 'class'):
      issues.append(Issue(other.line, f'{qualified} is a {member.kind} in the source but a {other.kind} in the stub', on_stub = True))
    elif member.kind == 'class':
      compare(member.members, other.members, f'{qualified}.', other, issues)
      if not is_enum(member.node) and not member.light:
        compare_docs(qualified, 'Attributes', attribute_names(member.members), other.node, issues)
    elif member.kind == other.kind == 'function':
      if member.is_async != other.is_async:
        issues.append(Issue(other.line, f'{qualified} async-ness differs from the source', on_stub = True))
      if member.count == other.count == 1 and member.signature != other.signature:
        text = f'{qualified} signature differs: source {format_signature(member.signature)} vs stub {format_signature(other.signature)}'
        issues.append(Issue(other.line, text, on_stub = True))
      if member.count == other.count == 1 and not member.light:
        compare_docs(qualified, 'Args', param_names(member.signature), other.node, issues)
  for name, other in stub.items():
    if name not in source:
      by_hand = other.kind == 'import' and len(other.node.names) > 1 # a grouped import has other names in it
      action = None if by_hand else Action('remove', name, other, container)
      issues.append(Issue(other.line, f'{scope}{name} ({other.kind}) is in the stub but not in the source', on_stub = True, action = action))

# ----- main

def main():
  parser = argparse.ArgumentParser(description = 'Keep the discord-stubs/ folder in sync with what the package exports.')
  parser.add_argument('--check', action = 'store_true', help = 'change nothing, exit 1 if the stubs are out of date or unfinished')
  parser.add_argument('--diff', action = 'store_true', help = 'change nothing, show what a normal run would change')
  options = parser.parse_args()

  files = sorted(path for path in PACKAGE.rglob('*.py') if not any(part == '__pycache__' or part.startswith('.') for part in path.parts))
  if not files:
    print(f'no .py files found in {PACKAGE}, run this from the repo root')
    return 1
  modules, parsed = index_package(files)
  if '' not in modules:
    print(f'could not read {PACKAGE}/__init__.py, nothing to export from')
    return 1
  exports = exported(modules)
  shared = imported_anywhere(modules)

  problems = [] # (path, line, text)
  notes = []
  failed = False
  for path in files:
    stub_path = STUBS_DIR / path.relative_to(PACKAGE).with_suffix('.pyi')
    imports = path.name == '__init__.py'
    source_tree = parsed[path]
    if isinstance(source_tree, SyntaxError):
      problems.append((path, source_tree.lineno or 1, f'could not parse source: {source_tree.msg}'))
      continue
    module = module_name(path)
    source = collect(source_tree.body, imports, {})
    if module: # the root __init__.py defines what is exported, everything else is internal
      for name, member in list(source.items()):
        result = resolve(modules, module, name)
        if member.kind == 'import' or result in exports:
          continue
        is_alias = isinstance(member.node, ast.TypeAlias) # signatures can use these, so they stay
        if member.kind == 'variable' and result not in shared and not is_alias:
          del source[name] # an internal constant nothing else imports, never stubbed
        else:
          set_light(member)
    exists = stub_path.exists()
    if not exists and not source:
      continue
    if not exists and options.check:
      problems.append((path, 1, f'no stub file ({len(list(flatten(source)))} public names)'))
      continue

    lines, stub_tree = [], ast.Module(body = [], type_ignores = [])
    if exists:
      try:
        lines, stub_tree = parse(stub_path)
      except SyntaxError as error:
        problems.append((stub_path, error.lineno or 1, f'could not parse stub: {error.msg}'))
        continue
    found = []
    compare(source, collect(stub_tree.body, imports, {}), '', None, found)

    actions = [issue.action for issue in found if issue.action]
    if actions and not options.check:
      try:
        new_lines, unresolved = apply_actions(list(lines), stub_tree, source_tree, source, actions)
        ast.parse('\n'.join(new_lines)) # never write something that doesn't parse
      except (SyntaxError, IndexError) as error:
        notes.append(f'{stub_path.as_posix()}: not updated, the result would not parse ({error})')
        failed = True
      else:
        if options.diff:
          diff = difflib.unified_diff(lines, new_lines, fromfile = f'a/{stub_path.as_posix()}', tofile = f'b/{stub_path.as_posix()}', lineterm = '')
          print('\n'.join(diff))
        else:
          stub_path.parent.mkdir(parents = True, exist_ok = True)
          stub_path.write_text('\n'.join(new_lines) + '\n', encoding = 'utf-8', newline = '\n')
          added = sum(a.kind == 'add' for a in actions)
          notes.append(f"{stub_path.as_posix()}: {'updated' if exists else 'created'}, added {added}" + (f', removed {len(actions) - added}' if added < len(actions) else ''))
          exists = True
        notes.extend(f'{stub_path.as_posix()}: placeholders use {name!r} but the source has no import for it, add one by hand' for name in unresolved)
        done = {id(action) for action in actions}
        found = [issue for issue in found if id(issue.action) not in done]
    problems.extend((stub_path if issue.on_stub else path, issue.line, issue.text) for issue in found)

    if exists and not options.diff:
      marked = [number for number, line in enumerate(stub_path.read_text(encoding = 'utf-8').splitlines(), 1) if TODO.search(line)]
      if marked:
        problems.append((stub_path, marked[0], f'{len(marked)} placeholder(s) left to fill in (search for "TODO")'))

  for note in notes:
    print(note)
  if not options.diff:
    for path, line, text in sorted(problems, key = lambda problem: (problem[0].as_posix(), problem[1])):
      print(f'{path.as_posix()}:{line}: {text}')
    if not (problems or notes):
      print('all stubs are up to date')
    elif problems:
      print(f'\n{len(problems)} thing(s) left to look at')
  if options.check:
    return int(bool(problems))
  return int(failed)

if __name__ == '__main__':
  sys.exit(main())
