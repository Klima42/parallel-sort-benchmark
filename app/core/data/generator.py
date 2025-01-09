from typing import Dict, List, Any
import numpy as np

class DataGenerator:
    def __init__(self):
        self.supported_distributions = ['uniform', 'normal', 'exponential']

    def generate_datasets(self, params: Dict[str, Any]) -> Dict[int, List[int]]:
        """Generate test datasets according to configuration parameters."""
        # Set random seed for reproducibility
        np.random.seed(params.get('random_seed', 42))
        
        datasets = {}
        sizes = [1000, 5000, 10000]  # Default sizes for testing
        
        for size in sizes:
            # Generate random data
            data = np.random.randint(0, size * 10, size=size)
            datasets[size] = data.tolist()
        
        return datasets

    def _generate_special_case(self, size: int, case_type: str) -> List[int]:
        """Generate special test cases."""
        if case_type == 'sorted':
            return list(range(size))
        elif case_type == 'reverse_sorted':
            return list(range(size-1, -1, -1))
        elif case_type == 'all_equal':
            return [42] * size
        elif case_type == 'nearly_sorted':
            arr = list(range(size))
            # Swap a few elements
            for _ in range(size // 20):
                i, j = np.random.randint(0, size, 2)
                arr[i], arr[j] = arr[j], arr[i]
            return arr
        else:
            return list(np.random.randint(0, size, size))