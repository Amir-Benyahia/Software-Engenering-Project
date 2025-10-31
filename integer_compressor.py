import abc
from array import array
from typing import List

# This is the "interface" for all integer compressors
# All my compressors must implement these methods
class IntegerCompressor(abc.ABC):

    def __init__(self) -> None:
        """
        Init the shared attributes.
        """
        # 'I' = unsigned int (32 bits)
        # This is to simulate the 32-bit int from the project subject
        self.compressed_data: array = array('I') 
        self.num_elements: int = 0
        self.bits_per_element: int = 0 # This is 'k'

    @abc.abstractmethod
    def compress(self, data: List[int]) -> None:
        # Child classes MUST implement this
        pass

    @abc.abstractmethod
    def decompress(self) -> List[int]:
        # Child classes MUST implement this
        pass

    @abc.abstractmethod
    def get(self, i: int) -> int:
        # Child classes MUST implement this
        pass

    def get_compressed_size_in_bytes(self) -> int:
        # Get the size of the compressed data in bytes
        if not self.compressed_data:
            return 0
        # .itemsize is the size of one 'I' (4 bytes)
        return self.compressed_data.itemsize * len(self.compressed_data)