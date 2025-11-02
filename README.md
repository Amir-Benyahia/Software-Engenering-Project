# Software Engineering Project

This project was created for the M1 Software Engineering course. 

**Author:** Amir Benyahia


## How to Use

### 1. Requirements

* Python 3.10+

### 2. Setup

```bash
# 1. Clone the repository
git clone [https://github.com/Amir-Benyahia/Software-Engenering-Project.git](https://github.com/Amir-Benyahia/Software-Engenering-Project.git)
cd Software-Engenering-Project

# 2. Create a virtual environment
python3 -m venv venv

# 3. Activate the environment
# On macOS/Linux:
source venv/bin/activate

# On Windows:
  .\venv\Scripts\activate
```

### 3. Run

You can run the demo program (`main.py`) or the benchmark (`benchmark.py`). Run them from the project root after activating the virtual environment.

#### 3.1 Demo / tests (`main.py`)

Basics:

```bash
# Run all built-in tests (default datasets for each compressor)
python3 main.py

# Run one compressor on a provided array (Python list literal or CSV)
python3 main.py non_spanning "[9,8,7,0,15]"
python3 main.py spanning 1,2,3,4,5

# Read the array from stdin using '-'
echo "[1,2,3,4,5]" | python3 main.py non_spanning -

# Overflow compressor with custom main bits (k')
python3 main.py overflow "[1,2,3,1024,2048]" --main-bits 10
```

Arguments reference:

- compressor (optional positional): one of `non_spanning`, `spanning`, `overflow`.
- array (optional positional):
  - Accepts a Python list literal like `[1,2,3]`
  - Or CSV like `1,2,3`
  - Or `-` to read from STDIN
- `--main-bits` (optional): number of bits for the main area when using the overflow compressor. Default when using CLI is `3`.

Notes:
- If you create an overflow compressor directly via the factory without passing `main_bits`, its default is `8`. From the CLI, the default is `3`. Specify `--main-bits` explicitly to avoid confusion.
- Values greater than or equal to the sentinel `(1 << main_bits) - 1` are stored in the overflow area by design.
- Current implementation assumes non-negative 32-bit integers (array('I')).

Positional arguments note:
- `compressor` and `array` are both optional positionals. If you pass a single positional argument, it will be interpreted as `compressor`.
- To provide an array, pass the compressor first, then the array or use `-` to read the array from STDIN.

Examples:

```bash
# Array provided after the compressor name
python3 main.py spanning 1,2,3,4,5

# Array via stdin (convenient for piping/generators)
echo "[1,2,3,4,5]" | python3 main.py non_spanning -
```

#### 3.2 Benchmark (`benchmark.py`)

Runs timing for `compress`, `decompress`, and `get(i)` on a 10,000-element dataset using `timeit`.

```bash
python3 benchmark.py
```

Output includes average times for the spanning and overflow compressors.

### 4. Project structure

- `main.py`: demo/CLI to try the compressors and verify round-trip + get(i)
- `benchmark.py`: performance measurements with timeit
- `compressor_factory.py`: factory + compressor name constants
- `bit_packing_non_spanning.py`: non-spanning BitPacking
- `bit_packing_spanning.py`: spanning BitPacking
- `bit_packing_overflow.py`: overflow BitPacking (decorator over spanning)
- `integer_compressor.py`: common interface and shared utilities

### 5. Known limitations and notes

- Negative integers are not supported in the current representation.
- For large proportions of overflow values, `get(i)` in the overflow codec can be slower an index cache would improve it.
- To reproduce results on another machine, ensure Python 3.10+ and similar environment times can vary by hardware.
