"""
Image Utilities
"""
from logging import getLogger
from binascii import hexlify
from hexdump2 import hexdump

class ImageBlock:
    """
    Construct for generic 'block'

    Consists of header + data, with helpers for populating
    """
    def __init__ (self, data_size):
        self.data_size = data_size
        self.header = None
        self.data = bytes()
        self.empty = False

    def set_header(self, header):
        """ Set the header elements directly """
        self.header = header

    def set_data (self, data):
        """ Set the data elements directly """
        self.data = data

    def add_data(self, data):
        """ Append to data elements """
        self.data += data

    def fill_to_data_size(self, data):
        """
        Fill up with data elements until the pre-determined size

        Returns how many elements fitted in
        """
        self.data = data[0:self.data_size]
        return self.data_size

    def pad_to_data_size(self, value):
        """ Fill up with padding data elements until the pre-determined size """
        while len(self.data) < self.data_size:
            self.data += value.to_bytes(1, 'little')

    def to_bytes(self):
        """ Convert to byte array """
        return self.header + self.data

    def mark_empty(self, empty=True):
        """
        Mark or unmark block as empty (containing no programmable data).
        """
        self.empty = empty

    def is_empty(self):
        return self.empty


class FirmwareImage:
    """
    Firmware image helper

    Consists of an array of blocks as objects
    """
    def __init__(self):
        self.logger = getLogger(__name__)
        self.blocks = []

    def add_block(self, block):
        """ Add a block to the image """
        self.blocks.append(block)

    def __str__(self):
        """ Human readable output for printing """
        self.logger.debug("%d blocks in image", len(self.blocks))
        readable = ''
        for block in self.blocks:
            readable += hexlify(block.to_bytes()).decode().upper()
        return readable

    def _flatten_data(self):
        """ Convert list of blocks to one large block """
        flatdata = bytes()
        for block in self.blocks:
            flatdata += block.to_bytes()
        return flatdata

    def save(self, filename):
        """ Save the image to file """
        with open(filename, "wb") as file:
            file.write(self._flatten_data())

    def dump(self, filename):
        """ Save image dump in human readable form"""
        with open(filename, "w") as file:
            print(hexdump(self._flatten_data(), result='return'), file=file)
