from typing import List, Dict, Tuple
from concurrent.futures import ProcessPoolExecutor
import multiprocessing as mp
from ..base import BaseSortingAlgorithm

class ParallelQuickSort(BaseSortingAlgorithm):
    def __init__(self, num_processes: int = None):
        super().__init__(name="Parallel Quick Sort")
        self.num_processes = num_processes or mp.cpu_count()
        self.min_partition_size = 1000  # Minimum size for parallel processing

    @property
    def is_parallel(self) -> bool:
        return True

    def partition(self, arr: List[int], low: int, high: int) -> Tuple[int, List[int]]:
        """Partition the array and return pivot index."""
        pivot = arr[high]
        i = low - 1
        
        for j in range(low, high):
            if arr[j] <= pivot:
                i += 1
                arr[i], arr[j] = arr[j], arr[i]
                
        arr[i + 1], arr[high] = arr[high], arr[i + 1]
        return i + 1, arr

    def _sequential_sort(self, arr: List[int], low: int, high: int) -> List[int]:
        """Sequential quicksort implementation."""
        if low < high:
            pivot_idx, arr = self.partition(arr, low, high)
            
            arr = self._sequential_sort(arr, low, pivot_idx - 1)
            arr = self._sequential_sort(arr, pivot_idx + 1, high)
            
        return arr

    def _parallel_partition(self, arr: List[int]) -> Tuple[List[int], List[int], List[int]]:
        """Partition array into three parts for parallel processing."""
        pivot = arr[len(arr) // 2]
        left = [x for x in arr if x < pivot]
        middle = [x for x in arr if x == pivot]
        right = [x for x in arr if x > pivot]
        
        return left, middle, right

    def _sort_partition(self, partition: List[int]) -> List[int]:
        """Sort a single partition."""
        if len(partition) <= 1:
            return partition
        return self._sequential_sort(partition.copy(), 0, len(partition) - 1)

    def sort(self, data: List[int]) -> List[int]:
        """Main parallel quicksort implementation."""
        if len(data) <= self.min_partition_size:
            return self._sequential_sort(data.copy(), 0, len(data) - 1)

        # Perform initial partition
        left, middle, right = self._parallel_partition(data)

        # Process partitions in parallel
        with ProcessPoolExecutor(max_workers=self.num_processes) as executor:
            # Sort left and right partitions in parallel
            future_left = executor.submit(self.sort, left)
            future_right = executor.submit(self.sort, right)

            # Wait for results
            sorted_left = future_left.result()
            sorted_right = future_right.result()

        # Combine results
        return sorted_left + middle + sorted_right

    def get_complexity(self) -> Dict[str, str]:
        """Return algorithm complexity information."""
        return {
            'time_best': 'O(n log n)',
            'time_average': 'O(n log n)',
            'time_worst': 'O(n²)',
            'space': 'O(n)',
            'parallel_speedup': 'O(p)',  # p is number of processors
            'parallel_efficiency': '~70-90%'
        }