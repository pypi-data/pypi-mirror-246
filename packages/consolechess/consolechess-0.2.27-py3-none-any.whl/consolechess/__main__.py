"""Play a game of chess in Python module mode, i.e. `python -m chess`."""

from sys import argv

from . import asciiconsole, console, tui


def main() -> None:
    """Start chess."""
    args = " ".join(argv)
    if "ascii" in args or "-a" in args:
        asciiconsole.main()
    elif " console" in args or "-c" in args:
        console.main()
    else:
        tui.main()


if __name__ == "__main__":
    main()
