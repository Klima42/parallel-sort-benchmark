import streamlit as st
from typing import Dict, Any

class ConfigPanel:
    def __init__(self):
        self.default_config = {
            'min_size': 1000,
            'max_size': 100000,
            'num_sizes': 5,
            'num_trials': 3,
            'num_processes': 4,
            'algorithms': [
                'Merge Sort',
                'Quick Sort',
                'Parallel Merge Sort',
                'Parallel Quick Sort'
            ]
        }

    def render(self) -> None:
        st.sidebar.header("Benchmark Configuration")
        # Basic configuration to test
        st.sidebar.number_input(
            "Test Size",
            value=self.default_config['min_size'],
            min_value=100,
            max_value=10000
        )

    def get_parameters(self) -> Dict[str, Any]:
        return {
            'min_size': 1000,
            'max_size': 10000,
            'num_sizes': 3,
            'num_trials': 2
        }