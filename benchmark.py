import timeit
import random
from compressor_factory import CompressorFactory, COMPRESSOR_SPANNING, COMPRESSOR_NON_SPANNING, COMPRESSOR_OVERFLOW
from integer_compressor import IntegerCompressor
from typing import List, Dict

def setup_compressor(compressor_name: str, data: List[int], **kwargs) -> IntegerCompressor:

    # Helper function for the benchmark.
    # It creates the compressor and runs compress()
    # so we don't measure that part.
  
    compressor = CompressorFactory.create_compressor(compressor_name, **kwargs)
    compressor.compress(data)
    return compressor

def run_benchmark() -> None:
    # Runs the performance benchmarks as requested by the subject.
    print("===== STARTING BENCHMARK =====")
    print("Protocol: Using 'timeit' to run each function multiple times.")
    print("This gives a reliable average time.")
    print("Testing on a 10,000 integer dataset.")
    print("-" * 50)

    # 1 - Prepare test data
    k_prime: int = 10
    max_normal: int = (1 << k_prime) - 1 # Max value for k'
    data_size: int = 10000
    test_data: List[int] = []
    
    # Create dataset with some overflow values
    for _ in range(data_size):
        if random.random() < 0.05: # 5% chance of overflow
            test_data.append(random.randint(max_normal, max_normal * 10))
        else:
            test_data.append(random.randint(0, max_normal - 1))

    print(f"Dataset created: {data_size} ints, k'={k_prime} bits.\n")
    
    compressors: Dict[str, IntegerCompressor] = {}
    
    # We need to pass the local/global variables to timeit
    benchmark_context = globals().copy()
    benchmark_context.update(locals())
    
    # 2 - Benchmark compress() 
    print(f"--- Timing compress() [10 runs] ---")
    
    setup_code_spanning_compress = "compressor = CompressorFactory.create_compressor(COMPRESSOR_SPANNING)"
    
    # Run compress() 10 times
    time_spanning_compress = timeit.timeit(
        stmt="compressor.compress(test_data)", 
        setup=setup_code_spanning_compress, 
        globals=benchmark_context,
        number=10
    ) / 10
    print(f"  {COMPRESSOR_SPANNING:<15}: {time_spanning_compress:.6f} seconds (avg over 10)")
    
    # Setup the compressor for later tests
    compressors[COMPRESSOR_SPANNING] = setup_compressor(COMPRESSOR_SPANNING, test_data)

    setup_code_overflow_compress = "compressor = CompressorFactory.create_compressor(COMPRESSOR_OVERFLOW, main_bits=k_prime)"
    time_overflow_compress = timeit.timeit(
        stmt="compressor.compress(test_data)", 
        setup=setup_code_overflow_compress, 
        globals=benchmark_context,
        number=10
    ) / 10
    print(f"  {COMPRESSOR_OVERFLOW:<15}: {time_overflow_compress:.6f} seconds (avg over 10)")
    compressors[COMPRESSOR_OVERFLOW] = setup_compressor(COMPRESSOR_OVERFLOW, test_data, main_bits=k_prime)
    
    print("\n")

    #3 - Benchmark decompress()
    print(f"--- Timing decompress() [100 runs] ---")
    
    # Run decompress() 100 times
    time_spanning_decompress = timeit.timeit(
        stmt="compressors[COMPRESSOR_SPANNING].decompress()",
        setup="pass", # Compressor is already set up
        globals=benchmark_context,
        number=100
    ) / 100
    print(f"  {COMPRESSOR_SPANNING:<15}: {time_spanning_decompress:.6f} seconds (avg over 100)")

    time_overflow_decompress = timeit.timeit(
        stmt="compressors[COMPRESSOR_OVERFLOW].decompress()",
        setup="pass",
        globals=benchmark_context,
        number=100
    ) / 100
    print(f"  {COMPRESSOR_OVERFLOW:<15}: {time_overflow_decompress:.6f} seconds (avg over 100)")
    
    print("\n")

    # 4 - Benchmark get(i)
    print(f"--- Timing get(i) [1000 runs] ---")
    
    setup_code_get = f"i = {data_size // 2}" # get middle element
    
    # Run get() 1000 times
    time_spanning_get = timeit.timeit(
        stmt="compressors[COMPRESSOR_SPANNING].get(i)",
        setup=setup_code_get,
        globals=benchmark_context,
        number=1000
    ) / 1000
    print(f"  {COMPRESSOR_SPANNING:<15}: {time_spanning_get:.6f} seconds (avg over 1000)")

    time_overflow_get = timeit.timeit(
        stmt="compressors[COMPRESSOR_OVERFLOW].get(i)",
        setup=setup_code_get,
        globals=benchmark_context,
        number=1000
    ) / 1000
    print(f"  {COMPRESSOR_OVERFLOW:<15}: {time_overflow_get:.6f} seconds (avg over 1000)")
    
    print("-" * 50)
    print("===== BENCHMARK FINISHED =====")

# Run the benchmark
if __name__ == "__main__":
    run_benchmark()