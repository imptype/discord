"""
format.py - Runs ruff and removes double blank lines.
"""

import ast
import difflib
import subprocess
import sys
from pathlib import Path

def fix(src):
  lines = src.split('\n')
  protected = set()
  for node in ast.walk(ast.parse(src)):
    if isinstance(node, (ast.Constant, ast.JoinedStr)):
      end = node.end_lineno
      if (
        end is not None
        and end != node.lineno
        and (isinstance(node, ast.JoinedStr) or isinstance(node.value, str))
      ):
        protected.update(range(node.lineno, end + 1))
  out = []
  prev_blank = False
  for i, line in enumerate(lines, 1):
    blank = not line.strip() and i not in protected
    if blank and prev_blank:
      continue
    out.append(line)
    prev_blank = blank
  return '\n'.join(out)

def ruff(*args):
  subprocess.run([sys.executable, '-m', 'ruff', *args], check=False)

def diff(path, old, new):
  return ''.join(
    difflib.unified_diff(
      old.splitlines(True), new.splitlines(True), str(path), str(path)
    )
  )

mode = sys.argv[1] if len(sys.argv) > 1 else ''
files = [*Path('.').glob('*.py'), *Path('discord').rglob('*.py')]
before = {p: p.read_text(encoding='utf-8', newline='') for p in files}

if mode == '--check':
  ruff('check', '.')
  for path in files:
    if before[path] != fix(before[path]):
      print(f'Would reformat {path}')
elif mode == '--diff':
  ruff('check', '--diff', '.')
  for path in files:
    new = fix(before[path])
    if before[path] != new:
      print(diff(path, before[path], new))
else:
  ruff('check', '--fix', '--show-fixes', '.')
  ruff('format', '--quiet', '.')
  for path in files:
    current = path.read_text(encoding='utf-8', newline='')
    new = fix(current)
    if new != current:
      path.write_text(new, encoding='utf-8', newline='')
    if new != before[path]:
      print(f'Reformatted {path}')
