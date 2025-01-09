from typing import List, Dict, Any
import psutil
import numpy as np
from ..utils.logging import get_logger

logger = get_logger(__name__)

def calculate_metrics(
    original_data: List[int],
    sorted_data: List[int],
    execution_time: float,
    algorithm_name: str,
    input_size: int
) -> Dict[str, Any]:
    """Calculate comprehensive performance metrics for a sorting run."""
    try:
        metrics = {
            'algorithm': algorithm_name,
            'input_size': input_size,
            'execution_time': execution_time,
            'memory_usage': psutil.Process().memory_info().rss / 1024 / 1024,  # MB
            'is_sorted': is_sorted(sorted_data),
            'stability_score': calculate_stability_score(original_data, sorted_data),
        }
        
        # Calculate additional metrics for parallel algorithms
        if 'parallel' in algorithm_name.lower():
            metrics.update({
                'cpu_utilization': psutil.cpu_percent(interval=0.1),
                'num_cpu_cores': psutil.cpu_count(),
                'parallel_efficiency': calculate_parallel_efficiency(
                    execution_time,
                    input_size,
                    psutil.cpu_count()
                )
            })
            
        return metrics
        
    except Exception as e:
        logger.error(f"Error calculating metrics: {str(e)}")
        raise

def is_sorted(data: List[int]) -> bool:
    """Check if the array is correctly sorted."""
    return all(data[i] <= data[i + 1] for i in range(len(data) - 1))

def calculate_stability_score(original: List[int], sorted_data: List[int]) -> float:
    """Calculate the stability score of the sorting algorithm.
    A score of 1.0 indicates perfect stability."""
    if len(original) != len(sorted_data):
        return 0.0
        
    # Create value-to-indices mapping for original array
    value_indices = {}
    for i, value in enumerate(original):
        if value not in value_indices:
            value_indices[value] = []
        value_indices[value].append(i)
    
    # Check relative ordering of equal elements
    total_pairs = 0
    preserved_pairs = 0
    
    for value, indices in value_indices.items():
        if len(indices) > 1:
            # Get corresponding indices in sorted array
            sorted_indices = [i for i, v in enumerate(sorted_data) if v == value]
            
            # Check if relative ordering is preserved
            total_pairs += len(indices) - 1
            for i in range(len(indices) - 1):
                if sorted_indices[i] < sorted_indices[i + 1]:
                    preserved_pairs += 1
    
    return preserved_pairs / total_pairs if total_pairs > 0 else 1.0

def calculate_parallel_efficiency(
    execution_time: float,
    input_size: int,
    num_cores: int
) -> float:
    """Calculate the parallel efficiency of the algorithm.
    A value close to 1.0 indicates good parallel scalability."""
    # Estimate sequential time based on O(n log n) complexity
    estimated_sequential_time = (input_size * np.log2(input_size)) / 1e6
    
    # Calculate speedup
    speedup = estimated_sequential_time / execution_time
    
    # Calculate efficiency
    efficiency = speedup / num_cores
    
    return min(1.0, efficiency)  # Cap at 1.0 for reasonable values

def aggregate_metrics(metrics_list: List[Dict[str, Any]]) -> Dict[str, Any]:
    """Aggregate metrics from multiple runs."""
    df = pd.DataFrame(metrics_list)
    
    aggregated = {
        'mean_execution_time': df['execution_time'].mean(),
        'std_execution_time': df['execution_time'].std(),
        'mean_memory_usage': df['memory_usage'].mean(),
        'success_rate': df['is_sorted'].mean() * 100,
        'mean_stability_score': df['stability_score'].mean()
    }
    
    if 'parallel_efficiency' in df.columns:
        aggregated.update({
            'mean_parallel_efficiency': df['parallel_efficiency'].mean(),
            'mean_cpu_utilization': df['cpu_utilization'].mean()
        })
    
    return aggregated