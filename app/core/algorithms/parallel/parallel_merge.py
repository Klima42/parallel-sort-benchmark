from typing import List
from concurrent.futures import ProcessPoolExecutor
import multiprocessing as mp
from ..base import BaseSortingAlgorithm

class ParallelMergeSort(BaseSortingAlgorithm):
    def __init__(self, num_processes: int = None):
        super().__init__(name="Parallel Merge Sort")
        self.num_processes = num_processes or mp.cpu_count()

    @property
    def is_parallel(self) -> bool:
        return True

    def merge(self, left: List[int], right: List[int]) -> List[int]:
        result = []
        i = j = 0
        
        while i < len(left) and j < len(right):
            if left[i] <= right[j]:
                result.append(left[i])
                i += 1
            else:
                result.append(right[j])
                j += 1
        
        result.extend(left[i:])
        result.extend(right[j:])
        return result

    def _sequential_sort(self, arr: List[int]) -> List[int]:
        if len(arr) <= 1:
            return arr
            
        mid = len(arr) // 2
        left = self._sequential_sort(arr[:mid])
        right = self._sequential_sort(arr[mid:])
        
        return self.merge(left, right)

    def sort(self, data: List[int]) -> List[int]:
        if len(data) <= 1000:  # Use sequential for small arrays
            return self._sequential_sort(data)

        # Split data into chunks
        chunk_size = len(data) // self.num_processes
        chunks = [data[i:i + chunk_size] for i in range(0, len(data), chunk_size)]

        # Sort chunks in parallel
        with ProcessPoolExecutor(max_workers=self.num_processes) as executor:
            sorted_chunks = list(executor.map(self._sequential_sort, chunks))

        # Merge sorted chunks
        while len(sorted_chunks) > 1:
            pairs = [(sorted_chunks[i], sorted_chunks[i + 1]) 
                    for i in range(0, len(sorted_chunks) - 1, 2)]
            
            if len(sorted_chunks) % 2:
                pairs.append((sorted_chunks[-1], []))

            with ProcessPoolExecutor(max_workers=self.num_processes) as executor:
                sorted_chunks = list(executor.map(
                    lambda x: self.merge(x[0], x[1]), pairs
                ))

        return sorted_chunks[0]