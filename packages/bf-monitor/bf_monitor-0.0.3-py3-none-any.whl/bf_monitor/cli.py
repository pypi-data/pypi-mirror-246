import os, sys
import argparse
import inspect

from .utils import USER, NAME, VERSION, ENTRY_POINTS
from .driver import Monitor

CLI_ENTRY = ENTRY_POINTS[0]

def _line():
    try:
        width = os.get_terminal_size().columns
    except:
        width = 32
    return "="*width
    
class ArgumentParser(argparse.ArgumentParser):
    def error(self, message):
        self.print_help(sys.stderr)
        self.exit(2, '\n%s: error: %s\n' % (self.prog, message))

class CommandLineInterface:
    def _get_fn_name(self):
        return inspect.stack()[1][3]

    def run(self, args):
        parser = ArgumentParser(
            prog = f'{CLI_ENTRY} {self._get_fn_name()}',
        )
        parser.add_argument('-u', '--url', help="url to notify", required=True)
        parser.add_argument('-p', '--path', help="path to watch", required=True)
        parsed_args = parser.parse_args(args)

        Monitor(parsed_args.url, parsed_args.path)

    def help(self, args=None):
        help = [
            f"{NAME} v{VERSION}",
            f"https://github.com/{USER}/{NAME}",
            f"",
            f"Syntax: {CLI_ENTRY} COMMAND [OPTIONS]",
            f"",
            f"Where COMMAND is one of:",
        ]+[f"- {k}" for k in COMMANDS]+[
            f"",
            f"for additional help, use:",
            f"{CLI_ENTRY} COMMAND -h/--help",
        ]
        help = "\n".join(help)
        print(help)
COMMANDS = {k:v for k, v in CommandLineInterface.__dict__.items() if k[0]!="_"}

def main():
    cli = CommandLineInterface()
    if len(sys.argv) <= 1:
        cli.help()
        return

    COMMANDS.get(# calls command function with args
        sys.argv[1], 
        CommandLineInterface.help # default
    )(cli, sys.argv[2:]) # cli is instance of "self"

if __name__ == "__main__":
    main()
