import timeit
import random
from compressor_factory import CompressorFactory, COMPRESSOR_SPANNING, COMPRESSOR_NON_SPANNING, COMPRESSOR_OVERFLOW
from integer_compressor import IntegerCompressor
from typing import List

def setup_compressor(compressor_name: str, data: List[int], **kwargs) -> IntegerCompressor:
    """
    Fonction de "setup" pour le benchmark.
    Crée le compresseur et compresse les données.
    On ne veut pas mesurer ça, on veut mesurer get() et decompress().
    """
    compressor = CompressorFactory.create_compressor(compressor_name, **kwargs)
    compressor.compress(data)
    return compressor

def run_benchmark():
    """
    Exécute les benchmarks pour les différentes fonctions.
    """
    print("===== DÉBUT DU BENCHMARK =====")
    print("Protocole : Nous utilisons 'timeit' pour exécuter chaque fonction 100 fois.")
    print("Ceci permet d'obtenir une moyenne fiable et d'ignorer les bruits système.")
    print("Nous testons sur un jeu de données de 10 000 entiers.")
    print("-" * 50)

    # 1. Préparer les données de test
    k_prime = 10
    max_normal = (1 << k_prime) - 1
    data_size = 10000
    test_data = []
    for _ in range(data_size):
        if random.random() < 0.05: # 5% de chance
            test_data.append(random.randint(max_normal, max_normal * 10))
        else:
            test_data.append(random.randint(0, max_normal - 1))

    print(f"Jeu de données créé : {data_size} entiers, k'={k_prime} bits.\n")
    
    compressors = {}
    
    # === LA CORRECTION EST ICI ===
    # On crée un dictionnaire qui contient TOUTES les variables
    # (globales ET locales)
    benchmark_context = globals().copy()
    benchmark_context.update(locals())
    # ============================
    
    # --- 2. Benchmark de la fonction compress() ---
    print(f"--- Mesure du temps de compress() [10 exécutions] ---")
    
    setup_code_spanning_compress = "compressor = CompressorFactory.create_compressor(COMPRESSOR_SPANNING)"
    
    time_spanning_compress = timeit.timeit(
        stmt="compressor.compress(test_data)", 
        setup=setup_code_spanning_compress, 
        globals=benchmark_context, # On utilise notre nouveau contexte
        number=10
    ) / 10
    print(f"  {COMPRESSOR_SPANNING:<15}: {time_spanning_compress:.6f} secondes (moyenne sur 10)")
    
    compressors[COMPRESSOR_SPANNING] = setup_compressor(COMPRESSOR_SPANNING, test_data)

    # --- Test de l'Overflow ---
    setup_code_overflow_compress = "compressor = CompressorFactory.create_compressor(COMPRESSOR_OVERFLOW, main_bits=k_prime)"
    time_overflow_compress = timeit.timeit(
        stmt="compressor.compress(test_data)", 
        setup=setup_code_overflow_compress, 
        globals=benchmark_context, # On utilise notre nouveau contexte
        number=10
    ) / 10
    print(f"  {COMPRESSOR_OVERFLOW:<15}: {time_overflow_compress:.6f} secondes (moyenne sur 10)")
    compressors[COMPRESSOR_OVERFLOW] = setup_compressor(COMPRESSOR_OVERFLOW, test_data, main_bits=k_prime)
    
    print("\n")

    # --- 3. Benchmark de la fonction decompress() ---
    print(f"--- Mesure du temps de decompress() [100 exécutions] ---")
    
    time_spanning_decompress = timeit.timeit(
        stmt="compressors[COMPRESSOR_SPANNING].decompress()",
        setup="pass",
        globals=benchmark_context, # On utilise notre nouveau contexte
        number=100
    ) / 100
    print(f"  {COMPRESSOR_SPANNING:<15}: {time_spanning_decompress:.6f} secondes (moyenne sur 100)")

    time_overflow_decompress = timeit.timeit(
        stmt="compressors[COMPRESSOR_OVERFLOW].decompress()",
        setup="pass",
        globals=benchmark_context, # On utilise notre nouveau contexte
        number=100
    ) / 100
    print(f"  {COMPRESSOR_OVERFLOW:<15}: {time_overflow_decompress:.6f} secondes (moyenne sur 100)")
    
    print("\n")

    # --- 4. Benchmark de la fonction get(i) ---
    print(f"--- Mesure du temps de get(i) [1000 exécutions] ---")
    
    setup_code_get = f"i = {data_size // 2}"
    time_spanning_get = timeit.timeit(
        stmt="compressors[COMPRESSOR_SPANNING].get(i)",
        setup=setup_code_get,
        globals=benchmark_context, # On utilise notre nouveau contexte
        number=1000
    ) / 1000
    print(f"  {COMPRESSOR_SPANNING:<15}: {time_spanning_get:.6f} secondes (moyenne sur 1000)")

    time_overflow_get = timeit.timeit(
        stmt="compressors[COMPRESSOR_OVERFLOW].get(i)",
        setup=setup_code_get,
        globals=benchmark_context, # On utilise notre nouveau contexte
        number=1000
    ) / 1000
    print(f"  {COMPRESSOR_OVERFLOW:<15}: {time_overflow_get:.6f} secondes (moyenne sur 1000)")
    
    print("-" * 50)
    print("===== FIN DU BENCHMARK =====")

# Point d'entrée pour le benchmark
if __name__ == "__main__":
    run_benchmark()