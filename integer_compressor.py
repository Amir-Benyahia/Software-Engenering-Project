import abc
from array import array
from typing import List

class IntegerCompressor(abc.ABC):
    """
    Interface (Classe de Base Abstraite) pour les compresseurs d'entiers.
    
    Elle définit les méthodes obligatoires (compress, decompress, get)
    que chaque classe de compression concrète devra implémenter.
    
    Elle gère aussi les attributs communs.
    """

    def __init__(self) -> None:
        """
        Initialise les attributs communs à tous les compresseurs.
        """
        # 'I' signifie "unsigned int" (entier non signé 32 bits).
        self.compressed_data: array = array('I') 
        self.num_elements: int = 0
        self.bits_per_element: int = 0

    @abc.abstractmethod
    def compress(self, data: List[int]) -> None:
        """
        Méthode abstraite.
        Compresse une liste d'entiers.
        Le résultat doit être stocké dans self.compressed_data.
        """
        pass

    @abc.abstractmethod
    def decompress(self) -> List[int]:
        """
        Méthode abstraite.
        Décompresse les données de self.compressed_data.
        Retourne une nouvelle liste contenant les entiers d'origine.
        """
        pass

    @abc.abstractmethod
    def get(self, i: int) -> int:
        """
        Méthode abstraite.
        Retourne le i-ème entier du tableau d'origine (non compressé)
        en y accédant directement depuis self.compressed_data.
        """
        pass

    def get_compressed_size_in_bytes(self) -> int:
        """
        Retourne la taille en octets des données compressées.
        """
        if not self.compressed_data:
            return 0
        return self.compressed_data.itemsize * len(self.compressed_data)