from pathlib import Path

FILE_CONT = """
{
  // See https://go.microsoft.com/fwlink/?LinkId=733558
  // for the documentation about the tasks.json format
  "version": "1.0.0",
  "tasks": [
    {
      "label": "AnyErpLint",
      "type": "process",
      "command": "python",
      "args": ["-m", "anyerplint", "check", "${file}"],
      "group": "test",
      "presentation": {
        "reveal": "always",
        "panel": "dedicated"
      }
    }
  ]
}
"""

import argparse


def handle_init(args: argparse.Namespace) -> None:
    init_vscode()


def init_parser(parser: argparse.ArgumentParser) -> argparse.ArgumentParser:
    """Declare arguments you need here."""
    parser.set_defaults(func=handle_init)
    return parser


def init_vscode() -> None:
    target = Path().absolute() / ".vscode/tasks.json"
    print(
        "This command will allow running AnyErpLint check tasks under current directory."
    )
    print("Press ENTER to create AnyErpLint vscode task at", target)
    input()
    target.parent.mkdir(exist_ok=True)
    target.write_text(FILE_CONT)
    print(
        "Done! Now run ctrl+shift+P 'Run task' and select AnyErpLint while editing a file."
    )
