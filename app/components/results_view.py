import streamlit as st
import pandas as pd
import numpy as np
from typing import Dict, Any
import plotly.express as px
import plotly.graph_objects as go
import logging

class ResultsView:
    def __init__(self):
        # Formatters for different metric types
        self.metric_formatters = {
            'execution_time': lambda x: f"{x:.4f} seconds",
            'memory_usage': lambda x: f"{x:.2f} MB",
            'parallel_efficiency': lambda x: f"{x*100:.1f}%",
            'cpu_utilization': lambda x: f"{x:.1f}%",
            'stability_score': lambda x: f"{x*100:.1f}%"
        }

    def display_results(self, results: pd.DataFrame) -> None:
        """Display benchmark results in an organized manner."""
        st.header("Benchmark Results")

        # Create tabs for different views
        tab1, tab2, tab3 = st.tabs(["Summary", "Detailed Results", "Charts"])

        with tab1:
            self._display_summary(results)
        
        with tab2:
            self._display_detailed_results(results)
        
        with tab3:
            self._display_charts(results)

    def _display_summary(self, results: pd.DataFrame) -> None:
        """Display summary metrics."""
        st.subheader("Performance Summary")
        
        # Create three columns for metrics
        col1, col2, col3 = st.columns(3)

        with col1:
            # Best performing algorithm
            logger = logging.getLogger(__name__)
            logger.info("Results DataFrame columns: %s", results.columns)
            logger.info("Results DataFrame head: %s", results.head())

            best_algo = results.groupby('algorithm')['execution_time'].mean().idxmin()
            best_time = results[results['algorithm'] == best_algo]['execution_time'].mean()
            st.metric(
                "Best Algorithm",
                best_algo,
                f"Avg. time: {best_time:.4f}s"
            )

        with col2:
            # Overall efficiency
            if 'parallel_efficiency' in results.columns:
                avg_efficiency = results['parallel_efficiency'].mean()
                st.metric(
                    "Average Parallel Efficiency",
                    f"{avg_efficiency*100:.1f}%",
                    "Higher is better"
                )
            else:
                avg_memory = results['memory_usage'].mean()
                st.metric(
                    "Average Memory Usage",
                    f"{avg_memory:.2f} MB",
                    "Lower is better"
                )

        with col3:
            # Speedup metric
            sequential_time = results[~results['algorithm'].str.contains('Parallel')]['execution_time'].mean()
            parallel_time = results[results['algorithm'].str.contains('Parallel')]['execution_time'].mean()
            speedup = sequential_time / parallel_time if parallel_time > 0 else 0
            st.metric(
                "Average Speedup",
                f"{speedup:.2f}x",
                "Parallel vs Sequential"
            )

    def _display_detailed_results(self, results: pd.DataFrame) -> None:
        """Display detailed benchmark results."""
        st.subheader("Detailed Results")

        # Group results by algorithm and input size
        grouped_results = results.groupby(['algorithm', 'input_size']).agg({
            'execution_time': ['mean', 'std', 'min', 'max'],
            'memory_usage': 'mean'
        }).round(4)

        # Reset index for better display
        grouped_results = grouped_results.reset_index()

        # Format column names
        grouped_results.columns = [
            'Algorithm', 'Input Size', 'Mean Time (s)', 'Std Dev (s)',
            'Min Time (s)', 'Max Time (s)', 'Memory (MB)'
        ]

        # Display as a sortable table
        st.dataframe(
            grouped_results,
            hide_index=True,
            column_config={
                "Input Size": st.column_config.NumberColumn(format="%d"),
                "Mean Time (s)": st.column_config.NumberColumn(format="%.4f"),
                "Memory (MB)": st.column_config.NumberColumn(format="%.2f"),
            }
        )

    def _display_charts(self, results: pd.DataFrame) -> None:
        """Display performance charts."""
        st.subheader("Performance Charts")

        # Execution time vs input size
        fig1 = px.line(
            results,
            x='input_size',
            y='execution_time',
            color='algorithm',
            title='Execution Time vs Input Size',
            labels={
                'input_size': 'Input Size',
                'execution_time': 'Execution Time (seconds)',
                'algorithm': 'Algorithm'
            }
        )
        st.plotly_chart(fig1, use_container_width=True)

        # Memory usage comparison
        fig2 = px.bar(
            results.groupby('algorithm')['memory_usage'].mean().reset_index(),
            x='algorithm',
            y='memory_usage',
            title='Average Memory Usage by Algorithm',
            labels={
                'algorithm': 'Algorithm',
                'memory_usage': 'Memory Usage (MB)'
            }
        )
        st.plotly_chart(fig2, use_container_width=True)

        # Display download buttons
        st.subheader("Export Results")
        col1, col2 = st.columns(2)
        
        with col1:
            csv = results.to_csv(index=False)
            st.download_button(
                label="Download CSV",
                data=csv,
                file_name="sorting_benchmark_results.csv",
                mime="text/csv"
            )
            
        with col2:
            json_str = results.to_json(orient="records", indent=2)
            st.download_button(
                label="Download JSON",
                data=json_str,
                file_name="sorting_benchmark_results.json",
                mime="application/json"
            )