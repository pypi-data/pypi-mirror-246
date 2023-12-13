class FirmwareImageBuilder:
    """
    Base class - Class to house common and repeated code between all image builders.
    """
    def __init__(self, config):
        self.config = config
        self.write_block_size = self.config['bootloader']['WRITE_BLOCK_SIZE']