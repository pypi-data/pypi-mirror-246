"""
Main Builder Algorithm
"""
from logging import getLogger
import toml
from intelhex import IntelHex

from .pic18builder import FirmwareImagebuilderPic18
from .pic16builder import FirmwareImagebuilderPic16
from .avrbuilder import FirmwareImagebuilderAVR, AVR_ARCH_LIST
from .imageutils import FirmwareImage

def builder_factory(architecture, config):
    """ Factory for various architectures"""
    if architecture == "PIC18":
        # TODO - check the version requirements from the config file here too before creating the object
        return FirmwareImagebuilderPic18(config)
    if architecture == "PIC16":
        # TODO - check the version requirements from the config file here too before creating the object
        return FirmwareImagebuilderPic16(config)
    if architecture in AVR_ARCH_LIST:
        # TODO - check the version requirements from the config file here too before creating the object
        return FirmwareImagebuilderAVR(config)
    raise NotImplementedError (f"Unsupported architecture '{architecture}'")


def build(input_filename, config_filename, output_filename, hexdump_filename=None, include_empty_blocks=False):
    """
    Does the build
    """
    logger = getLogger(__name__)

    # The goal is to generate a new firmware image
    image = FirmwareImage()

    # Read in hex file for conversion
    hexfile = IntelHex()
    hexfile.fromfile(input_filename, format='hex')

    # Read in config which was generated when this bootloader was built
    logger.debug("Loading bootloader config from %s", config_filename)
    bootloader_config = toml.load(config_filename)

    # Find out which architecture is used
    architecture = bootloader_config['bootloader']['ARCH']
    architecture_variant = builder_factory(architecture, bootloader_config)

    # Generate the first block and add it
    first_block = architecture_variant.generate_metadata_block()
    image.add_block(first_block)

    # Parse the hexfile
    segments = hexfile.segments()
    for segment in segments:
        segment_start, segment_stop = segment
        logger.debug("Segment from %08X to %08X", segment_start, segment_stop)

        # Check if this segment is relevant
        if not architecture_variant.include_segment(segment_start):
            logger.debug("Skipping")
            continue

        # Extract data for this segment
        segment_data = hexfile.tobinarray(start=segment_start, end=segment_stop-1)
        logger.debug("Adding segment of length: %d", len(segment_data))

        address = segment_start
        # Loop through the segment creating blocks
        while segment_data:
            # Set the block address
            logger.debug("Address: %X", address)
            block, bytes_filled = architecture_variant.generate_operational_block(address, segment_data)

            # Add block to image, adjust remaining data and counters
            if include_empty_blocks or not block.is_empty():
                image.add_block(block)
            else:
                logger.debug("Skipping empty block at address %08x", address)
            segment_data = segment_data[bytes_filled:]
            logger.debug("Data remaining: %d", len(segment_data))
            address += bytes_filled

    # Save to target image file
    if output_filename:
        image.save(output_filename)
        logger.info("Image written to '%s'", output_filename)

    # Return human readable form for display
    if hexdump_filename:
        image.dump(hexdump_filename)
        logger.info("Ascii version of image written to '%s'", hexdump_filename)

    return str(image)
