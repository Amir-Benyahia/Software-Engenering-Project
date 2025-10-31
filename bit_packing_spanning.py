import math
from array import array
from typing import List
from integer_compressor import IntegerCompressor

# This is the "spanning" version
# Ints can be written across two 32-bit blocks
class BitPackingSpanning(IntegerCompressor):

    def __init__(self) -> None:
        super().__init__()

    def compress(self, data: List[int]) -> None:
        if not data:
            self.num_elements = 0
            self.compressed_data = array('I')
            return
        
        self.num_elements = len(data)

        max_val = max(data) if data else 0

        if max_val == 0:
            self.bits_per_element = 1
        else:
            self.bits_per_element = max_val.bit_length()
        
        # Total bits needed
        total_bits = self.num_elements * self.bits_per_element
        output_size = math.ceil(total_bits / 32)
        if output_size == 0 and self.num_elements > 0:
             output_size = 1 # At least one int if we have data

        self.compressed_data = array('I', [0] * output_size)

        bit_cursor = 0 # Global bit position
        mask_k_bits = (1 << self.bits_per_element) - 1 
        
        # This is needed because Python's integers are not limited
        # to 32 bits, which would crash the array('I')
        mask_32_bits = 0xFFFFFFFF 

        for val in data:
            array_index = bit_cursor // 32 # Which 32-bit int
            bit_offset = bit_cursor % 32   # Offset inside that int
            
            value = val & mask_k_bits

            # Part 1: Write the first part
            # Shift value and mask to 32 bits
            self.compressed_data[array_index] |= ((value << bit_offset) & mask_32_bits)

            # Part 2: Check if we need to write to the next int
            bits_written = 32 - bit_offset
            if bits_written < self.bits_per_element:
                # The number didn't fit
                if array_index + 1 < len(self.compressed_data):
                    # Calculate the wrapped part
                    wrapped_value = value >> bits_written
                    # Write to the next int
                    self.compressed_data[array_index + 1] |= wrapped_value
            
            # Move the global cursor
            bit_cursor += self.bits_per_element

    def get(self, i: int) -> int:
        if not (0 <= i < self.num_elements):
            raise IndexError(f"Index {i} is out of bounds")

        # 1 - Find the global bit position
        bit_cursor = i * self.bits_per_element
        array_index = bit_cursor // 32
        bit_offset = bit_cursor % 32

        mask = (1 << self.bits_per_element) - 1

        # 2 - Read the first part
        value = self.compressed_data[array_index] >> bit_offset

        # 3 - Check if we need to read from the next int
        bits_read = 32 - bit_offset
        if bits_read < self.bits_per_element:
            bits_to_read_wrap = self.bits_per_element - bits_read
            
            if array_index + 1 < len(self.compressed_data):
                # Read the wrapped part
                wrap_mask = (1 << bits_to_read_wrap) - 1
                wrapped_value = self.compressed_data[array_index + 1] & wrap_mask
                
                # Combine the two parts
                value |= (wrapped_value << bits_read)

        # 4 - Mask the final result to get only k bits
        return value & mask

    def decompress(self) -> List[int]:
        # Simple loop calling get()
        return [self.get(i) for i in range(self.num_elements)]