"""
Python firmware image builder main
"""

from pathlib import Path
from logging import getLogger
from .builder import build

def pyfwimagebuilder(args):
    """
    Main program
    """
    logger = getLogger(__name__)
    if args.output:
        imagefilename = args.output
    else:
        imagefilename = Path(args.input).stem + '.img'

    logger.info("pyfwimagebuilder - Python firmware image builder for Microchip mdfu bootloaders")

    logger.debug("Input hex file: '%s'", args.input)
    logger.debug("Config file: '%s'", args.config)
    logger.debug("Output img file: '%s'", imagefilename)
    if args.dump:
        logger.debug("Hex dump file: '%s'", args.dump)
    build(args.input, args.config, imagefilename, args.dump, args.include_empty_blocks)

    logger.info("Image building complete")
