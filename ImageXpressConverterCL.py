import argparse
from pathlib import Path
import logging
from ImageXpress import processfolder


def get_args() -> argparse.Namespace:
    myparser = argparse.ArgumentParser(
        formatter_class=argparse.ArgumentDefaultsHelpFormatter
    )
    myparser.add_argument(
        "-i",
        type=str,
        help="The root input folder containing all the separate tif images",
        default=Path.cwd(),
    )
    myparser.add_argument(
        "-l",
        type=str,
        help="LogLevel: 0 error (default), 1 warning, 2 info",
        default=0,
    )
    myparser.add_argument(
        "-o", type=str, help="Output folder", default=Path(Path.cwd(), "Output")
    )
    return myparser.parse_args()


if __name__ == "__main__":
    args = get_args()
    loglevels = [logging.ERROR, logging.WARNING, logging.INFO]
    loglevel = loglevels[int(args.l)]
    logging.basicConfig(level=loglevel)
    logging.info("Arguments parsed")
    logging.info(f"Loglevel: {logging.getLevelName(loglevel)}")
    if not Path(args.o).exists():
        print(f"{args.o} does not exist. Shall I create it for you? (y/n)")
        x = input()
        if x == "y":
            Path(args.o).mkdir(parents=True)
            processfolder(Path(args.i), Path(args.o))
        else:
            print("Ok. Goodbye!")
    else:
        processfolder(Path(args.i), Path(args.o))
