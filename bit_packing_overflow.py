import math
from array import array
from typing import List, Tuple
from integer_compressor import IntegerCompressor
from bit_packing_spanning import BitPackingSpanning # On décore le Spanning

class BitPackingOverflow(IntegerCompressor):
    """
    Implémentation du BitPacking AVEC zone de débordement.
    
    Ceci est un Design Pattern "Décorateur". Il "enveloppe"
    un autre compresseur (ici, BitPackingSpanning) pour lui
    ajouter une fonctionnalité.
    
    Il va compresser la plupart des nombres avec k' bits, et
    stocker les nombres trop grands dans une zone séparée.
    """

    def __init__(self, main_bits: int):
        """
        Initialise le décorateur.
        
        Args:
            main_bits: Le nombre de bits (k') à utiliser pour
                       la compression principale.
        """
        super().__init__()
        
        # Le compresseur qu'on "décore"
        # Il gérera la compression principale
        self.wrapped_compressor = BitPackingSpanning()
        
        # k' : le nombre de bits pour les données principales
        self.main_bits = main_bits
        
        # Valeur spéciale qui signifie "chercher dans l'overflow"
        # On utilise la valeur max possible sur k' bits
        self.overflow_sentinel = (1 << main_bits) - 1
        
        # La zone de débordement
        self.overflow_area = array('I') # Tableau 32 bits non signé

    def compress(self, data: List[int]) -> None:
        if not data:
            self.num_elements = 0
            self.compressed_data = array('I')
            return

        self.num_elements = len(data)
        
        # 1. Séparer les données en deux listes
        main_data = []
        overflow_list = []
        
        for val in data:
            if val < self.overflow_sentinel:
                # Ce nombre est "normal", on le garde
                main_data.append(val)
            else:
                # Ce nombre est trop grand
                # On met la valeur "sentinelle" dans les données principales
                main_data.append(self.overflow_sentinel)
                # Et on stocke la vraie valeur dans la liste d'overflow
                overflow_list.append(val)
        
        # 2. Compresser les données principales
        # On force notre compresseur interne à utiliser k' bits
        # (Petite astuce : on lui donne un 'max_val' qui force k' bits)
        fake_max_val_data = list(main_data)
        fake_max_val_data.append(self.overflow_sentinel - 1) # Assure k' bits
        
        self.wrapped_compressor.compress(fake_max_val_data)
        
        # 3. Stocker les données compressées et la zone d'overflow
        self.compressed_data = self.wrapped_compressor.compressed_data
        self.overflow_area = array('I', overflow_list)
        
        # 4. Mettre à jour les attributs (ils sont utilisés par get/decompress)
        self.bits_per_element = self.wrapped_compressor.bits_per_element
        
        # [DEBUG] print(f"Overflow: k'={self.main_bits}, Sentinelle={self.overflow_sentinel}")
        # [DEBUG] print(f"Overflow: Données principales: {main_data}")
        # [DEBUG] print(f"Overflow: Zone de débordement: {overflow_list}")


    def get(self, i: int) -> int:
        if not (0 <= i < self.num_elements):
            raise IndexError(f"Index {i} hors limites (0-{self.num_elements - 1})")

        # 1. Récupérer la valeur depuis le compresseur principal
        # C'est la magie du décorateur : on réutilise le 'get' du Spanning
        value = self.wrapped_compressor.get(i)
        
        if value == self.overflow_sentinel:
            # 2. Si c'est la sentinelle, il faut chercher dans l'overflow
            # On doit compter combien de "sentinelles" on a vues avant l'index 'i'
            
            overflow_index = 0
            for j in range(i):
                if self.wrapped_compressor.get(j) == self.overflow_sentinel:
                    overflow_index += 1
                    
            # Cet index correspond à la position dans notre overflow_area
            return self.overflow_area[overflow_index]
        else:
            # 3. Sinon, c'est la bonne valeur
            return value

    def decompress(self) -> List[int]:
        """
        Décompresse les données en combinant les données principales
        et la zone de débordement.
        """
        decompressed_list = []
        overflow_index = 0
        
        for i in range(self.num_elements):
            # On appelle le 'get' du compresseur principal
            value = self.wrapped_compressor.get(i)
            
            if value == self.overflow_sentinel:
                # C'est une valeur de l'overflow
                decompressed_list.append(self.overflow_area[overflow_index])
                overflow_index += 1
            else:
                # C'est une valeur normale
                decompressed_list.append(value)
                
        return decompressed_list

    def get_compressed_size_in_bytes(self) -> int:
        """
        Surcharge la méthode pour inclure la taille de l'overflow.
        """
        main_size = self.wrapped_compressor.get_compressed_size_in_bytes()
        overflow_size = self.overflow_area.itemsize * len(self.overflow_area)
        return main_size + overflow_size