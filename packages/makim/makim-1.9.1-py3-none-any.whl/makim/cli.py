"""Cli functions to define the arguments and to call Makim."""
import argparse
import os
import sys

from pathlib import Path

from makim import Makim, __version__


class CustomHelpFormatter(argparse.RawTextHelpFormatter):
    """Formatter for generating usage messages and argument help strings.

    Only the name of this class is considered a public API. All the methods
    provided by the class are considered an implementation detail.
    """

    def __init__(
        self,
        prog,
        indent_increment=2,
        max_help_position=4,
        width=None,
        **kwargs,
    ):
        """Define the parameters for the argparse help text."""
        super().__init__(
            prog,
            indent_increment=indent_increment,
            max_help_position=max_help_position,
            width=width,
            **kwargs,
        )


makim = Makim()


def _get_args():
    """
    Define the arguments for the CLI.

    note: when added new flags, update the list of flags to be
          skipped at extract_makim_args function.
    """
    makim_file_default = str(Path(os.getcwd()) / '.makim.yaml')

    parser = argparse.ArgumentParser(
        prog='Makim',
        description=(
            'Makim is a tool that helps you to organize '
            'and simplify your helper commands.'
        ),
        epilog=(
            'If you have any problem, open an issue at: '
            'https://github.com/osl-incubator/makim'
        ),
        add_help=False,
        formatter_class=CustomHelpFormatter,
    )
    parser.add_argument(
        '--help',
        '-h',
        action='store_true',
        help='Show the help menu',
    )

    parser.add_argument(
        '--version',
        action='store_true',
        help='Show the version of the installed Makim tool.',
    )

    parser.add_argument(
        '--verbose',
        action='store_true',
        help='Show the commands to be executed.',
    )

    parser.add_argument(
        '--dry-run',
        action='store_true',
        help="Show the commands but don't execute them.",
    )

    parser.add_argument(
        '--makim-file',
        type=str,
        default=makim_file_default,
        help='Specify a custom location for the makim file.',
    )

    try:
        idx = sys.argv.index('--makim-file')
        makim_file = sys.argv[idx + 1]
    except ValueError:
        makim_file = makim_file_default

    makim.load(makim_file)
    target_help = []
    groups = makim.global_data.get('groups', [])
    for group in groups:
        target_help.append('\n' + group + ':')
        target_help.append('-' * (len(group) + 1))
        for target_name, target_data in groups[group]['targets'].items():
            target_name_qualified = f'{group}.{target_name}'
            help_text = target_data['help'] if 'help' in target_data else ''
            target_help.append(f'  {target_name_qualified} => {help_text}')

            if 'args' in target_data:
                target_help.append('    ARGS:')

                for arg_name, arg_data in target_data['args'].items():
                    target_help.append(
                        f'      --{arg_name}: ({arg_data["type"]}) '
                        f'{arg_data["help"]}'
                    )

    parser.add_argument(
        'target',
        nargs='?',
        default=None,
        help=(
            'Specify the target command to be performed. Options are:\n'
            + '\n'.join(target_help)
        ),
    )

    return parser


def show_version():
    """Show version."""
    print(__version__)


def extract_makim_args():
    """Extract makim arguments from the CLI call."""
    makim_args = {}
    index_to_remove = []
    for ind, arg in enumerate(list(sys.argv)):
        if arg in [
            '--help',
            '--version',
            '--verbose',
            '--makim-file',
            '--dry-run',
        ]:
            continue

        if not arg.startswith('--'):
            continue

        index_to_remove.append(ind)

        arg_name = None
        arg_value = None

        next_ind = ind + 1

        arg_name = sys.argv[ind]

        if (
            len(sys.argv) == next_ind
            or len(sys.argv) > next_ind
            and sys.argv[next_ind].startswith('--')
        ):
            arg_value = True
        else:
            arg_value = sys.argv[next_ind]
            index_to_remove.append(next_ind)

        makim_args[arg_name] = arg_value

    # remove exclusive makim flags from original sys.argv
    for ind in sorted(index_to_remove, reverse=True):
        sys.argv.pop(ind)

    return makim_args


def app():
    """Call the makim program with the arguments defined by the user."""
    makim_args = extract_makim_args()
    args_parser = _get_args()
    args = args_parser.parse_args()

    if args.version:
        return show_version()

    if not args.target or args.help:
        return args_parser.print_help()

    if args.help:
        return args_parser.print_help()

    makim.load(args.makim_file)
    makim_args.update(dict(args._get_kwargs()))
    return makim.run(makim_args)
