"""
Common Firmware Builder functions for MCU8 builders.
"""
from .imageutils import ImageBlock
from .firmwareimagebuilder import FirmwareImageBuilder
from logging import getLogger
from packaging.version import parse as version_parse

logger = getLogger(__name__)

"""
Block Types for MCU8
0 - Nothing has been set. The bootloader will never use a block type of zero.
1 - Metadata block
2 - Flash data operation block, used to transfer bytes that appear between FLASH_START and FLASH_END
3 - EEPROM data operation block, used to transfer bytes that appear between EEPROM_START and EEPROM_END
"""
class BlockTypeMcu8(enumerate):
    UNINITIALIZED = 0
    METADATA_OPERATION = 1
    FLASH_OPERATION = 2

class FirmwareImageBuilderMcu8 (FirmwareImageBuilder):
    def __init__(self, config):
        """
        Override - Set the default undefined data for MCU8 devices
        """
        super().__init__(config)
        self.UNDEFINED_SEQUENCE = 0xFF
        self.UNDEFINED_SEQUENCE_BYTE_LENGTH = 1
        self.max_format_version = '0.3.0'
        self.min_format_version = '0.3.0'
    """
    Image Builder functions
    """
    def versiontobytes(self, version):
        """
        Convert a major.minor.micro version string to little-endian bytes representation
        """
        format_version = version_parse(version)
        return ((int(format_version.major) << 16) + (int(format_version.minor) << 8) + (int(format_version.micro))).to_bytes(3, 'little')

    def include_segment(self, address):
        """
        Returns true if the segment must be included.

        :param address: Byte address of the segment.
        """
        if (address >= (self.config['bootloader']['FLASH_END']) or
            address < (self.config['bootloader']['FLASH_START'])):
            return False
        return True
    
    def empty_block(self, size):
        """
        Return platform-specific empty byte pattern block with given size in bytes.

        param: size: size of the block in bytes.
        """
        return size * self.UNDEFINED_SEQUENCE.to_bytes(self.UNDEFINED_SEQUENCE_BYTE_LENGTH, 'little')

    def is_valid_version(self, version):
        """
        Return true when the requested version is equal to or between the min and max version values of the class.

        :param: version: semver string.
        """
        requested_version =  version_parse(version)
        max_version = version_parse(self.max_format_version)
        min_version = version_parse(self.min_format_version)
        if min_version < requested_version and requested_version < max_version:
            result = True
        elif (min_version == requested_version or requested_version == max_version):
            result = True
        else:
            result = False
        return result

    def generate_operational_header(self):
        """
        Generate operational block header for basic MCU8 variant.
        """
        page_erase_key = self.config['bootloader']['PAGE_ERASE_KEY']
        page_write_key = self.config['bootloader']['PAGE_WRITE_KEY']
        page_read_key = self.config['bootloader']['PAGE_READ_KEY']
        byte_write_key = self.config['bootloader']['BYTE_WRITE_KEY']
        operationalHeader = OperationalHeaderFormat(page_erase_key, page_write_key,
                                            byte_write_key, page_read_key)
        return operationalHeader

    def generate_header(self):
        """
        Generate basic header for MCU8 file format
        """
        header = BlockHeaderFormat(self.write_block_size)
        return header

    def generate_metadata_block(self):
        """
        Generate start of image / preamble
        """
        # generate block header
        header = self.generate_header()
        header.set_blocktype(BlockTypeMcu8.METADATA_OPERATION)

        # TODO: I think we could get the image block to work more optimally here.
        NUMBER_OF_DATA_BYTES_IN_HEADER = 1
        metadata = ImageBlock(self.write_block_size - NUMBER_OF_DATA_BYTES_IN_HEADER)

        op_header = self.generate_operational_header()

        header.set_blocklength(header.get_size() + op_header.get_size() + self.write_block_size)
        op_header.set_address(self.config['bootloader']['FLASH_START'])
        # Check if we support required file format version from config file
        config_version = self.config['bootloader']['IMAGE_FORMAT_VERSION']
        logger.info(f'File format versions: Requested {config_version} Supported {self.max_format_version}')
        if not self.is_valid_version(config_version):
            raise ValueError(
                f'Requested format version {config_version} not supported, builder supports versions {self.min_format_version} - {self.max_format_version}' )

        # There is NUMBER_OF_DATA_BYTES_IN_HEADER extra bytes in this header object.
        # The length of the block should be understood taking that into account
        meta_header = (
            header.to_bytes() +
            self.versiontobytes(config_version) +
            self.config['bootloader']['DEVICE_ID'].to_bytes(4, 'little') +
            (self.write_block_size).to_bytes(2, 'little') +
            op_header.address.to_bytes(4, 'little')
        )
        metadata.set_header(meta_header)
        metadata.add_data(op_header.page_erase_key.to_bytes(2, 'little'))
        metadata.add_data(op_header.page_write_key.to_bytes(2, 'little'))
        metadata.add_data(op_header.byte_write_key.to_bytes(2, 'little'))
        metadata.add_data(op_header.page_read_key.to_bytes(2, 'little'))
        metadata.pad_to_data_size(0)

        return metadata

    def generate_operational_block(self, address, data):
        """
        Generates a new operation block

        :param address: Byte address of the segment.
        :param data: Bytearray read from the application input file.
        """
        # Generate block header
        header = self.generate_header()
        header.set_blocktype(BlockTypeMcu8.FLASH_OPERATION)
        # generate operation header
        operationalHeader = self.generate_operational_header()
        operationalHeader.set_address(address)
        header.set_blocklength(header.get_size() + operationalHeader.get_size() + self.write_block_size)
        # Create a new block
        block = ImageBlock(self.write_block_size)
        combined_header = header.to_bytes() + operationalHeader.to_bytes()
        block.set_header(combined_header)
        # Fill the block with data
        bytes_filled = block.fill_to_data_size(data)
        block.mark_empty(data[:(self.write_block_size)].tobytes() == self.empty_block(bytes_filled))
        return block, bytes_filled

class BlockHeaderFormat:
    """
    Standard header:

    3 byte standard header:
    - block length: 2 bytes little endian
    - block type: 1 byte
    """
    def __init__(self, write_block_size):
        self.write_block_size = write_block_size
        self.blocktype = BlockTypeMcu8.UNINITIALIZED
        self.blocklength = 0
        self.header_size = 3

    def set_blocktype(self, blocktype):
        """Set the blocktype in the header"""
        self.blocktype = blocktype

    def set_blocklength(self, blocklength):
        """Set the blocklength in the header"""
        self.blocklength = blocklength

    def get_size(self):
        """Get the length of this block"""
        return self.header_size

    def to_bytes(self):
        """
        Convert header to bytes

        This is where the frame format is generated
        """
        return \
            self.blocklength.to_bytes(2, 'little') + \
            bytes([self.blocktype])

class OperationalHeaderFormat:
    """
    Operation header for MCU8 format:

    12 byte operation header:
    - start address: 4 bytes little endian
    - page erase key: 2 bytes little endian
    - page write key: 2 bytes little endian
    - byte write key: 2 bytes little endian
    - page read key: 2 bytes little endian
    """
    def __init__(self, page_erase_key, page_write_key, byte_write_key, page_read_key):
        self.key_length = 2
        self.address_length = 4
        self.address = 0
        self.page_erase_key = page_erase_key
        self.page_write_key = page_write_key
        self.page_read_key = page_read_key
        self.byte_write_key = byte_write_key

    def get_size(self):
        return ((self.key_length * 4) + (self.address_length))

    def set_address(self, address):
        """Set the address in the header"""
        self.address = address

    def to_bytes(self):
        """
        Convert header to bytes

        This is where the frame format is generated
        """
        return \
            self.address.to_bytes(self.address_length, 'little') + \
            self.page_erase_key.to_bytes(self.key_length, 'little') + \
            self.page_write_key.to_bytes(self.key_length, 'little') + \
            self.byte_write_key.to_bytes(self.key_length, 'little') + \
            self.page_read_key.to_bytes(self.key_length, 'little')
