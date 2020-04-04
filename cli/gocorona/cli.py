"""
gocorona

Usage:
  gocorona hello
  gocorona -h | --help
  gocorona --version

Options:
  -h --help                         Show this screen.
  --version                         Show version.

Examples:
  gocorona hello

Help:
  For help using this tool, please open an issue on the Github repository:
  https://github.com/GoCorona-org/Backend
"""


from inspect import getmembers, isclass

from docopt import docopt

from . import __version__ as VERSION


def main():
    """Main CLI entrypoint."""
    import gocorona.commands
    options = docopt(__doc__, version=VERSION)

    # Here we'll try to dynamically match the command the user is trying to run
    # with a pre-defined command class we've already created.
    for (k, v) in options.items(): 
        if hasattr(gocorona.commands, k) and v:
            module = getattr(gocorona.commands, k)
            gocorona.commands = getmembers(module, isclass)
            command = [command[1] for command in gocorona.commands if command[0] != 'Base'][0]
            command = command(options)
            command.run()
