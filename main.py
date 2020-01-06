import getopt
import logging
import sys

from kodi.Application import run, init
from loggerConfiguration import setup_logging

setup_logging()

logger = logging.getLogger(__name__)


def main(argv):
    try:
        opts, args = getopt.getopt(argv, "hci", ["config=", 'init'])
    except getopt.GetoptError:
        logger.error("Use next format main.py --config=...")
        sys.exit(2)
    config_path = None
    init_act = False
    for opt, arg in opts:
        if opt == "-h":
            print("main.py --config=...")
            sys.exit(2)
        if opt in ("-c", "--config"):
            config_path = arg
        if opt in ("-i", "--init"):
            init_act = True
    if not config_path:
        print("Does not find any argument! \nType \"python main.py -h\"")
        return
    try:
        if init_act:
            init(config_path)
        else:
            run(config_path)
    except BaseException as ex:
        logger.error("Catch exception", exc_info=ex)


if __name__ == "__main__":
    main(sys.argv[1:])
