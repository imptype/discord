import os
import sys
import logging
import argparse
import importlib
from functools import reduce
from importlib import metadata
from .log import enable_logs

def main(argv = None):
  parser = argparse.ArgumentParser(prog = 'discord', description = 'A CLI to run an ASGI server or to check the PyPI version.')
  parser.add_argument('app', help = 'the location of the ASGI app, for example `main:app`')
  parser.add_argument('--host', default = '127.0.0.1', help = 'the host string, default is `127.0.0.1`')
  parser.add_argument('--port', type = int, default = 8000, help = 'the port number, default is `8000`')
  parser.add_argument('--log-level', default = 'info', choices = ['debug', 'info', 'warning', 'error', 'critical'],
    help = 'override log level, default is `info`')

  parser.add_argument('--version', action = 'version', version = f'idiscord {metadata.version('idiscord')}',
    help = 'show the library version and exit')

  args = parser.parse_args(argv)

  if args.log_level:
    enable_logs(level = getattr(logging, args.log_level.upper()))

  sys.path.insert(0, os.getcwd())
  module, attribute = args.app.split(':')
  app = reduce(getattr, attribute.split('.'), importlib.import_module(module))
  app.run(args.host, args.port)
