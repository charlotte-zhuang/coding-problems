"""Starts the heap runtime test CLI app.

Example:
    $ python3 start.py

Attributes:
    FILE_NAME_FILTER (Pattern[str]): Regular expression to filter out invalid
        characters from a filename.
    DATA_DIR (Path): The path to the data directory.
    CONFIG_DIR (Path): The path to the config directory.
    DEFAULT_OPTIONS (dict[str, (str or int)]): Default config for the gen
        module.
"""

import sys
from pathlib import Path
import re

sys.path.append(str(Path(__file__).parent.parent.absolute()))

import gen
import run

FILE_NAME_FILTER = re.compile("[^a-zA-Z0-9_\-]")
DATA_DIR = Path(__file__).parent.parent.absolute() / "data"
CONFIG_DIR = Path(__file__).parent.parent.absolute() / "config"
DEFAULT_OPTIONS = {
    "name": "default",
    "size": 1000,
    "op": 1000000,
    "addfreq": 1,
    "decfreq": 8,
    "popfreq": 1,
    "minval": int(-1e9),
    "maxval": int(1e9),
}


def main():
    """Runs the heap tester."""

    print(
        "\n==================\n"
        "=  Heap-o-Matic  =\n"
        "=                =\n"
        "=  by charlotte  =\n"
        "=================="
    )
    display_help()
    try:
        while True:
            args = input_command()
            try:
                if args[0] == "gen":
                    gen_command(args)
                elif args[0] == "run":
                    run_command(args)
                elif args[0] == "help":
                    display_help(args)
                else:
                    print("Invalid command. Type 'help' to display all commands.")
            except CancelException:
                pass
    except ExitException:
        print("bye ^.^")


# Commands


def gen_command(args: tuple[str]) -> None:
    """Command to generate test data.

    Args:
        args (tuple[str]): The config filename. Default config used if no
            filename specified.

        ("gen", Optional(str))
    """

    if len(args) < 1:
        print("Invalid option. Type 'help gen' for usage")
        return
    if len(args) == 1:
        options = DEFAULT_OPTIONS
    else:
        config = CONFIG_DIR / args[1]
        if not config.is_file():
            print(f"File not found: {config}")
            return
        options = read_config(config)
    test_data = DATA_DIR / options["name"]
    print("generating...")
    t, a, d, p, miv, mav = gen.random_test(
        test_data=test_data,
        size=options["size"],
        op=options["op"],
        addfreq=options["addfreq"],
        decfreq=options["decfreq"],
        popfreq=options["popfreq"],
        minval=options["minval"],
        maxval=options["maxval"],
    )
    display_test_data(t, a, d, p, miv, mav)


def run_command(args: tuple[str]) -> None:
    """Command to run tests.

    Args:
        args (tuple[str]): The heap to use and test data filename.
            data/default used if no filename specified.

        ("run", "p" or "f" or "b", Optional(str))
    """

    if len(args) < 2:
        print("Invalid options. Type 'help run' for usage")
        return
    if len(args) == 2:
        data = DATA_DIR / "default"
    else:
        data = DATA_DIR / args[2]
    if not data.is_file():
        print("Test data not found. Use the gen command if you haven't already.")
        return
    if args[1] == "p":
        print("running...")
        time = run.pairing_time(data)
        print(f"\nPairing heap runtime: {time:.5} s\n")
    elif args[1] == "f":
        print("running...")
        time = run.fibonacci_time(data)
        print(f"\nFibonacci heap runtime: {time:.5} s\n")
    elif args[1] == "b":
        print("running...")
        time = run.binary_time(data)
        print(f"\nBinary heap runtime: {time:.5} s\n")
    else:
        print("Invalid option. Type 'help run' for usage.")


# I/O


def display_help(args: tuple[str] = ("help",)) -> None:
    """Prints the available commands and their usage.

    Args:
        args (tuple[str]): The command to display help for.

        ("help", Optional(command: str))
    """

    if len(args) <= 1:
        print(
            "\nCommands\n"
            "  gen   Generate test data\n"
            "  run   Run a test\n"
            "  help  Display this help message\n"
            "  exit  Stop testing\n"
            "Type 'help <command>' to show more details.\n"
        )
    elif args[1] == "gen":
        print(
            "\nGenerate test data\n"
            "  usage: gen [config]\n"
            "  Where [config] is the name of the config file,\n"
            "  located in the config/ directory. Omit to use\n"
            "  default values.\n"
        )
    elif args[1] == "run":
        print(
            "\nMeasure a heap's runtime\n"
            "  usage: run <heap> [data]\n"
            "  Where <heap> is one of the following:\n"
            "    p -> pairing heap\n"
            "    f -> Fibonacci heap\n"
            "    b -> binary heap\n"
            "  And [data] is the name of the test data file,\n"
            "  located in the data/ directory. Omit to use\n"
            "  the default data file.\n"
        )
    elif args.count("help") > 2:
        print("same qq")
    elif args[1] == "help":
        print(
            "\nDisplay command information\n"
            "  usage: help [command]\n"
            "  Where [command] is the command to get help for.\n"
            "  Omit [command] to display all commands.\n"
        )
    elif args[1] == "exit":
        print("\nExit this application\n  usage: exit\n")
    else:
        print("Unrecognized command. Type 'help' to show all commands.")


def display_test_data(
    total: int, add: int, dec: int, pop: int, minval: int, maxval: int
) -> None:
    """Prints a formatted test composition message.

    Args:
        total (int): The total number of operations.
        add (int): The number of add operations.
        dec (int): The number of decrease key operations.
        pop (int): The number of pop minimum operations.
        minval (int): The minimum possible value in the heap.
        maxval (int): The maximum possible value in the heap.
    """

    print(
        "\n-----Test Composition-----\n"
        f"operations {total:,}\n"
        f"add        {add / total:.2%}\n"
        f"decrease   {dec / total:.2%}\n"
        f"pop min    {pop / total:.2%}\n"
        f"min value  {minval:,}\n"
        f"max value  {maxval:,}\n"
        f"--------------------------\n"
    )


def input_command() -> tuple[str]:
    """Takes input for a command.

    Returns:
        tuple[str]: The command and arguments passed.

    Raises:
        ExitException: If the command is "exit"
    """

    print("> ", end="")
    args = input().lower().split()
    if args[0] == "exit":
        raise ExitException()
    return args


def read_config(file: Path) -> dict[str, any]:
    """Reads a config file.

    Args:
        file (Path): The config file.

    Returns:
        dict[str, int]: Options and their values. Default values are
            used if the options wasn't read.
    """

    options = DEFAULT_OPTIONS.copy()
    options["name"] = file.name
    with file.open(mode="r") as config:
        for line in config:
            params = line.lower().split()
            if len(params) >= 2:
                if params[0] == "name":
                    options[params[0]] = params[1]
                elif params[0] in options:
                    try:
                        options[params[0]] = int(params[1])
                    except ValueError:
                        pass
    options["name"] = FILE_NAME_FILTER.sub("", options["name"])
    options["size"] = max(0, options["size"])
    options["op"] = max(0, options["op"])
    if options["op"] == 0 and options["size"] == 0:
        options["op"] = 1
    options["addfreq"] = max(0, options["addfreq"])
    options["decfreq"] = max(0, options["decfreq"])
    options["popfreq"] = max(0, options["popfreq"])
    if options["addfreq"] + options["decfreq"] + options["popfreq"] == 0:
        options["addfreq"] = 1
        options["decfreq"] = 1
        options["popfreq"] = 1
    options["minval"] = min(options["minval"], options["maxval"])
    return options


# Exceptions


class ExitException(Exception):
    """When the user wants to exit the application."""

    pass


class CancelException(Exception):
    """When the user wants to cancel a command."""

    pass


if __name__ == "__main__":
    main()
