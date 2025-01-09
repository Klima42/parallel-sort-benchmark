import streamlit as st
import plotly.express as px
import plotly.graph_objects as go
import pandas as pd
import numpy as np
from typing import Dict, Any

class VisualizationDashboard:
    def __init__(self):
        self.color_scheme = {
            'Merge Sort': '#1f77b4',
            'Quick Sort': '#ff7f0e',
            'Parallel Merge Sort': '#2ca02c',
            'Parallel Quick Sort': '#d62728'
        }

    def plot_execution_times(self, results: pd.DataFrame) -> None:
        """Plot execution times for different algorithms and input sizes."""
        fig = px.line(
            results,
            x='input_size',
            y='execution_time',
            color='algorithm',
            markers=True,
            title='Algorithm Execution Times vs Input Size',
            labels={
                'input_size': 'Input Size',
                'execution_time': 'Execution Time (seconds)',
                'algorithm': 'Algorithm'
            }
        )
        st.plotly_chart(fig, use_container_width=True)

    def plot_speedup_comparison(self, results: pd.DataFrame) -> None:
        """Plot speedup of parallel vs sequential algorithms."""
        # Calculate speedup for each algorithm pair
        speedup_data = []
        
        for size in results['input_size'].unique():
            size_results = results[results['input_size'] == size]
            
            # Merge Sort speedup
            merge_time = size_results[
                size_results['algorithm'] == 'Merge Sort'
            ]['execution_time'].mean()
            parallel_merge_time = size_results[
                size_results['algorithm'] == 'Parallel Merge Sort'
            ]['execution_time'].mean()
            
            # Quick Sort speedup
            quick_time = size_results[
                size_results['algorithm'] == 'Quick Sort'
            ]['execution_time'].mean()
            parallel_quick_time = size_results[
                size_results['algorithm'] == 'Parallel Quick Sort'
            ]['execution_time'].mean()
            
            speedup_data.append({
                'input_size': size,
                'Merge Sort Speedup': merge_time / parallel_merge_time,
                'Quick Sort Speedup': quick_time / parallel_quick_time
            })
        
        speedup_df = pd.DataFrame(speedup_data)
        
        fig = go.Figure()
        fig.add_trace(go.Scatter(
            x=speedup_df['input_size'],
            y=speedup_df['Merge Sort Speedup'],
            name='Merge Sort Speedup',
            mode='lines+markers'
        ))
        fig.add_trace(go.Scatter(
            x=speedup_df['input_size'],
            y=speedup_df['Quick Sort Speedup'],
            name='Quick Sort Speedup',
            mode='lines+markers'
        ))
        
        fig.update_layout(
            title='Parallel Speedup vs Input Size',
            xaxis_title='Input Size',
            yaxis_title='Speedup Factor',
            showlegend=True
        )
        
        st.plotly_chart(fig, use_container_width=True)

    def plot_memory_usage(self, results: pd.DataFrame) -> None:
        """Plot memory usage patterns for different algorithms."""
        fig = px.bar(
            results,
            x='algorithm',
            y='memory_usage',
            color='algorithm',
            facet_col='input_size',
            title='Memory Usage by Algorithm and Input Size',
            labels={
                'memory_usage': 'Memory Usage (MB)',
                'algorithm': 'Algorithm',
                'input_size': 'Input Size'
            }
        )
        st.plotly_chart(fig, use_container_width=True)

    def plot_metrics(self, results: pd.DataFrame) -> None:
        """Display all visualization components."""
        st.subheader("Performance Metrics")
        
        # Create tabs for different visualizations
        tabs = st.tabs([
            "Execution Times",
            "Parallel Speedup",
            "Memory Usage",
            "Detailed Analysis"
        ])
        
        with tabs[0]:
            self.plot_execution_times(results)
            
        with tabs[1]:
            self.plot_speedup_comparison(results)
            
        with tabs[2]:
            self.plot_memory_usage(results)
            
        with tabs[3]:
            self.plot_detailed_analysis(results)

    def plot_detailed_analysis(self, results: pd.DataFrame) -> None:
        """Show detailed statistical analysis of results."""
        st.write("Statistical Summary")
        
        # Group by algorithm and calculate statistics
        stats = results.groupby('algorithm').agg({
            'execution_time': ['mean', 'std', 'min', 'max'],
            'memory_usage': ['mean', 'std']
        }).round(4)
        
        st.dataframe(stats)
        
        # Distribution plot
        fig = go.Figure()
        for algo in results['algorithm'].unique():
            fig.add_trace(go.Box(
                y=results[results['algorithm'] == algo]['execution_time'],
                name=algo,
                boxpoints='all',
                jitter=0.3,
                pointpos=-1.8
            ))
            
        fig.update_layout(
            title='Distribution of Execution Times by Algorithm',
            yaxis_title='Execution Time (seconds)',
            showlegend=True
        )
        
        st.plotly_chart(fig, use_container_width=True)