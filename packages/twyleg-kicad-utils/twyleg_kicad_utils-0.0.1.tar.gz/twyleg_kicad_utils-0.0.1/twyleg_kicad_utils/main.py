# Copyright (C) 2023 twyleg
import fileinput
import re
import sys
import argparse
import logging
import subprocess

from pathlib import Path

from twyleg_kicad_utils import __version__

FORMAT = "[%(asctime)s][%(levelname)s][%(name)s]: %(message)s"


def init(args: argparse.Namespace):
    logging.error("Not yet implemented!")


def submodules(args: argparse.Namespace):
    gitmodules_file_path = Path(args.working_dir) / ".gitmodules"
    with open(gitmodules_file_path, "r") as gitmodules_file:
        for line in gitmodules_file:
            logging.info("%s", line.replace("\n", ""))


def submodules_set_protocol(args: argparse.Namespace):
    def replace_string_in_file(filepath: Path, text_to_search: str, replacement_text: str):
        with fileinput.FileInput(filepath, inplace=True) as file:
            for line in file:
                print(line.replace(text_to_search, replacement_text), end="")

    gitmodules_file_path = Path(args.working_dir) / ".gitmodules"

    if "https" in args.protocol:
        replace_string_in_file(gitmodules_file_path, "git@github.com:", "https://github.com/")
    else:
        replace_string_in_file(gitmodules_file_path, "https://github.com/", "git@github.com:")


def build(args: argparse.Namespace):
    subprocess.run([
        "podman", "run",
        "-v", f"{args.working_dir}/:/root/project/",
        "-w", "/root/project",
        "ghcr.io/inti-cmnb/kicad7_auto_full:latest",
        "kibot", "-c", "/root/project/external/twyleg_kicad_utils/kibot/default.kibot.yaml"
    ])


def build_bom(args: argparse.Namespace):
    logging.error("Not yet implemented!")


def build_images(args: argparse.Namespace):
    logging.error("Not yet implemented!")


def build_pdf(args: argparse.Namespace):
    logging.error("Not yet implemented!")


def build_3d(args: argparse.Namespace):
    logging.error("Not yet implemented!")


def main():
    logging.basicConfig(stream=sys.stdout, format=FORMAT, level=logging.INFO)

    #
    # Top-level parser
    #
    parser = argparse.ArgumentParser(description="foo")
    parser.add_argument(
        "-v",
        "--version",
        help="Show version and exit",
        action="version",
        version=__version__,
    )

    parser.add_argument(
        "-w",
        "--working_dir",
        help="Use a specific working directory. Default=./",
        type=str,
        default=Path.cwd()
    )

    subparsers = parser.add_subparsers(required=True, title='subcommands')

    #
    # Subcommand: init
    #
    parser_build = subparsers.add_parser('init', description="Initialize a project.")
    parser_build.set_defaults(func=init)

    #
    # Subcommand: submodules
    #
    parser_build = subparsers.add_parser('submodules', description="Manage git submodules.")
    parser_build.set_defaults(func=submodules)

    subparsers_submodules = parser_build.add_subparsers(required=False, title='subcommands')
    parser_submodules_set_protocol = subparsers_submodules.add_parser("set_protocol")
    parser_submodules_set_protocol.set_defaults(func=submodules_set_protocol)
    parser_submodules_set_protocol.add_argument(dest="protocol", metavar="{ssh,https}", choices=["ssh", "https"],
                                                nargs=1, help="Chose \"ssh\" or \"https\"")

    #
    # Subcommand: build
    #
    parser_build = subparsers.add_parser('build', description="Build project or specific parts of it.")
    parser_build.set_defaults(func=build)

    parser_build.add_argument(
        "-o",
        "--output_dir",
        help=f"Use a specific output dir for the results. Default=./export",
        type=str,
        default=Path.cwd() / "export"
    )

    subparsers_build = parser_build.add_subparsers(required=False, title='subcommands')
    parser_build_bom = subparsers_build.add_parser('bom')
    parser_build_bom.set_defaults(func=build_bom)

    parser_build_images = subparsers_build.add_parser('images')
    parser_build_images.set_defaults(func=build_images)

    parser_build_pdf = subparsers_build.add_parser('pdf')
    parser_build_pdf.set_defaults(func=build_pdf)

    parser_build_3d = subparsers_build.add_parser('3d')
    parser_build_3d.set_defaults(func=build_3d)

    args = parser.parse_args(sys.argv[1:])

    logging.info("twyleg_kicad_utils started!")
    logging.info("Command: %s", args.func.__name__.replace("_", " -> "))
    logging.info("Working dir: %s", args.working_dir)
    args.func(args)


if __name__ == "__main__":
    main()
