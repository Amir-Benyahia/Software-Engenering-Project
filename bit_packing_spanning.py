import math
from array import array
from typing import List
from integer_compressor import IntegerCompressor # On importe encore notre interface

class BitPackingSpanning(IntegerCompressor):
    """
    Implémentation du BitPacking AVEC débordement ("spanning").
    
    Les entiers compressés sont écrits bit à bit et peuvent s'étaler
    sur deux entiers (32 bits) consécutifs du tableau de sortie.
    C'est plus efficace en espace que la version NonSpanning.
    """

    def __init__(self):
        # Appelle le constructeur de la classe parent
        super().__init__()
        # Pas d'attributs spécifiques, tout est géré par les 3 attributs de base

    def compress(self, data: List[int]) -> None:
        """
        Compresse un tableau d'entiers en permettant le débordement.
        """
        if not data:
            self.num_elements = 0
            self.compressed_data = array('I')
            return
        
        self.num_elements = len(data)

        # 1. Trouver le max
        max_val = max(data) if data else 0

        # 2. Calculer le nombre de bits (k)
        if max_val == 0:
            self.bits_per_element = 1
        else:
            self.bits_per_element = max_val.bit_length()
        
        # 3. Calculer la taille du tableau de sortie
        total_bits = self.num_elements * self.bits_per_element
        output_size = math.ceil(total_bits / 32)
        if output_size == 0 and self.num_elements > 0:
             output_size = 1

        self.compressed_data = array('I', [0] * output_size)

        # 4. Remplir le tableau compressé
        bit_cursor = 0  # Pointeur de bit global
        mask_k_bits = (1 << self.bits_per_element) - 1
        
        # Masque 32 bits pour tronquer les grands nombres
        mask_32_bits = 0xFFFFFFFF 

        for val in data:
            array_index = bit_cursor // 32
            bit_offset = bit_cursor % 32
            
            value = val & mask_k_bits

            # --- Partie 1: Écrire les bits dans le premier int ---
            
            # === C'EST LA LIGNE CORRIGÉE ===
            # On décale la valeur, ET ON MASQUE à 32 bits
            self.compressed_data[array_index] |= ((value << bit_offset) & mask_32_bits)
            # ==============================

            # --- Partie 2: Vérifier si ça déborde (span) ---
            bits_written = 32 - bit_offset
            if bits_written < self.bits_per_element:
                bits_to_wrap = self.bits_per_element - bits_written
                
                if array_index + 1 < len(self.compressed_data):
                    wrapped_value = value >> bits_written
                    self.compressed_data[array_index + 1] |= wrapped_value
            
            bit_cursor += self.bits_per_element

    def get(self, i: int) -> int:
        """
        Retourne le i-ème entier, en gérant le cas "spanning".
        """
        if not (0 <= i < self.num_elements):
            raise IndexError(f"Index {i} hors limites (0-{self.num_elements - 1})")

        # 1. Calculer la position de début en bits
        bit_cursor = i * self.bits_per_element
        
        array_index = bit_cursor // 32
        bit_offset = bit_cursor % 32

        # 2. Créer le masque pour nos k bits
        mask = (1 << self.bits_per_element) - 1

        # 3. Lire la première partie
        value = self.compressed_data[array_index] >> bit_offset

        # 4. Vérifier si on doit lire la seconde partie (sur l'entier suivant)
        bits_read = 32 - bit_offset
        if bits_read < self.bits_per_element:
            bits_to_read_wrap = self.bits_per_element - bits_read
            
            if array_index + 1 < len(self.compressed_data):
                wrap_mask = (1 << bits_to_read_wrap) - 1
                wrapped_value = self.compressed_data[array_index + 1] & wrap_mask
                value |= (wrapped_value << bits_read)

        # 5. Masquer le résultat final pour ne garder que k bits
        return value & mask

    def decompress(self) -> List[int]:
        """
        Décompresse les données stockées en interne.
        """
        return [self.get(i) for i in range(self.num_elements)]