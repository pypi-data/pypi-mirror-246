import argparse
import os
from pathlib import Path
import re
import glob

emit = print


def render(cont: str) -> bool:
    error = False
    tokens = re.split(r"([\{\(\}\)\[\];\n])", cont)
    tokens = [t.strip() for t in tokens if t.strip()]
    indent = 0

    stack: list[str] = []
    enders = {"{": "}", "(": ")", "[": "]"}

    # simplify round, merge () and single ;

    for i, t in enumerate(tokens):
        if not t:
            continue
        # last char would be index out of range
        if i == len(tokens) - 1:
            break

        if t in enders and tokens[i + 1] == enders[t]:
            tokens[i] = t + tokens[i + 1]
            tokens[i + 1] = None
        if t == ";" and tokens[i - 1] and ";" not in tokens[i - 1]:
            tokens[i] = None
            tokens[i - 1] = tokens[i - 1] + " ;"

    # remove nones
    tokens = [t for t in tokens if t]

    for t in tokens:
        t = t.strip()
        if not t:
            continue

        brace = t.strip(" ;")
        if brace == "}" or brace == ")" or brace == "]":
            indent -= 1
            got = stack.pop()
            expected = enders[got]
            if brace != expected:
                emit("ERROR: Expected", expected, "got", t)

        emit(indent * "  " + t)

        if brace == "{" or brace == "(" or brace == "[":
            indent += 1
            stack.append(brace)

    if stack:
        emit("Stack was not empty in the end:", stack)
        error = True

    return error


def handle_nest(args: argparse.Namespace) -> None:
    for pat in args.filename:
        if os.path.isdir(pat):
            pat = pat + "/**/*.xml"
        fnames = glob.glob(pat, recursive=True) if "*" in pat else [pat]
        for f in fnames:
            emit("<-- ---- ", f, "-------- -->")
            try:
                render(open(f).read())
            except Exception as e:
                emit(f"**************************  ERROR:: {e}")
                continue


def init_parser(parser: argparse.ArgumentParser) -> argparse.ArgumentParser:
    """Declare arguments you need here."""
    parser.add_argument("filename", nargs="+", help="File to pretty print")
    parser.set_defaults(func=handle_nest)
    return parser
