import matplotlib.pyplot as plt
import pandas as pd
import matplotlib as mpl
import numpy as np
import matplotlib.ticker as ticker
import matplotlib.dates as mdates
from datetime import datetime
import warnings
import os
import time

# Ignore matplotlib warnings
warnings.filterwarnings("ignore", category=UserWarning, module="matplotlib")

# Configure matplotlib
mpl.rcParams['agg.path.chunksize'] = 10000
mpl.rcParams['axes.grid'] = True
mpl.rcParams['grid.alpha'] = 0.3
mpl.rcParams['figure.autolayout'] = True

class DataFrameVisualizer:
    def __init__(self, localizer):
        self.localizer = localizer
        self._cleanup_figures()

    def show_menu(self, df: pd.DataFrame):
        while True:
            print(f"\n{self.localizer.get_string(48)}")
            print(f"1. {self.localizer.get_string(300)}")
            print(f"2. {self.localizer.get_string(301)}")
            print(f"3. {self.localizer.get_string(5)}")
            try:
                choice = int(input(f"{self.localizer.get_string(17)}: "))
                if choice == 1:
                    self._plot_chart(df, "bar")
                elif choice == 2:
                    self._plot_chart(df, "line")
                else:
                    return
            except ValueError:
                print(self.localizer.get_string(9))

    def _cleanup_figures(self):
        """Clean up any existing matplotlib figures."""
        plt.close('all')
        
    def _can_show_interactive(self):
        """Check if we can show interactive plots."""
        try:
            # More thorough check for interactive backend
            backend = plt.get_backend() if hasattr(plt, 'get_backend') else 'unknown'
            
            # Check for non-interactive backends
            if backend.lower() in ['agg', 'svg', 'pdf', 'ps', 'template']:
                return False
                
            # Check for display availability
            if not os.environ.get('DISPLAY') and not 'inline' in backend.lower():
                return False
                
            # Check if running over SSH without X forwarding
            if os.environ.get('SSH_CONNECTION') and not os.environ.get('SSH_ASKPASS'):
                return False
                
            return True
        except Exception as e:
            print(f"Display check error: {str(e)}")
            return False
            
    def _generate_filename(self, chart_type, x_col, y_cols):
        """Generate a unique filename for saving the plot.
        
        Args:
            chart_type: Type of chart ('bar' or 'line')
            x_col: X-axis column name
            y_cols: List of Y-axis column names
            
        Returns:
            str: A unique filename based on time, chart type and columns
        """
        timestamp = int(time.time())
        y_str = '_'.join(y_cols) if isinstance(y_cols, list) else y_cols
        
        # Clean up column names for filenames
        x_col = x_col.replace(' ', '_').replace('/', '_')
        if isinstance(y_str, str):
            y_str = y_str.replace(' ', '_').replace('/', '_')
            
        return f"plot_{chart_type}_{x_col}_{y_str}_{timestamp}.png"
        
    def _display_plot(self, chart_type, x_col, y_cols, filename=None):
        """Display or save the plot based on environment.
        
        Args:
            chart_type: Type of chart ('bar' or 'line')
            x_col: X-axis column name
            y_cols: List of Y-axis column names
            filename: Optional filename to save plot to
        """
        try:
            # Check if we can show interactive plots
            if not self._can_show_interactive():
                # Non-interactive environment - save to file immediately
                print("\nNon-interactive environment detected. Saving plot to file...")
                self._save_plot(chart_type, x_col, y_cols, filename)
                return
                
            # Interactive environment - try to show the plot
            print(f"\n{self.localizer.get_string(311)}")
            try:
                plt.show(block=True)
            except Exception as e:
                print(f"Warning: Could not display plot interactively: {str(e)}")
                self._save_plot(chart_type, x_col, y_cols, filename)
        finally:
            # Ensure cleanup happens even if there's an error
            self._cleanup_figures()
            
    def _save_plot(self, chart_type, x_col, y_cols, filename=None):
        """Save the plot to a file with better error handling.
        
        Args:
            chart_type: Type of chart ('bar' or 'line')
            x_col: X-axis column name
            y_cols: List of Y-axis column names
            filename: Optional filename to save plot to
            
        Returns:
            bool: True if plot was saved successfully, False otherwise
        """
        try:
            if filename is None:
                filename = self._generate_filename(chart_type, x_col, y_cols)
                
            plt.savefig(filename, dpi=300, bbox_inches='tight')
            print(f"\nPlot saved to: {filename}")
            return True
        except Exception as e:
            print(f"Error saving plot: {str(e)}")
            try:
                # Try to save with a simpler filename if there was an error
                plt.savefig("plot.png")
                print("Plot saved to: plot.png")
                return True
            except:
                print("Could not save plot to file.")
                return False
        finally:
            self._cleanup_figures()
        
    def _is_date_column(self, series):
        """Check if a column contains date/time data.
        
        Args:
            series: The pandas Series to check
            
        Returns:
            bool: True if the series contains datetime data
        """
        # Check if it's already a datetime type
        if pd.api.types.is_datetime64_any_dtype(series):
            return True
            
        # Try to convert a sample to datetime
        if len(series) > 0:
            sample = series.iloc[0]
            if isinstance(sample, str):
                try:
                    pd.to_datetime(sample)
                    return True
                except:
                    pass
        return False
        
    def _adjust_figure_size(self, x_col, y_cols, data_points):
        """Determine optimal figure size based on data.
        
        Args:
            x_col: Name of x column
            y_cols: Y column name(s) - either a string or list of strings
            data_points: Number of data points
            
        Returns:
            tuple: Width and height in inches
        """
        # Start with default size
        width, height = 12, 6
        
        # Normalize y_cols to a list
        y_cols_list = y_cols if isinstance(y_cols, list) else [y_cols]
        
        # Adjust width based on number of data points and label length
        max_y_label_length = max(len(col) for col in y_cols_list)
        label_length = max(len(x_col), max_y_label_length)
        if label_length > 20:
            width += min(4, label_length / 10)  # Add up to 4 inches for long labels
            
        # Add width for multiple y columns
        if len(y_cols_list) > 1:
            width += min(8, len(y_cols_list))  # Add space for multiple columns
            
        # Adjust height if we have many data points
        if data_points > 100:
            height += 1
            
        return (width, height)
    
    def _format_axes(self, ax, x_col, y_col, plot_df, chart_type):
        """Format axes with proper scaling, grids and labels.
        
        Args:
            ax: The matplotlib axis to format
            x_col: Name of x column
            y_col: Name of y column
            plot_df: DataFrame with data
            chart_type: Type of chart ('bar' or 'line')
        """
        # Add gridlines
        ax.grid(True, which='major', linestyle='-', linewidth=0.5, alpha=0.7)
        ax.grid(True, which='minor', linestyle=':', linewidth=0.5, alpha=0.4)
        ax.minorticks_on()
        
        # Format y-axis with thousands separator for numeric columns
        if pd.api.types.is_numeric_dtype(plot_df[y_col]):
            ax.yaxis.set_major_formatter(ticker.StrMethodFormatter('{x:,.0f}'))
            
        # Handle date columns on x-axis
        is_date_x = self._is_date_column(plot_df[x_col])
        if is_date_x:
            # Convert to datetime if it isn't already
            if not pd.api.types.is_datetime64_any_dtype(plot_df[x_col]):
                plot_df[x_col] = pd.to_datetime(plot_df[x_col], errors='coerce')
                
            # Format date ticks appropriately
            date_formatter = mdates.DateFormatter('%Y-%m-%d')
            ax.xaxis.set_major_formatter(date_formatter)
            
            # Rotate date labels for better readability
            plt.setp(ax.get_xticklabels(), rotation=45, ha='right')
        elif chart_type == 'bar' or len(plot_df[x_col].astype(str).str.len().max()) > 5:
            # Rotate x labels if they're long (for bar charts or long string labels)
            plt.setp(ax.get_xticklabels(), rotation=45, ha='right')
            
        # Add some padding to avoid cutting off labels
        plt.tight_layout(pad=2.0)
        
        # Make sure tick labels don't overlap
        fig = plt.gcf()
        fig.canvas.draw()
        if chart_type == 'bar':
            # Adjust figure size if x-tick labels are too crowded
            labels = [label.get_text() for label in ax.get_xticklabels()]
            if len(labels) > 10:
                fig = plt.gcf()
                fig.set_size_inches(fig.get_size_inches()[0] * 1.2, fig.get_size_inches()[1])
                
    def create_plot(self, df, x_col, y_cols, chart_type):
        """Create a plot without user interaction.
        
        Args:
            df: DataFrame containing data to plot
            x_col: X-axis column name
            y_cols: Y-axis column name(s), string or list
            chart_type: Type of chart to plot ('bar' or 'line')
        """
        # Handle single column as string or multiple columns as list
        if isinstance(y_cols, str):
            y_cols = [y_cols]
            
        self._plot_chart(df, chart_type, x_col, y_cols)
        
    def _plot_chart(self, df: pd.DataFrame, chart_type: str, preset_x_col=None, preset_y_cols=None):
        """Plot a chart based on user input columns or preset values.
        
        Args:
            df: DataFrame containing data to plot
            chart_type: Type of chart to plot ('bar' or 'line')
            preset_x_col: Optional preset X column (for automated testing)
            preset_y_cols: Optional preset Y column(s) (for automated testing)
        """
        self._cleanup_figures()
        print(f"\n{self.localizer.get_string(302)}: {', '.join(df.columns)}")
        
        try:
            # Use preset values if provided (for automated testing)
            if preset_x_col and preset_y_cols:
                x_col = preset_x_col
                y_cols = preset_y_cols if isinstance(preset_y_cols, list) else [preset_y_cols]
                print(f"Using preset columns - X: {x_col}, Y: {', '.join(y_cols)}")
            else:
                # Get column selections from user
                x_col = input(f"{self.localizer.get_string(49)}: ").strip()
                y_col = input(f"{self.localizer.get_string(50)}: ").strip()
                
                # Support multiple y-columns (comma-separated)
                y_cols = [col.strip() for col in y_col.split(',')]
            
            # Validate column existence
            all_cols = [x_col] + y_cols
            missing_cols = [col for col in all_cols if col not in df.columns]
            if missing_cols:
                print(self.localizer.get_string(51))
                print(f"Missing columns: {', '.join(missing_cols)}")
                return
            
            # Create a copy to avoid modifying the original dataframe
            plot_df = df.copy()
            
            # Line chart specific validations and preparations
            if chart_type == "line":
                # Validate y-axis columns are numeric
                non_numeric_cols = [col for col in y_cols if not pd.api.types.is_numeric_dtype(plot_df[col])]
                if non_numeric_cols:
                    print(self.localizer.get_string(303))
                    print(f"Non-numeric columns: {', '.join(non_numeric_cols)}")
                    return
                
                # Validate x-axis can be sorted properly
                try:
                    # Check if x column is date-like
                    is_date_x = self._is_date_column(plot_df[x_col])
                    
                    if is_date_x:
                        # Convert to datetime for proper sorting
                        plot_df[x_col] = pd.to_datetime(plot_df[x_col], errors='coerce')
                    elif not pd.api.types.is_numeric_dtype(plot_df[x_col]):
                        # Try to convert to numeric if possible (for better sorting)
                        try:
                            plot_df[x_col] = pd.to_numeric(plot_df[x_col])
                        except:
                            pass
                    
                    # Sort by x-axis for better line visualization
                    plot_df = plot_df.sort_values(by=x_col)
                    
                    # Limit data points for performance
                    if len(plot_df) > 200:
                        print(self.localizer.get_string(304))
                        # More intelligent sampling - keep extremes and sample the middle
                        n_samples = 198  # 198 + 2 endpoints = 200
                        if pd.api.types.is_numeric_dtype(plot_df[x_col]) or is_date_x:
                            # Keep min and max points
                            min_idx = plot_df[x_col].idxmin()
                            max_idx = plot_df[x_col].idxmax()
                            endpoints = plot_df.loc[[min_idx, max_idx]]
                            
                            # Sample the rest
                            middle = plot_df.drop([min_idx, max_idx])
                            if len(middle) > n_samples:
                                middle = middle.sample(n=n_samples)
                            
                            # Combine and resort
                            plot_df = pd.concat([endpoints, middle])
                            plot_df = plot_df.sort_values(by=x_col)
                        else:
                            plot_df = plot_df.sample(n=200)
                except Exception as e:
                    # If sorting fails, just proceed with original data
                    print(f"Warning: {str(e)}")
                    plot_df = df.copy()
                    if len(plot_df) > 200:
                        plot_df = plot_df.sample(n=200)
            
            # Determine optimal figure size
            fig_width, fig_height = self._adjust_figure_size(x_col, y_cols, len(plot_df))
            
            # Create a new figure
            plt.figure(figsize=(fig_width, fig_height))
            ax = plt.gca()
            
            # Plot based on chart type
            if chart_type == "bar":
                if len(y_cols) == 1:
                    # Single y column
                    plot_df.plot.bar(x=x_col, y=y_cols[0], ax=ax, rot=0)
                else:
                    # Multiple y columns - group them
                    plot_df.plot.bar(x=x_col, y=y_cols, ax=ax, rot=0)
            else:
                if len(y_cols) == 1:
                    # Single y column line plot
                    plot_df.plot.line(x=x_col, y=y_cols[0], marker='o', ax=ax)
                else:
                    # Multiple y columns - each gets its own line
                    plot_df.plot.line(x=x_col, y=y_cols, marker='o', ax=ax)
            
            # Set title and labels using localized strings
            if len(y_cols) == 1:
                plt.title(self.localizer.get_string(307).format(y_cols[0], x_col))
            else:
                # Multiple columns - use a generic title
                cols_str = ', '.join(y_cols)
                plt.title(self.localizer.get_string(307).format(cols_str, x_col))
                
            plt.xlabel(x_col)
            
            if len(y_cols) == 1:
                plt.ylabel(y_cols[0])
            else:
                plt.ylabel(', '.join(y_cols))
            
            # Format axes with proper scaling, grids and labels
            self._format_axes(ax, x_col, y_cols[0], plot_df, chart_type)
            
            # Display or save the plot
            self._display_plot(chart_type, x_col, y_cols)
            # Cleanup is now handled in _display_plot and _save_plot
            
        except Exception as e:
            print(f"{self.localizer.get_string(52)}: {str(e)}")
            self._cleanup_figures()
