"""
Command line interface for epion library.

Usage:
  epion [-v | -vv] [options]
  epion (-h | --help)
  epion --version

 Options:
  -h --help                 Show this screen.
  -v                        Increase verbosity.
  -vv                       Increase verbosity more.
  --version                 Show version.
  --token=<token>           API Token to use
"""
import logging
import sys

import pkg_resources
from docopt import docopt

from .epion import Epion


def main(argv=sys.argv[1:]):
    """Parse argument and start main program."""
    args = docopt(__doc__, argv=argv,
                  version=pkg_resources.require('epion')[0].version)

    level = logging.ERROR
    if args['-v']:
        level = logging.INFO
    if args['-v'] == 2:
        level = logging.DEBUG
    logging.basicConfig(level=level)

    log = logging.getLogger(__name__)
    log.info("Start...")

    token = args['--token']

    #api = epion.Epion(token)
    #result = api.get_current()
    #log.debug("Retrieved data:\n%s", result)

    #print(result)


if __name__ == '__main__':
    # execute only if run as the entry point into the program
    main()