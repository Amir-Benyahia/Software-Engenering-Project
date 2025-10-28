import math
from array import array
from typing import List
from integer_compressor import IntegerCompressor # On importe notre interface

class BitPackingNonSpanning(IntegerCompressor):
    """
    Implémentation du BitPacking SANS débordement ("non-spanning").
   
    
    Cette classe hérite de IntegerCompressor et implémente ses méthodes.
    Chaque entier compressé est entièrement contenu dans un seul entier 32 bits
    du tableau de sortie.
    """

    def __init__(self):
        # Appelle le constructeur de la classe parent (IntegerCompressor)
        super().__init__()
        # Attribut spécifique à cette classe :
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

        # 1. Trouver le max pour déterminer le nombre de bits
        # (On suppose des entiers positifs pour l'instant, cf. Bonus)
        max_val = max(data) if data else 0

        # 2. Calculer le nombre de bits (k)
        if max_val == 0:
            self.bits_per_element = 1 # Au moins 1 bit
        else:
            # .bit_length() donne le nombre de bits exacts
            self.bits_per_element = max_val.bit_length()
            
        # [DEBUG] print(f"Détecté {self.bits_per_element} bits nécessaires.")

        # 3. Calculer combien d'éléments on peut stocker par int de 32 bits
        # C'est la logique clé de CETTE version "non-spanning"
        self.elements_per_int = 32 // self.bits_per_element
        
        # [DEBUG] print(f"Stockage de {self.elements_per_int} éléments par entier.")


        # 4. Calculer la taille du tableau de sortie
        output_size = math.ceil(self.num_elements / self.elements_per_int)
        # On initialise un tableau de zéros de la bonne taille
        self.compressed_data = array('I', [0] * output_size)

        # 5. Remplir le tableau compressé
        output_index = 0
        bit_offset = 0
        
        # Le masque pour ne garder que les 'k' bits de droite
        # (1 << k) - 1 => ex: k=3 -> 1000 - 1 = 0111
        mask = (1 << self.bits_per_element) - 1

        for i in range(self.num_elements):
            # Si on n'a plus de place dans l'entier 32 bits actuel...
            if bit_offset + self.bits_per_element > 32:
                # ...on passe à l'entier suivant et on repart à zéro
                output_index += 1
                bit_offset = 0

            # On prend la valeur et on la masque
            value = data[i] & mask
            
            # On la décale à sa place et on l'ajoute avec un OU binaire
            self.compressed_data[output_index] |= (value << bit_offset)

            # On décale notre "curseur" de bits pour le prochain nombre
            bit_offset += self.bits_per_element

    def get(self, i: int) -> int:
        """
        Retourne le i-ème entier du tableau d'origine.
       
        """
        if not (0 <= i < self.num_elements):
            raise IndexError(f"Index {i} hors limites (0-{self.num_elements - 1})")

        # 1. Trouver dans quel int du tableau compressé se trouve l'élément
        array_index = i // self.elements_per_int

        # 2. Trouver la position (offset) à l'intérieur de cet int
        index_in_int = i % self.elements_per_int
        bit_offset = index_in_int * self.bits_per_element

        # 3. Extraire la valeur
        # Le masque pour isoler les bits
        mask = (1 << self.bits_per_element) - 1

        # On prend l'entier 32 bits, on déc