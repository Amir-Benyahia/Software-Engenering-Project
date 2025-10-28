from integer_compressor import IntegerCompressor
from bit_packing_non_spanning import BitPackingNonSpanning
from bit_packing_spanning import BitPackingSpanning
# On importera bit_packing_overflow ici plus tard
# from bit_packing_overflow import BitPackingOverflow

# On peut définir des constantes pour les noms, c'est une bonne pratique
# pour éviter les fautes de frappe.
COMPRESSOR_NON_SPANNING = "non_spanning"
COMPRESSOR_SPANNING = "spanning"
COMPRESSOR_OVERFLOW = "overflow"


class CompressorFactory:
    """
    Design Pattern Factory (Fabrique).
    
    Cette classe centralise la création des différents types
    de compresseurs. Le code "client" (main.py) n'a plus besoin
    de connaître les noms des classes concrètes, il lui suffit
    de demander un type par son nom (string).
    
    Cela respecte le principe Ouvert/Fermé (SOLID)[cite: 815, 822]:
    on peut ajouter de nouveaux compresseurs (comme "overflow")
    sans modifier le code qui UTILISE la factory.
    """

    @staticmethod
    def create_compressor(compressor_type: str) -> IntegerCompressor:
        """
        Crée et retourne une instance du compresseur demandé.
        
        Args:
            compressor_type: Le nom du compresseur (ex: "spanning").
        
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
            # On le prépare pour plus tard
            # return BitPackingOverflow()
            raise NotImplementedError("Le compresseur 'overflow' n'est pas encore implémenté.")
            
        else:
            raise ValueError(f"Type de compresseur inconnu : '{compressor_type}'")