#!/bin/bash
# Run the 4 pre-registered pair evaluations, 2 at a time, single-threaded BLAS.
cd "$(dirname "$0")/.."
export OMP_NUM_THREADS=1 OPENBLAS_NUM_THREADS=1 MKL_NUM_THREADS=1
(python3 -I scripts/11_evaluate_pairs.py 0 1000 > logs/primary_pair0.log 2>&1; python3 -I scripts/11_evaluate_pairs.py 2 1000 > logs/primary_pair2.log 2>&1) &
(python3 -I scripts/11_evaluate_pairs.py 1 1000 > logs/primary_pair1.log 2>&1; python3 -I scripts/11_evaluate_pairs.py 3 1000 > logs/primary_pair3.log 2>&1) &
wait
