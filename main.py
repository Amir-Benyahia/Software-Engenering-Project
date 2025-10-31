from compressor_factory import CompressorFactory, COMPRESSOR_SPANNING, COMPRESSOR_NON_SPANNING, COMPRESSOR_OVERFLOW
import sys
from typing import List

# Simple test function
def test_compression(compressor_name: str, data: List[int], **kwargs) -> None:
    print("-" * 40)
    print(f"TESTING: '{compressor_name}'")
    print(f"Original data: {data}")

    try:
        # 1. Create compressor from factory
        compressor = CompressorFactory.create_compressor(compressor_name, **kwargs)
        
        # 2. Compress
        compressor.compress(data)
        
        # 3. Decompress
        decompressed_data = compressor.decompress()
        
        print(f"Decompressed: {decompressed_data}")

        # 4. Check if it worked
        if data == decompressed_data:
            print("SUCCESS: Data is identical.")
        else:
            print("FAILURE: Data is different!")
            
        # 5. Test get()
        index_to_test = len(data) // 2
        original_val = data[index_to_test]
        get_val = compressor.get(index_to_test)
        
        print(f"Testing get({index_to_test}): Original={original_val}, Got={get_val}")
        if original_val == get_val:
            print("SUCCESS: get() works.")
        else:
            print("FAILURE: get() failed!")
            
        # 6. Show size
        original_size = len(data) * 4 # 4 bytes per int
        compressed_size = compressor.get_compressed_size_in_bytes()
        print(f"Original size (approx): {original_size} bytes")
        print(f"Compressed size: {compressed_size} bytes")
        
    except Exception as e:
        print(f"ERROR testing '{compressor_name}': {e}")
        sys.exit(1)
    
    print("-" * 40)


# Main entry point
if __name__ == "__main__":
    
    print("===== STARTING COMPRESSION TESTS =====")
    
    test_data_simple: List[int] = [1, 2, 3, 4, 5, 6, 7, 0, 1, 3]
    test_data_medium: List[int] = [100, 2000, 4095, 0, 1234, 567]
    # Subject example: [1, 2, 3, 1024, 4, 5, 2048] 
    test_data_overflow: List[int] = [1, 2, 3, 1024, 4, 5, 2048]
    
    # Test non-spanning
    test_compression(COMPRESSOR_NON_SPANNING, test_data_simple)
    test_compression(COMPRESSOR_NON_SPANNING, test_data_medium)
    
    # Test spanning
    test_compression(COMPRESSOR_SPANNING, test_data_simple)
    test_compression(COMPRESSOR_SPANNING, test_data_medium)
    
    # Test overflow
    print("\n===== TESTING OVERFLOW AREA =====")
    test_compression(COMPRESSOR_OVERFLOW, test_data_overflow, main_bits=3)

    print("\n===== ALL TESTS FINISHED =====")