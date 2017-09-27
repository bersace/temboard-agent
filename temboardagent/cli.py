from distutils.util import strtobool
import logging
import os
import pdb
import sys

from .errors import UserError
from .logger import LOG_FORMAT


logger = logging.getLogger(__name__)


def define_common_arguments(parser):
    parser.add_argument(
        '-c', '--config',
        action='store', dest='configfile',
        default='/etc/temboard-agent/temboard-agent.conf',
        help="Configuration file. Default: %(default)s",
    )


def cli(main):
    # A decorator to add consistent CLI bootstrap
    #
    # Decorated function must accept argv and environ arguments and return an
    # exit code.
    #
    # The decorator adds basic logging setup and error management. The
    # decorated function can just raise exception and log using logging module
    # as usual.

    def cli_wrapper(argv=sys.argv[1:], environ=os.environ):
        debug = strtobool(environ.get('DEBUG', '0'))

        retcode = 1
        try:
            logging.basicConfig(
                level=logging.DEBUG if debug else logging.INFO,
                format=LOG_FORMAT,
            )
            logger.debug("Starting temBoard agent.")
            retcode = main(argv, environ) or 1
        except pdb.bdb.BdbQuit:
            logger.info("Graceful exit from debugger.")
        except UserError as e:
            retcode = e.retcode
            logger.critical("%s", e)
        except Exception:
            logger.exception('Unhandled error:')
            if debug:
                pdb.post_mortem(sys.exc_info()[2])
            else:
                logger.error("This is a bug!")
                logger.error(
                    "Please report traceback to "
                    "https://github.com/dalibo/temboard-agent/issues! Thanks!"
                )

        exit(retcode)
    return cli_wrapper