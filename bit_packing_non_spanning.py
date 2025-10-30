import math
from array import array
from typing import List
from integer_compressor import IntegerCompressor 

class BitPackingNonSpanning(IntegerCompressor):
    """
    Implémentation du BitPacking SANS débordement ("non-spanning").
    Hérite de IntegerCompressor et implémente ses méthodes.
    """

    def __init__(self) -> None:
        super().__init__()
        self.elements_per_int: int = 0

    def compress(self, data: List[int]) -> None:
        """
        Compresse un tableau d'entiers.
        Le résultat est stocké dans self.compressed_data.
        """
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

        self.elements_per_int = 32 // self.bits_per_element

        output_size = math.ceil(self.num_elements / self.elements_per_int)
        self.compressed_data = array('I', [0] * output_size)

        output_index = 0
        bit_offset = 0
        
        mask = (1 << self.bits_per_element) - 1

        for i in range(self.num_elements):
            if bit_offset + self.bits_per_element > 32:
                output_index += 1
                bit_offset = 0

            value = data[i] & mask
            
            self.compressed_data[output_index] |= (value << bit_offset)

            bit_offset += self.bits_per_element

    def get(self, i: int) -> int:
        """
        Retourne le i-ème entier du tableau d'origine.
        """
        if not (0 <= i < self.num_elements):
            raise IndexError(f"Index {i} hors limites (0-{self.num_elements - 1})")

        array_index = i // self.elements_per_int
        index_in_int = i % self.elements_per_int
        bit_offset = index_in_int * self.bits_per_element

        mask = (1 << self.bits_per_element) - 1
        value = (self.compressed_data[array_index] >> bit_offset) & mask
        
        return value

    def decompress(self) -> List[int]:
        """
        Décompresse les données stockées en interne.
        """
        return [self.get(i) for i in range(self.num_elements)]