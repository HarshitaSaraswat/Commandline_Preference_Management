import sys
from flags import START_FLAG, ERROR_FLAG, EXIT_FLAG


def main():
    from Commandline_Preference_Management.src.interface import CommandLineInterface
    cli = CommandLineInterface(sys.argv[1:])
    cli.run()

try:
    print(START_FLAG)
    main()
except Exception as exc:
    print(ERROR_FLAG)
    print(exc)
finally:
    print(EXIT_FLAG)