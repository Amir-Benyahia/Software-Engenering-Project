from compressor_factory import CompressorFactory, COMPRESSOR_SPANNING, COMPRESSOR_NON_SPANNING
import sys # Pour quitter en cas d'erreur

def test_compression(compressor_name: str, data: list):
    """
    Une fonction simple pour tester un type de compresseur.
    """
    print("-" * 40)
    print(f"TEST DU COMPRESSEUR : '{compressor_name}'")
    print(f"Données d'origine ({len(data)} éléments): {data}")

    try:
        # 1. Créer le compresseur via la Factory
        compressor = CompressorFactory.create_compressor(compressor_name)
        
        # 2. Compresser les données
        compressor.compress(data)
        
        # 3. Récupérer les données décompressées
        decompressed_data = compressor.decompress()
        
        print(f"Données décompressées: {decompressed_data}")

        # 4. Vérifier si c'est correct
        if data == decompressed_data:
            print("✅ SUCCÈS : Les données sont identiques.")
        else:
            print("❌ ÉCHEC : Les données sont différentes !")
            
        # 5. Tester l'accès direct (la fonction get())
        index_to_test = len(data) // 2 # On prend un index au milieu
        original_val = data[index_to_test]
        get_val = compressor.get(index_to_test)
        
        print(f"Test de get({index_to_test}): Orig={original_val}, Get={get_val}")
        if original_val == get_val:
            print("✅ SUCCÈS : get() fonctionne.")
        else:
            print("❌ ÉCHEC : get() ne fonctionne pas !")
            
        # 6. Afficher l'efficacité
        original_size = len(data) * 4 # 4 octets par int (estimation)
        compressed_size = compressor.get_compressed_size_in_bytes()
        print(f"Taille originale (estimée): {original_size} octets")
        print(f"Taille compressée: {compressed_size} octets")
        
    except Exception as e:
        print(f"💥 ERREUR lors du test de '{compressor_name}': {e}")
        sys.exit(1) # Quitte le programme en cas d'erreur
    
    print("-" * 40)


# --- POINT D'ENTRÉE PRINCIPAL DU PROGRAMME ---
if __name__ == "__main__":
    
    print("===== DÉBUT DU TEST DE COMPRESSION =====")
    
    # Données de test simples (pour k=3 bits)
    # 1, 2, 3, 4, 5
    test_data_simple = [1, 2, 3, 4, 5, 6, 7, 0, 1, 3]
    
    # Données avec des nombres plus grands (pour k=12 bits)
    # L'exemple du sujet (12 bits)
    test_data_medium = [100, 2000, 4095, 0, 1234, 567]
    
    # Teste le premier compresseur
    test_compression(COMPRESSOR_NON_SPANNING, test_data_simple)
    test_compression(COMPRESSOR_NON_SPANNING, test_data_medium)
    
    # Teste le second compresseur
    test_compression(COMPRESSOR_SPANNING, test_data_simple)
    test_compression(COMPRESSOR_SPANNING, test_data_medium)

    print("\n===== FIN DU TEST DE COMPRESSION =====")