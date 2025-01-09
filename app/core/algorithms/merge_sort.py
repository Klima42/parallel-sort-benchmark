from typing import List, Dict
from .base import BaseSortingAlgorithm

class MergeSort(BaseSortingAlgorithm):
    def __init__(self):
        super().__init__(name="Merge Sort")

    def merge(self, left: List[int], right: List[int]) -> List[int]:
        """Merge two sorted arrays."""
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

    def sort(self, data: List[int]) -> List[int]:
        """Sequential merge sort implementation."""
        if len(data) <= 1:
            return data

        mid = len(data) // 2
        left = self.sort(data[:mid])
        right = self.sort(data[mid:])
        
        return self.merge(left, right)

    def get_complexity(self) -> Dict[str, str]:
        return {
            'time_best': 'O(n log n)',
            'time_average': 'O(n log n)',
            'time_worst': 'O(n log n)',
            'space': 'O(n)'
        }