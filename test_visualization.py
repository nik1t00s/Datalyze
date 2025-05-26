"""Test script for visualizing different types of data.

This script creates test datasets and directly uses the DataFrameVisualizer
to create plots without user interaction.

Usage:
    python test_visualization.py
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import sys

from localization import Localizer
from data_visualizer import DataFrameVisualizer

def test_basic_visualizations():
    """Test basic visualization capabilities."""
    print("\nWelcome to the Simplified Visualization Test Suite")
    print("This will test the visualization capabilities with different data types")
    
    # Create test data
    np.random.seed(42)
    dates = pd.date_range(start='2024-01-01', periods=50)
    df = pd.DataFrame({
        'Date': dates,
        'Value': np.random.normal(100, 10, 50),
        'Category': np.random.choice(['A', 'B', 'C'], 50),
        'Count': np.random.randint(1, 100, 50)
    })
    
    print(f"\nTest data sample:\n{df.head()}")
    
    localizer = Localizer()
    visualizer = DataFrameVisualizer(localizer)
    
    # Test 1: Line chart with dates
    print("\nTesting line chart with dates...")
    visualizer.create_plot(df, 'Date', 'Value', 'line')
    
    # Test 2: Bar chart with categories
    print("\nTesting bar chart with categories...")
    visualizer.create_plot(df, 'Category', 'Count', 'bar')
    
    # Test 3: Multiple Y columns
    print("\nTesting multiple Y columns...")
    visualizer.create_plot(df, 'Date', ['Value', 'Count'], 'line')
    
    # Test 4: Large numbers
    print("\nTesting large numbers...")
    # Add a column with large numbers
    df['LargeValue'] = df['Value'] * 100000
    visualizer.create_plot(df, 'Category', 'LargeValue', 'bar')
    
    print("\nAll tests completed. Please check the generated plot files.")

if __name__ == '__main__':
    test_basic_visualizations()

