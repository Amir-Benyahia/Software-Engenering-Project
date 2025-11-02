from compressor_factory import CompressorFactory, COMPRESSOR_SPANNING, COMPRESSOR_NON_SPANNING, COMPRESSOR_OVERFLOW
import sys
import argparse
import ast
from typing import List, Optional


# This is the main test function
# It creates a compressor, runs compress/decompress, and validates the results
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


def parse_array(text: Optional[str]) -> Optional[List[int]]:
    """
    Parse an array from a string input.
    
    This function accepts multiple formats:
    - Python list literal like [1,2,3]
    - CSV format like 1,2,3
    - Or '-' to read from STDIN
    
    Returns list[int] or None if text is None.
    """
    if text is None:
        return None

    s = text.strip()
    
    # Special case: read from stdin
    if s == "-":
        s = sys.stdin.read().strip()

    if not s:
        return []

    # Method 1: Try to parse as Python literal (accepts [1,2,3])
    try:
        val = ast.literal_eval(s)
        if isinstance(val, (list, tuple)):
            return [int(x) for x in val]
    except Exception:
        pass

    # Method 2: Fallback to comma-separated values
    try:
        parts = [p.strip() for p in s.split(',') if p.strip() != '']
        return [int(p) for p in parts]
    except Exception:
        raise ValueError(f"Cannot parse array from: {text}")


def main():
    # This is the main entry point
    # It parses command line arguments and runs the appropriate tests
    parser = argparse.ArgumentParser(description="Run compressor tests. Both arguments are optional.")
    parser.add_argument('compressor', nargs='?', help=f"Compressor name (one of: {COMPRESSOR_NON_SPANNING}, {COMPRESSOR_SPANNING}, {COMPRESSOR_OVERFLOW})")
    parser.add_argument('array', nargs='?', help="Array to test: Python list literal '[1,2,3]' or comma-separated '1,2,3'. Use '-' to read from stdin.")
    parser.add_argument('--main-bits', type=int, default=3, help="(optional) main_bits for overflow compressor (default: 3)")

    args = parser.parse_args()

    # Default test datasets
    test_data_simple: List[int] = [1, 2, 3, 4, 5, 6, 7, 0, 1, 3]
    test_data_medium: List[int] = [100, 2000, 4095, 0, 1234, 567]
    test_data_overflow: List[int] = [1, 2, 3, 1024, 4, 5, 2048]

    allowed = [COMPRESSOR_NON_SPANNING, COMPRESSOR_SPANNING, COMPRESSOR_OVERFLOW]

    compressor = args.compressor
    array = parse_array(args.array) if args.array is not None else None

    print("===== STARTING COMPRESSION TESTS =====")

    # Case 1: No arguments - run all tests on default datasets
    if compressor is None and array is None:
        # Test non-spanning
        test_compression(COMPRESSOR_NON_SPANNING, test_data_simple)
        test_compression(COMPRESSOR_NON_SPANNING, test_data_medium)

        # Test spanning
        test_compression(COMPRESSOR_SPANNING, test_data_simple)
        test_compression(COMPRESSOR_SPANNING, test_data_medium)

        # Test overflow
        print("\n===== TESTING OVERFLOW AREA =====")
        test_compression(COMPRESSOR_OVERFLOW, test_data_overflow, main_bits=args.main_bits)

        print("\n===== ALL TESTS FINISHED =====")
        return

    # Case 2: Only compressor provided - run it on default datasets
    if compressor is not None and array is None:
        if compressor not in allowed:
            print(f"Unknown compressor '{compressor}'. Allowed: {allowed}")
            sys.exit(2)

        if compressor == COMPRESSOR_OVERFLOW:
            print(f"Running '{compressor}' on default overflow data with main_bits={args.main_bits}")
            test_compression(compressor, test_data_overflow, main_bits=args.main_bits)
        else:
            print(f"Running '{compressor}' on default sample data")
            test_compression(compressor, test_data_simple)
            test_compression(compressor, test_data_medium)

        print("\n===== DONE =====")
        return

    # Case 3: Only array provided - run all compressors on this array
    if compressor is None and array is not None:
        print(f"Running all compressors on provided array: {array}")
        test_compression(COMPRESSOR_NON_SPANNING, array)
        test_compression(COMPRESSOR_SPANNING, array)
        test_compression(COMPRESSOR_OVERFLOW, array, main_bits=args.main_bits)
        print("\n===== DONE =====")
        return

    # Case 4: Both compressor and array provided - run that specific test
    if compressor is not None and array is not None:
        if compressor not in allowed:
            print(f"Unknown compressor '{compressor}'. Allowed: {allowed}")
            sys.exit(2)

        print(f"Running compressor '{compressor}' on provided array: {array}")
        if compressor == COMPRESSOR_OVERFLOW:
            test_compression(compressor, array, main_bits=args.main_bits)
        else:
            test_compression(compressor, array)


if __name__ == "__main__":
    main()