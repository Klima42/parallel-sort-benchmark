from abc import ABC, abstractmethod
from typing import List, Dict, Any

class BaseSortingAlgorithm(ABC):
    """Abstract base class for all sorting algorithms."""
    
    def __init__(self, name: str, **kwargs):
        self.name = name
        self.config = kwargs
    
    @abstractmethod
    def sort(self, data: List[int]) -> List[int]:
        """Sort the input data and return sorted list."""
        pass
    
    @property
    def is_parallel(self) -> bool:
        """Whether this is a parallel sorting implementation."""
        return False
    
    def get_complexity(self) -> Dict[str, str]:
        """Return time and space complexity information."""
        return {
            'time_best': 'O(n log n)',
            'time_average': 'O(n log n)', 
            'time_worst': 'O(n log n)',
            'space': 'O(n)'
        }
    
    def validate_sort(self, sorted_data: List[int]) -> bool:
        """Validate that the data is correctly sorted."""
        if len(sorted_data) <= 1:
            return True
            
        for i in range(len(sorted_data) - 1):
            if sorted_data[i] > sorted_data[i + 1]:
                return False
                
        return True
    
    def __str__(self) -> str:
        return f"{self.name} ({'Parallel' if self.is_parallel else 'Sequential'})"