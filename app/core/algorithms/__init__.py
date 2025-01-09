"""
Sorting Algorithms Module
-----------------------
Contains implementations of various sorting algorithms.
"""

from .base import BaseSortingAlgorithm
from .parallel.parallel_merge import ParallelMergeSort
from .parallel.parallel_quick import ParallelQuickSort

# Available algorithms
AVAILABLE_ALGORITHMS = {
    'merge_sort': ParallelMergeSort,
    'quick_sort': ParallelQuickSort,
}

__all__ = [
    'BaseSortingAlgorithm',
    'ParallelMergeSort',
    'ParallelQuickSort',
    'AVAILABLE_ALGORITHMS'
]