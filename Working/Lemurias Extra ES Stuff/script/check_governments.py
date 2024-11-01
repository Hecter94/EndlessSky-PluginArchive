"""
Checks systems to ensure that they have a "government" node set.
"""

__author__ = "Lemuria"
__version__ = "0.1.0"
__license__ = "GPL 3"

import argparse
import endlessparser as ep

def check_node(node: ep.Node):
    if type(node) is not ep.SystemNode:
        return
    if node.government() is None:
        print(f"No government in system {node.name()}")
    else:
        if node.government() == "Sayari Plushies":
            print(f"Government in system {node.name()} uses `Sayari Plushies`, that is the display name. The actual name is `Sayari Plushie`.")

def main(args):
    with open(args.file, "r") as f:
        nodes = ep.parse(text=f.read())
        for node in nodes:
            check_node(node)


if __name__ == "__main__":
    parser = argparse.ArgumentParser()

    # Required positional argument
    parser.add_argument("file", help="Required positional argument")

    # Specify output of "--version"
    parser.add_argument(
        "--version",
        action="version",
        version="%(prog)s (version {version})".format(version=__version__),
    )

    args = parser.parse_args()
    main(args)
