"""Repeatable benchmark and cProfile summary; standard library only."""
from __future__ import annotations
import cProfile
import io
import pstats
import statistics
import time
from original import summarize_sales as baseline, make_dataset
from optimized import summarize_sales as optimized

def time_function(function, data, repeats=5):
    samples = []
    for _ in range(repeats):
        start = time.perf_counter()
        result = function(data)
        samples.append(time.perf_counter() - start)
    return statistics.median(samples), result

def profile_function(function, data):
    profiler = cProfile.Profile()
    profiler.enable()
    result = function(data)
    profiler.disable()
    stream = io.StringIO()
    pstats.Stats(profiler, stream=stream).strip_dirs().sort_stats("cumulative").print_stats(12)
    return result, stream.getvalue()

def main():
    data = make_dataset(size=20_000, category_count=80)
    # Warm-up helps reduce one-off interpreter startup effects.
    baseline(data[:100])
    optimized(data[:100])
    base_time, base_result = time_function(baseline, data)
    opt_time, opt_result = time_function(optimized, data)
    assert base_result == opt_result, "Implementations returned different results"
    speedup = base_time / opt_time if opt_time else float("inf")
    print("Dataset: 20,000 records, 80 possible categories")
    print("Timing: median of 5 runs; dataset generated before timing")
    print(f"Baseline median:  {base_time:.6f} seconds")
    print(f"Optimized median: {opt_time:.6f} seconds")
    print(f"Speedup:          {speedup:.2f}x")
    print(f"Time reduction:   {(1 - opt_time/base_time)*100:.1f}%")
    print("Correctness:      PASS (full output dictionaries match)")
    _, base_profile = profile_function(baseline, data)
    _, opt_profile = profile_function(optimized, data)
    os.makedirs("profiles", exist_ok=True)
    with open("profiles/original_cprofile.txt", "w", encoding="utf-8") as f:
        f.write(base_profile)
    with open("profiles/optimized_cprofile.txt", "w", encoding="utf-8") as f:
        f.write(opt_profile)
    print("\nTop baseline profile entries:\n" + base_profile)
    print("\nTop optimized profile entries:\n" + opt_profile)

if __name__ == "__main__":
    import os
    main()
