"""
main moduel
"""

from subprocess import getoutput

import argparse
import re


def get_args() -> argparse.Namespace:
    """parse command-line arguments

    Returns:
        argparse.Namespace: parsed arguments
    """

    # define argument parser
    parser = argparse.ArgumentParser(
        description="Download python packages and make an installer file."
    )
    # add arguments
    parser.add_argument("name", help="Package name to download")

    return parser.parse_args()


def write_installer(text: str, name: str):
    """make an installer file for package

    Args:
        text (str): text of download install process
        name (str): package to download
    """

    # split text into lines
    lines = [line.strip() for line in text.split("\n")]

    # get package version and make filename
    version = re.findall("-[0-9.]+[-.]", lines[1])[0][1:-1]
    filename = f"{name}-{version}.txt"

    # find all dependencies
    dependencies = [
        line[line.rindex("\\") + 1:]
        for line in lines
        if line[:4] == "File" or line[:5] == "Saved"
    ]

    # write installer text
    with open(f"{filename}", "w", encoding="utf8") as file:
        file.write("\n".join(dependencies))


def main():
    """
    main function
    """

    # get command-line arguments
    args = get_args()

    # download python package and make an installer file
    out = getoutput(f"pip download {args.name} --timeout 600")
    write_installer(out, args.name)


if __name__ == "__main__":
    main()
