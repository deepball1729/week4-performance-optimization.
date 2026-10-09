# Week 4 Report: Performance Optimization in Python Applications

## 1. Objective
This project measures and improves a Python application that summarizes sales records. The output includes the record count, total revenue, and revenue grouped by category. The original and optimized implementations must return identical results.

## 2. Workload and reproducibility
- Synthetic dataset: 20,000 records and 80 possible categories.
- Dataset is deterministic and generated in code; no external input files are required.
- Each record contains a category string, quantity integer, and unit price.
- Timings use `time.perf_counter()` and the median of five runs after a small warm-up.
- Dataset creation is outside the timed section, so the measurement focuses on aggregation.
- Both implementations are run in the same Python process and environment.
- Profiling uses the standard-library `cProfile` and `pstats` modules. Captured reports are in `profiles/`.

## 3. Baseline implementation and bottleneck
`original.py` first builds a list of distinct categories using membership checks on a list. It then scans all records to compute the total, and scans all records again for every distinct category to calculate category revenue.

If there are N records and K distinct categories, the repeated category aggregation costs O(N × K). List membership while discovering categories can also cost O(N × K) in the worst case. This is avoidable repeated work and is the main expected bottleneck.

## 4. Optimization applied
`optimized.py` performs a single pass through the records:
1. Calculate each record's revenue once.
2. Add it to the running total.
3. Add it to a dictionary entry for that category, using `dict.get()`.

The aggregation is expected O(N) average time with O(K) additional memory. This avoids rescanning the dataset per category and uses a dictionary for direct average-case category lookup. The public result structure, rounding behavior, and values are kept equivalent to the baseline.

## 5. Before-and-after measurements
The benchmark was executed in the environment used to prepare this archive. Results are machine- and interpreter-dependent; rerun `python benchmark.py` on the submission machine and use those results if they differ.

```text
Baseline median:  0.014552 seconds
Optimized median: 0.003123 seconds
Speedup:          4.66x
Time reduction:   78.5%
Correctness:      PASS (full output dictionaries match)
```

The recorded speedup is calculated as baseline median time divided by optimized median time. Time reduction is calculated as 100 × (1 − optimized time / baseline time).

## 6. Profiling
`profiles/original_cprofile.txt` and `profiles/optimized_cprofile.txt` contain the top cumulative-time entries from `cProfile`. The profile includes profiler overhead, so the benchmark's `perf_counter` median is used for the primary timing comparison. To reproduce:
```bash
python -m cProfile -s cumulative original.py
python -m cProfile -s cumulative optimized.py
python benchmark.py
```
Run these commands on the same machine and Python version for a fair comparison.

## 7. Correctness verification
Automated tests compare the complete output dictionaries from both implementations for:
- Empty input
- One record
- Multiple categories and repeated categories
- Generated synthetic input
- Explicit total and per-category values

Test command:
```bash
python -m unittest -v test_app.py
```

Test result during archive preparation: **PASS** (5 tests). The benchmark also checks that complete result dictionaries match before reporting performance.

## 8. Resource usage and limitations
The optimized version uses a dictionary with one entry per distinct category, so its aggregation memory is O(K). The baseline also stores a list of categories and a result dictionary. This project does not claim a measured RAM reduction: no memory profiler was used, and actual memory use depends on Python's object overhead. The strongest demonstrated metric is execution time. For memory measurements, a future extension could use `tracemalloc` and report peak traced allocations.

Floating-point accumulation order is preserved for the total and within each category, which helps maintain output equivalence. Benchmarks can vary with CPU load, power mode, OS, Python version, and interpreter warm-up.

## 9. Conclusion
The primary optimization is algorithmic rather than a micro-optimization: repeated full-dataset scans were replaced by one-pass aggregation. The benchmark and correctness tests provide evidence of the performance change while checking that behavior remains unchanged.
