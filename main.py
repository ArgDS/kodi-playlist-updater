import getopt
import logging
import sys

from kodi.Application import run
from loggerConfiguration import setup_logging

setup_logging()

logger = logging.getLogger(__name__)


def main(argv):
    try:
        opts, args = getopt.getopt(argv, "hc", ["config="])
    except getopt.GetoptError:
        logger.error("Use next format main.py --config=...")
        sys.exit(2)
    for opt, arg in opts:
        if opt == "-h":
            print("main.py --config=...")
            sys.exit(2)
        if opt in ("-c", "--config"):
            run(arg)
            sys.exit(0)
    print("Does not find any argument! \nType \"python main.py -h\"")


if __name__ == "__main__":
    main(sys.argv[1:])
