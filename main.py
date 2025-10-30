from compressor_factory import CompressorFactory, COMPRESSOR_SPANNING, COMPRESSOR_NON_SPANNING, COMPRESSOR_OVERFLOW
import sys
from typing import List

def test_compression(compressor_name: str, data: List[int], **kwargs) -> None:
    """
    Une fonction simple pour tester un type de compresseur.
    """
    print("-" * 40)
    print(f"TEST DU COMPRESSEUR : '{compressor_name}'")
    print(f"Données d'origine ({len(data)} éléments): {data}")

    try:
        compressor = CompressorFactory.create_compressor(compressor_name, **kwargs)
        compressor.compress(data)
        decompressed_data = compressor.decompress()
        
        print(f"Données décompressées: {decompressed_data}")

        if data == decompressed_data:
            print("✅ SUCCÈS : Les données sont identiques.")
        else:
            print("❌ ÉCHEC : Les données sont différentes !")
            
        index_to_test = len(data) // 2
        original_val = data[index_to_test]
        get_val = compressor.get(index_to_test)
        
        print(f"Test de get({index_to_test}): Orig={original_val}, Get={get_val}")
        if original_val == get_val:
            print("✅ SUCCÈS : get() fonctionne.")
        else:
            print("❌ ÉCHEC : get() ne fonctionne pas !")
            
        original_size = len(data) * 4
        compressed_size = compressor.get_compressed_size_in_bytes()
        print(f"Taille originale (estimée): {original_size} octets")
        print(f"Taille compressée: {compressed_size} octets")
        
    except Exception as e:
        print(f"💥 ERREUR lors du test de '{compressor_name}': {e}")
        sys.exit(1)
    
    print("-" * 40)


if __name__ == "__main__":
    
    print("===== DÉBUT DU TEST DE COMPRESSION =====")
    
    test_data_simple: List[int] = [1, 2, 3, 4, 5, 6, 7, 0, 1, 3]
    test_data_medium: List[int] = [100, 2000, 4095, 0, 1234, 567]
    test_data_overflow: List[int] = [1, 2, 3, 1024, 4, 5, 2048]
    
    test_compression(COMPRESSOR_NON_SPANNING, test_data_simple)
    test_compression(COMPRESSOR_NON_SPANNING, test_data_medium)
    
    test_compression(COMPRESSOR_SPANNING, test_data_simple)
    test_compression(COMPRESSOR_SPANNING, test_data_medium)
    
    print("\n===== TEST DE LA ZONE DE DÉBORDEMENT =====")
    test_compression(COMPRESSOR_OVERFLOW, test_data_overflow, main_bits=3)

    print("\n===== FIN DU TEST DE COMPRESSION =====")