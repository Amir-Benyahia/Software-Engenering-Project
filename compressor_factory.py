from integer_compressor import IntegerCompressor
from bit_packing_non_spanning import BitPackingNonSpanning
from bit_packing_spanning import BitPackingSpanning
from bit_packing_overflow import BitPackingOverflow

# Constants to avoid typos
COMPRESSOR_NON_SPANNING = "non_spanning"
COMPRESSOR_SPANNING = "spanning"
COMPRESSOR_OVERFLOW = "overflow"

# This is the "Factory" pattern
# It creates the compressor objects for us
# This way main.py doesn't need to know the class names
class CompressorFactory:

    @staticmethod
    def create_compressor(compressor_type: str, **kwargs) -> IntegerCompressor:
        
        if compressor_type == COMPRESSOR_NON_SPANNING:
            return BitPackingNonSpanning()
            
        elif compressor_type == COMPRESSOR_SPANNING:
            return BitPackingSpanning()
            
        elif compressor_type == COMPRESSOR_OVERFLOW:
            # Get the 'main_bits' argument
            # Default to 8 bits if not provided
            main_bits: int = kwargs.get("main_bits", 8) 
            return BitPackingOverflow(main_bits=main_bits)
            
        else:
            raise ValueError(f"Unknown compressor type: '{compressor_type}'")