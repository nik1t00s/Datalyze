import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
from typing import Union, List, Optional, Tuple
import warnings
from datetime import datetime
import matplotlib.dates as mdates

# Ignore matplotlib warnings
warnings.filterwarnings("ignore")

class DataFrameVisualizer:  # Changed from DataVisualizer to maintain backward compatibility
    def __init__(self, localizer):
        # Configure matplotlib for better performance
        plt.style.use('fast')
        
        # Store localizer for internationalization
        self.localizer = localizer
        
        # Performance-oriented defaults
        self.MAX_POINTS = 1000  # Maximum points to display
        self.MIN_POINTS = 50    # Minimum points to ensure readable plots
        self.CATEGORY_LIMIT = 30  # Maximum categories for bar charts
        
        # Clean up any existing plots at initialization
        self._cleanup_figures()
        
    def _cleanup_figures(self):
        """Clean up any existing matplotlib figures and resources."""
        plt.close('all')
        plt.clf()  # Clear current figure
        plt.cla()  # Clear current axes
        plt.rcParams['figure.figsize'] = plt.rcParamsDefault['figure.figsize']  # Reset figure size
        import gc
        gc.collect()  # Force garbage collection
        
    def _is_datetime(self, series: pd.Series) -> bool:
        """Check if series contains datetime data."""
        return (
            pd.api.types.is_datetime64_any_dtype(series) or
            (len(series) > 0 and isinstance(series.iloc[0], (datetime, np.datetime64)))
        )
        
    def _is_date_column(self, series: pd.Series) -> bool:
        """Check if series can be converted to datetime."""
        if len(series) == 0:
            return False
            
        try:
            pd.to_datetime(series.iloc[0])
            return True
        except:
            return False
            
    def _adjust_figure_size(self, x_col: str, y_cols: List[str], n_points: int) -> Tuple[int, int]:
        """Calculate optimal figure size based on data."""
        base_width = 12
        base_height = 6
        
        if n_points > 100:
            base_width = min(20, base_width * (1 + np.log10(n_points/100)))
            
        if len(y_cols) > 2:
            base_height *= 1.5
            
        return (base_width, base_height)
        
    def _validate_data(self, df: pd.DataFrame, x_col: str, y_cols: List[str]) -> None:
        """Validate input data before plotting.
        
        Args:
            df: Input DataFrame
            x_col: X-axis column name
            y_cols: Y-axis column names
            
        Raises:
            ValueError: If validation fails
        """
        # Check for empty DataFrame more efficiently
        if df.empty:
            raise ValueError("DataFrame is empty")
            
        # Check columns existence without creating new lists
        missing_cols = set([x_col] + y_cols) - set(df.columns)
        if missing_cols:
            raise ValueError(f"Missing columns: {', '.join(missing_cols)}")
            
        # Check for missing values
        missing_data = df[[x_col] + y_cols].isnull().sum()
        if missing_data.any():
            print("\nWarning: Missing values detected:")
            for col, count in missing_data[missing_data > 0].items():
                print(f"- {col}: {count} missing values")
        
        # Check for data range issues
        for col in y_cols:
            if pd.api.types.is_numeric_dtype(df[col]):
                if df[col].isin([np.inf, -np.inf]).any():
                    print(f"\nWarning: Infinite values found in column {col}")
                # Check for very large values that might cause overflow
                try:
                    if (df[col].abs() > 1e308).any():
                        print(f"\nWarning: Very large values found in column {col}")
                except:
                    pass
    
    def _manage_memory(self, df: pd.DataFrame) -> None:
        """Manage memory for large datasets."""
        if len(df) > self.MAX_POINTS:
            import gc
            # More aggressive memory cleanup
            gc.collect()
            # Clear matplotlib cache
            plt.close('all')
            # Suggest memory optimization
            print(f"\nWarning: Large dataset detected ({len(df)} points). Consider reducing data size before plotting.")
        
    def create_plot(self, df: pd.DataFrame, x_col: str, y_cols: Union[str, List[str]], 
                   chart_type: str, sample_size: Optional[int] = None) -> None:
        """Create a plot without user interaction.
        
        Args:
            df: DataFrame containing data to plot
            x_col: X-axis column name
            y_cols: Y-axis column name(s), string or list
            chart_type: Type of chart to plot ('bar' or 'line')
            sample_size: Optional custom sample size
        """
        # Validate inputs
        if not isinstance(df, pd.DataFrame):
            raise ValueError("Input must be a pandas DataFrame")
        if not isinstance(chart_type, str):
            raise ValueError("chart_type must be a string")
        if chart_type.lower() not in ['line', 'bar']:
            raise ValueError("chart_type must be 'line' or 'bar'")
            
        # Handle single column as string or multiple columns as list
        if isinstance(y_cols, str):
            y_cols = [y_cols]
        
        # Manage memory for large datasets
        self._manage_memory(df)
        
        # For very large datasets, only keep required columns
        if len(df) > self.MAX_POINTS:
            required_cols = [x_col] + (y_cols if isinstance(y_cols, list) else [y_cols])
            df = df[required_cols].copy(deep=False)
        
        try:
            # Clean up any existing plots
            self._cleanup_figures()
            
            # Plot the chart
            self._plot_chart(df, chart_type.lower(), x_col, y_cols, sample_size)
            
        except Exception as e:
            print(f"Error creating plot: {str(e)}")
            import traceback
            traceback.print_exc()
        finally:
            # More thorough cleanup
            plt.close('all')
            import gc
            gc.collect()
            
    def show_menu(self, df: pd.DataFrame) -> None:
        """Show visualization menu and handle user interaction.
        
        Args:
            df: DataFrame to visualize
        """
        while True:
            print(f"\n=== {self.localizer.get_string(8)} ===")  # Data Visualization
            print(f"1 - {self.localizer.get_string(300)}")  # Bar chart
            print(f"2 - {self.localizer.get_string(301)}")  # Line chart
            print(f"0 - {self.localizer.get_string(5)}")  # Return to main menu
            
            try:
                choice = input(f"\n{self.localizer.get_string(17)}: ")  # Enter your choice
                
                if choice == "0":
                    break
                elif choice in ["1", "2"]:
                    # Show available columns
                    print(f"\n{self.localizer.get_string(302)}: {', '.join(df.columns)}")
                    
                    try:
                        # Get x-axis column
                        x_col = input(f"{self.localizer.get_string(49)}: ").strip()
                        
                        # Get y-axis column(s)
                        y_cols_input = input(f"{self.localizer.get_string(50)}: ").strip()
                        y_cols = [col.strip() for col in y_cols_input.split(',')]
                        
                        # Set chart type based on choice
                        chart_type = "bar" if choice == "1" else "line"
                        
                        # Call create_plot instead of _plot_chart to ensure proper memory management
                        self.create_plot(df, x_col, y_cols, chart_type)
                        
                    except ValueError as e:
                        print(f"\n{self.localizer.get_string(51)}: {str(e)}")
                        if "must be 'line' or 'bar'" in str(e):
                            print("\nTip: Use 1 for bar chart or 2 for line chart")
                    except Exception as e:
                        error_msg = str(e)
                        if "could not convert" in error_msg.lower():
                            print(f"\n{self.localizer.get_string(52)}: Invalid data type for selected columns")
                        else:
                            print(f"\n{self.localizer.get_string(52)}: {error_msg}")
                else:
                    print(self.localizer.get_string(9))  # Invalid choice
                    
            except KeyboardInterrupt:
                print(f"\n{self.localizer.get_string(15)}")  # Operation cancelled
                break
            except Exception as e:
                print(f"\n{self.localizer.get_string(16)}: {str(e)}")  # Error occurred
        
    def _optimize_data(self, data: pd.DataFrame, x: str, y_cols: List[str], 
                      n_points: int) -> pd.DataFrame:
        """Optimize dataset size while preserving important patterns.
        
        Args:
            data: Input DataFrame
            x: X-axis column
            y_cols: Y-axis columns
            n_points: Target number of points
            
        Returns:
            Optimized DataFrame
        """
        # Only copy required columns to save memory
        df = data[[x] + y_cols].copy(deep=False)
        
        # Handle datetime x-axis
        if self._is_datetime(df[x]):
            df[x] = pd.to_datetime(df[x])
            # Remove NaT values
            df = df.dropna(subset=[x])
            # Sort by time
            df = df.sort_values(x)
            
            # Ensure non-empty dataset
            if len(df) == 0:
                raise ValueError(f"No valid datetime values found in column '{x}'")
            
            # Use dynamic binning for time series
            bins = pd.date_range(
                start=df[x].min(),
                end=df[x].max(),
                periods=n_points
            )
            
            # Use pd.cut for more efficient binning
            df['bin'] = pd.cut(df[x], bins=bins)
            
            # Aggregate using groupby once instead of loop
            agg_dict = {col: 'mean' for col in y_cols}
            agg_dict[x] = lambda x: x.iloc[0]  # Take first timestamp in bin
            
            # This vectorized approach is more memory-efficient than looping
            result = df.groupby('bin').agg(agg_dict).reset_index(drop=True)
            result = result.sort_values(x)
            
            return result
            
        # Handle numeric x-axis
        elif pd.api.types.is_numeric_dtype(df[x]):
            # Handle infinite values
            df = df.replace([np.inf, -np.inf], np.nan)
            df = df.dropna(subset=[x] + y_cols)
            
            if len(df) == 0:
                raise ValueError(f"No valid numeric values found after removing infinites and NaNs")
                
            # Use quantile-based sampling for better distribution
            quantiles = np.linspace(0, 1, n_points)
            indices = []
            
            for q in quantiles:
                q_val = df[x].quantile(q)
                idx = (df[x] - q_val).abs().idxmin()
                indices.append(idx)
                
            return df.loc[indices].sort_values(x)
            
        # Handle categorical x-axis
        else:
            # Group by x and aggregate y values
            agg_dict = {col: 'mean' for col in y_cols}
            
            if len(df) > self.MAX_POINTS:
                # For large categorical datasets, pre-aggregate before groupby
                # This can significantly improve performance
                print(f"\nOptimizing large categorical dataset with {len(df)} rows")
            
            return df.groupby(x).agg(agg_dict).reset_index()
            
    def _plot_chart(self, df: pd.DataFrame, chart_type: str, x_col: str, 
                   y_cols: List[str], sample_size: Optional[int] = None) -> None:
        """Plot a chart with optimized data handling.
        
        Args:
            df: DataFrame containing data to plot
            chart_type: Type of chart to plot ('bar' or 'line')
            x_col: X-axis column name
            y_cols: Y-axis column name(s)
            sample_size: Optional custom sample size
        """
        try:
            # Validate input data
            self._validate_data(df, x_col, y_cols)
            
            # Validate chart type
            if chart_type.lower() not in ['line', 'bar']:
                raise ValueError(f"Unsupported chart type: {chart_type}")
            
            # Add performance warning for very large datasets
            if len(df) * len(y_cols) > 1_000_000:
                try:
                    memory_mb = df.memory_usage(deep=True).sum() / 1024 / 1024
                    print(f"\nWarning: Large dataset detected ({memory_mb:.1f} MB). "
                          f"Plotting {len(df):,} points may take longer than usual.")
                except:
                    print("\nWarning: Very large dataset detected. Plotting may take longer than usual.")
                
            # Create a copy for data manipulation (shallow copy to save memory)
            plot_df = df.copy(deep=False)  # Shallow copy is sufficient here
            sampling_info = ""
            
            # Process data based on chart type
            if chart_type == "line":
                # Validate numeric y columns
                non_numeric_cols = [col for col in y_cols if not pd.api.types.is_numeric_dtype(plot_df[col])]
                if non_numeric_cols:
                    print(self.localizer.get_string(303))
                    print(f"Non-numeric columns: {', '.join(non_numeric_cols)}")
                    return
                    
                # Check for non-finite values
                for col in y_cols:
                    non_finite = pd.isna(plot_df[col]) | np.isinf(plot_df[col])
                    if non_finite.any():
                        print(f"\nWarning: {non_finite.sum()} non-finite values found in {col}. Removing them.")
                        plot_df = plot_df[~non_finite]
                
                # Handle x-axis data type
                if self._is_datetime(plot_df[x_col]) or self._is_date_column(plot_df[x_col]):
                    try:
                        plot_df[x_col] = pd.to_datetime(plot_df[x_col], errors='coerce')
                        # Drop NaT values after conversion
                        invalid_dates = plot_df[x_col].isna()
                        if invalid_dates.any():
                            print(f"\nWarning: {invalid_dates.sum()} invalid dates removed")
                        plot_df = plot_df.dropna(subset=[x_col])
                        
                        # Convert to UTC if timezone-aware
                        if hasattr(plot_df[x_col].dt, 'tz') and plot_df[x_col].dt.tz is not None:
                            plot_df[x_col] = plot_df[x_col].dt.tz_convert('UTC')
                            print("\nNote: Dates converted to UTC")
                    except Exception as e:
                        raise ValueError(f"Failed to convert {x_col} to datetime: {str(e)}")
                elif not pd.api.types.is_numeric_dtype(plot_df[x_col]):
                    try:
                        plot_df[x_col] = pd.to_numeric(plot_df[x_col])
                    except:
                        pass
                
                # Optimize data size
                if len(plot_df) > self.MAX_POINTS:
                    n_points = sample_size or self.MAX_POINTS
                    try:
                        # Try optimizing with requested sample size
                        optimized_df = self._optimize_data(plot_df, x_col, y_cols, n_points)
                        if len(optimized_df) > 0:
                            plot_df = optimized_df
                        else:
                            print(f"\nWarning: Data optimization failed, falling back to first {n_points} points")
                            plot_df = plot_df.head(n_points)
                    except Exception as e:
                        print(f"\nWarning: Data optimization failed ({str(e)}), falling back to first {n_points} points")
                        plot_df = plot_df.head(n_points)
                elif sample_size:
                    # If a specific sample size was requested but data is small enough
                    try:
                        plot_df = self._optimize_data(plot_df, x_col, y_cols, sample_size)
                    except Exception as e:
                        print(f"\nWarning: Custom sampling failed ({str(e)})")
                # else: small dataset, no optimization needed
                
                if len(plot_df) < len(df):
                    reduction = 100 * (1 - len(plot_df)/len(df))
                    sampling_info = f"\nData reduced by {reduction:.1f}%"
                    print(f"\nWarning: Large dataset detected. {sampling_info}")
                    
            else:  # bar chart
                if plot_df[x_col].nunique() > self.CATEGORY_LIMIT:
                    # Use more efficient category reduction
                    # Group and calculate sums once for efficiency
                    agg_df = plot_df.groupby(x_col)[y_cols].agg('sum')
                    
                    # Get top categories based on first y column
                    top_cats = agg_df[y_cols[0]].nlargest(self.CATEGORY_LIMIT - 1).index
                    
                    # Create Others category efficiently
                    others_sum = agg_df.loc[~agg_df.index.isin(top_cats)].sum()
                    
                    # Combine results
                    plot_df = pd.DataFrame(agg_df.loc[top_cats]).reset_index()
                    
                    # Only add Others if there are values to aggregate
                    if len(agg_df) > len(top_cats):
                        others_row = pd.DataFrame([others_sum], columns=y_cols)
                        others_row[x_col] = 'Others'
                        plot_df = pd.concat([plot_df, others_row])
                        
                    reduction = 100 * (1 - len(plot_df[x_col].unique())/len(df[x_col].unique()))
                    sampling_info = f"\nTop {self.CATEGORY_LIMIT-1} categories + Others"
                    print(f"\nWarning: Too many categories. {sampling_info}")
            
            # Create plot
            fig_width, fig_height = self._adjust_figure_size(x_col, y_cols, len(plot_df))
            plt.figure(figsize=(fig_width, fig_height))
            
            if chart_type == "line":
                # Set rcParams for faster line plotting
                with plt.rc_context({'lines.markersize': 2, 'lines.linewidth': 1}):
                    for col in y_cols:
                        plt.plot(plot_df[x_col], plot_df[col], marker='.', label=col)
            else:
                unique_cats = plot_df[x_col].unique()
                x_pos = np.arange(len(unique_cats))
                
                # Adjust width based on number of bars
                width = min(0.8, 0.8 / len(y_cols))  # Prevent bars from being too wide
                
                for i, col in enumerate(y_cols):
                    offset = (i - len(y_cols)/2 + 0.5) * width
                    # More efficient aggregation
                    agg_values = plot_df.groupby(x_col)[col].mean()
                    values = [agg_values.get(cat, 0) for cat in unique_cats]
                    
                    plt.bar(x_pos + offset, values, width, label=col)
                
                plt.xticks(x_pos, unique_cats, rotation=45, ha='right')
            
            # Format plot
            if sampling_info:
                title = f"{', '.join(y_cols)} vs {x_col}{sampling_info}"
            else:
                title = self.localizer.get_string(307).format(', '.join(y_cols), x_col)
            
            plt.title(title)
            plt.xlabel(x_col)
            plt.ylabel(', '.join(y_cols))
            plt.grid(True, alpha=0.3)
            
            if len(y_cols) > 1:
                plt.legend()
                
            plt.tight_layout()
            plt.show()
            
        except Exception as e:
            print(f"{self.localizer.get_string(52)}: {str(e)}")
            import traceback
            traceback.print_exc()
            plt.close('all')  # Ensure figures are closed even on error
            import gc
            gc.collect()  # Clean up memory
            raise
        finally:
            plt.close('all')  # More thorough than just plt.close()
            import gc
            gc.collect()
