import math
from array import array
from typing import List, Tuple
from integer_compressor import IntegerCompressor
from bit_packing_spanning import BitPackingSpanning 

# This is the "overflow" version
# I used the "Decorator" design pattern
# to wrap around the BitPackingSpanning compressor
class BitPackingOverflow(IntegerCompressor):

    def __init__(self, main_bits: int) -> None:
        super().__init__()
        
        # The wrapped compressor
        self.wrapped_compressor: IntegerCompressor = BitPackingSpanning()
        
        # Number of bits for the main area (k')
        self.main_bits: int = main_bits
        
        # The sentinel value
        # Values >= this will go to the overflow area
        self.overflow_sentinel: int = (1 << main_bits) - 1
        
        # Array to store the "big" numbers
        self.overflow_area: array = array('I')

    def compress(self, data: List[int]) -> None:
        if not data:
            self.num_elements = 0
            self.compressed_data = array('I')
            return

        self.num_elements = len(data)
        
        # 1 - Split the data into two lists
        main_data: List[int] = []
        overflow_list: List[int] = []
        
        for val in data:
            if val < self.overflow_sentinel:
                # Normal value
                main_data.append(val)
            else:
                # Overflow value
                main_data.append(self.overflow_sentinel) # Write sentinel
                overflow_list.append(val)                # Store real value
        
        # 2 - Compress the main data
        # Use the wrapped compressor
        fake_max_val_data = list(main_data)
        fake_max_val_data.append(self.overflow_sentinel - 1)
        
        self.wrapped_compressor.compress(fake_max_val_data)
        
        # 3 - Store the results
        self.compressed_data = self.wrapped_compressor.compressed_data
        self.overflow_area = array('I', overflow_list)
        self.bits_per_element = self.wrapped_compressor.bits_per_element


    def get(self, i: int) -> int:
        if not (0 <= i < self.num_elements):
            raise IndexError(f"Index {i} is out of bounds")

        # 1 - Get the value from the main compressed data
        value = self.wrapped_compressor.get(i)
        
        # 2 - Check if it's a sentinel
        if value == self.overflow_sentinel:
            overflow_index = 0
            for j in range(i):
                if self.wrapped_compressor.get(j) == self.overflow_sentinel:
                    overflow_index += 1
            
            # This count is the index in the overflow_area
            return self.overflow_area[overflow_index]
        else:
            # 3 - Otherwise, it's a normal value
            return value

    def decompress(self) -> List[int]:
        decompressed_list: List[int] = []
        
        # Simple loop calling get()
        for i in range(self.num_elements):
            value = self.get(i)
            decompressed_list.append(value)
                
        return decompressed_list

    def get_compressed_size_in_bytes(self) -> int:
        # Get the total size main + overflow
        main_size = self.wrapped_compressor.get_compressed_size_in_bytes()
        overflow_size = self.overflow_area.itemsize * len(self.overflow_area)
        return main_size + overflow_size