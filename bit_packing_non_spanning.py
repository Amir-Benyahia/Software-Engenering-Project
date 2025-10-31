import math
from array import array
from typing import List
from integer_compressor import IntegerCompressor 

# This is the "non-spanning" version
# Compressed ints do not span across two 32-bit ints.
class BitPackingNonSpanning(IntegerCompressor):

    def __init__(self) -> None:
        super().__init__()
        # How many elements we can fit in one 32-bit int
        self.elements_per_int: int = 0

    def compress(self, data: List[int]) -> None:
        if not data:
            self.num_elements = 0
            self.compressed_data = array('I')
            return

        self.num_elements = len(data)

        # 1 - Find max value to determine k
        max_val = max(data) if data else 0

        # 2 - Calculate k (bits_per_element)
        if max_val == 0:
            self.bits_per_element = 1 
        else:
            self.bits_per_element = max_val.bit_length() 

        # 3 - How many elements per 32-bit int?
        # This is the main logic for "non-spanning" 
        self.elements_per_int = 32 // self.bits_per_element # ex: 32 // 3 = 10 elements

        # 4 - Size of the output array
        output_size = math.ceil(self.num_elements / self.elements_per_int)
        self.compressed_data = array('I', [0] * output_size) 

        # 5 - Fill the array
        output_index = 0
        bit_offset = 0
        
        # Mask to keep only k bits
        mask = (1 << self.bits_per_element) - 1

        for i in range(self.num_elements):
            # Check if we need to move to the next 32-bit int
            if bit_offset + self.bits_per_element > 32:
                # Move to next int
                output_index += 1
                bit_offset = 0

            # Get value and mask it
            value = data[i] & mask
            
            # Shift it to its position and add it with a bitwise OR
            self.compressed_data[output_index] |= (value << bit_offset)

            # Move the bit "cursor" for the next number
            bit_offset += self.bits_per_element

    def get(self, i: int) -> int:
        if not (0 <= i < self.num_elements):
            raise IndexError(f"Index {i} is out of bounds")

        # 1 - Find the index in the compressed array
        array_index = i // self.elements_per_int

        # 2 - Find the offset inside that 32-bit int
        index_in_int = i % self.elements_per_int
        bit_offset = index_in_int * self.bits_per_element

        # 3 - Extract the value
        mask = (1 << self.bits_per_element) - 1
        # Shift all the way to the right, then mask
        value = (self.compressed_data[array_index] >> bit_offset) & mask
        
        return value

    def decompress(self) -> List[int]:
        # Just loop and call get() for each element
        return [self.get(i) for i in range(self.num_elements)]