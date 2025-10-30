from integer_compressor import IntegerCompressor
from bit_packing_non_spanning import BitPackingNonSpanning
from bit_packing_spanning import BitPackingSpanning
from bit_packing_overflow import BitPackingOverflow

COMPRESSOR_NON_SPANNING = "non_spanning"
COMPRESSOR_SPANNING = "spanning"
COMPRESSOR_OVERFLOW = "overflow"


class CompressorFactory:
    """
    Design Pattern Factory (Fabrique).
    Centralise la création des différents types de compresseurs.
    """

    @staticmethod
    def create_compressor(compressor_type: str, **kwargs) -> IntegerCompressor:
        """
        Crée et retourne une instance du compresseur demandé.
        
        Args:
            compressor_type: Le nom du compresseur (ex: "spanning").
            **kwargs: Arguments optionnels (ex: main_bits=8).
        
        Returns:
            Une instance d'un objet qui hérite de IntegerCompressor.
        
        Raises:
            ValueError: Si le type de compresseur est inconnu.
        """
        
        if compressor_type == COMPRESSOR_NON_SPANNING:
            return BitPackingNonSpanning()
            
        elif compressor_type == COMPRESSOR_SPANNING:
            return BitPackingSpanning()
            
        elif compressor_type == COMPRESSOR_OVERFLOW:
            main_bits: int = kwargs.get("main_bits", 8) 
            return BitPackingOverflow(main_bits=main_bits)
            
        else:
            raise ValueError(f"Type de compresseur inconnu : '{compressor_type}'")