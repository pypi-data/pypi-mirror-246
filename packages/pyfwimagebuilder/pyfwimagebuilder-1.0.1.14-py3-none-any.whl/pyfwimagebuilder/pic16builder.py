"""
Firmware Builder functions for PIC16
"""
from .imageutils import ImageBlock
from .mcu8builder import FirmwareImageBuilderMcu8, BlockTypeMcu8

class FirmwareImagebuilderPic16 (FirmwareImageBuilderMcu8):
    """
    Image Builder functions for PIC16
    """
    def __init__(self, config):
        """
        Override Initialization
        """
        super().__init__(config)
        # Convert the default values to support PIC16
        self.UNDEFINED_SEQUENCE = 0x3FFF
        self.UNDEFINED_SEQUENCE_BYTE_LENGTH = 2
        self.write_block_size = self.write_block_size * 2

    def empty_block(self, size):
        """
        Override:
        Return platform-specific empty byte pattern block with given size in bytes
        For PIC16, empty block is filled with 0x3fff *words*.
        Keyword arguments:
            size -- the byte size of the block
        """
        if size != self.write_block_size:
            # PIC16 devices can only write complete blocks. If the length is not exact do not include it.
            # TODO - Consider erroring out here instead of silent exclusion.
            #       An error here would probably be due to programmer error for PIC16 devices
            return False
        else:
            return int(size/2) * self.UNDEFINED_SEQUENCE.to_bytes(self.UNDEFINED_SEQUENCE_BYTE_LENGTH, 'little')

    def include_segment(self, address):
        """
        Override:
        Returns true if the segment must be included. 

        Note: PIC16 variant needs to multiple the configured address by
        2 in order to correct the byte vs. word differences.
        """
        if (address >= (self.config['bootloader']['FLASH_END'] * 2) or
            address < (self.config['bootloader']['FLASH_START'] * 2)):
            return False
        return True

    def generate_operational_block(self, address, data):
        """
        Override:
        Generates a new block

        :param address: Byte address of a block
        """
        header = self.generate_header()
        # TODO: Evaluate the address here and use the proper operational block type for the variant
        header.set_blocktype(BlockTypeMcu8.FLASH_OPERATION)

        # generate operation header
        operationalHeader = self.generate_operational_header()
        operationalHeader.set_address(int(address/2))

        # Create a new block
        header.set_blocklength(header.get_size() + operationalHeader.get_size() + self.write_block_size)
        block = ImageBlock(self.write_block_size)
        combined_header = header.to_bytes() + operationalHeader.to_bytes()
        block.set_header(combined_header)

        # Fill the block with data
        bytes_filled = block.fill_to_data_size(data)
        block.mark_empty(data[:(self.write_block_size)].tobytes() == self.empty_block(bytes_filled))

        return block, bytes_filled