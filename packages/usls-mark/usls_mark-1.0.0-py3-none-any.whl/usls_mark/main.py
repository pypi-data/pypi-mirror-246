import sys
from omegaconf import OmegaConf, DictConfig
import argparse
from rich.console import Console

from . import __version__, MarkerApp

CONSOLE = Console()


def run() -> None:
    if len(sys.argv) == 1:
        sys.argv.append("-h")

    args = parse_cli()
    CONSOLE.print(f"[b]Args: {args}")

    # build then run
    marker = MarkerApp(
        dir_image=args.i,
        classes=args.c,
        classes_kpts=args.kc,
    )
    with CONSOLE.status("Running...") as _:
        marker.mainloop()


def parse_cli() -> DictConfig:
    parser = argparse.ArgumentParser(
        description="🍇🍈🍉🍊🍋🍌🍍🥭🍎🍏🍐🍑🍒🍓🫐🥝🍅🫒🥥🥑",
        epilog=f"version: {__version__} ",
    )

    parser.add_argument("-i", required=True, type=str, help="Source directory")

    parser.add_argument(
        "-c",
        default=None,
        nargs="+",
        required=False,
        type=str,
        help="Class names",
    )
    parser.add_argument(
        "-kc",
        default=None,
        nargs="+",
        required=False,
        type=str,
        help="Keypoints class names",
    )

    parser.add_argument(
        "--version",
        "-v",
        "-V",
        action="version",
        version=f"version: {__version__}",
        help="Get version",
    )

    args = vars(parser.parse_args())
    return OmegaConf.create(args)


if __name__ == "__main__":
    run()
