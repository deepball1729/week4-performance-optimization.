# Week 4 — Performance Optimization in Python Applications

A self-contained demonstration project comparing a deliberately inefficient implementation with an optimized implementation of a sales-data summary task.

## Requirements
- Python 3.9 or newer
- Standard library only; no external packages or input files required

## Run
```bash
python benchmark.py
python -m cProfile -s cumulative original.py
python -m cProfile -s cumulative optimized.py
python -m unittest -v test_app.py
```

The benchmark generates its own deterministic synthetic dataset. Timing varies by machine and Python version; use the measured output from your own computer in any final submission. See `REPORT.md` for methodology and results recorded when this archive was prepared.

## Files
- `original.py` — baseline implementation
- `optimized.py` — optimized implementation
- `benchmark.py` — repeatable before/after timing and cProfile summary
- `test_app.py` — correctness-equivalence tests
- `profiles/` — captured cProfile text output
- `REPORT.md` — analysis, optimization rationale, measured comparison, and limitations
