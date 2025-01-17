import streamlit as st
import sys
from pathlib import Path

# Add project root to Python path
project_root = Path(__file__).parent.parent.absolute()
sys.path.append(str(project_root))

from components.config_panel import ConfigPanel
from components.results_view import ResultsView
from components.visualizations import VisualizationDashboard
from benchmark.engine import BenchmarkEngine
from data.generator import DataGenerator

def main():
    st.set_page_config(
        page_title="Sorting Algorithm Benchmarks",
        page_icon="📊",
        layout="wide"
    )

    st.title("Sorting Algorithm Benchmarking Dashboard")

    # Initialize components
    config = ConfigPanel()
    results_view = ResultsView()
    viz_dashboard = VisualizationDashboard()
    
    # Sidebar configuration
    with st.sidebar:
        config.render()
        
    # Main content
    if st.button("Run Benchmarks"):
        with st.spinner("Running benchmarks..."):
            # Get configuration
            params = config.get_parameters()
            
            # Initialize benchmark engine
            engine = BenchmarkEngine()
            data_gen = DataGenerator()
            
            # Generate test data and run benchmarks
            test_data = data_gen.generate_datasets(params)
            results = engine.run_benchmarks(test_data, params)
            
            # Display results
            results_view.display_results(results)
            viz_dashboard.plot_metrics(results)

if __name__ == "__main__":
    main()