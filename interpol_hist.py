import numpy as np
from scipy.interpolate import interp1d
import os

def read_gnuplot_data(filepath):
    """
    Reads data from a gnuplot-formatted file.
    Assumes two columns of space-separated numerical data (x y).

    Args:
        filepath (str): The path to the gnuplot data file.

    Returns:
        tuple: A tuple containing two numpy arrays (x_data, y_data).
               Returns (None, None) if the file cannot be read or is empty.
    """
    try:
        data = np.loadtxt(filepath)
        if data.ndim == 1: # Handle case with only one row of data
            x_data = np.array([data[0]])
            y_data = np.array([data[1]])
        else:
            x_data = data[:, 0]
            y_data = data[:, 1]
        return x_data, y_data
    except Exception as e:
        print(f"Error reading file {filepath}: {e}")
        return None, None

def interpolate_y_for_x(x_data, y_data, x_target):
    """
    Finds the interpolated value of y for a given x_target.

    Args:
        x_data (np.array): The x-coordinates of the data points.
        y_data (np.array): The y-coordinates of the data points.
        x_target (float): The x-value for which to find the interpolated y.

    Returns:
        float: The interpolated y-value, or None if interpolation fails.
    """
    if x_data is None or y_data is None or len(x_data) < 2:
        print("Insufficient data for interpolation.")
        return None
    try:
        # 'linear' interpolation is generally robust. 'cubic' or 'quadratic' can be used for smoother curves.
        # 'bounds_error=False' allows extrapolation if x_target is outside the range,
        # and 'fill_value="extrapolate"' handles it.
        f_interp = interp1d(x_data, y_data, kind='quadratic', bounds_error=False, fill_value="extrapolate")
        return f_interp(x_target).item() # .item() converts numpy array to scalar
    except Exception as e:
        print(f"Error during y-interpolation for x={x_target}: {e}")
        return None

def interpolate_x_for_y(x_data, y_data, y_target):
    """
    Finds the interpolated value of x for a given y_target.
    This is done by interpolating x as a function of y.

    Args:
        x_data (np.array): The x-coordinates of the data points.
        y_data (np.array): The y-coordinates of the data points.
        y_target (float): The y-value for which to find the interpolated x.

    Returns:
        float: The interpolated x-value, or None if interpolation fails.
    """
    if x_data is None or y_data is None or len(y_data) < 2:
        print("Insufficient data for interpolation.")
        return None
    try:
        # To interpolate x for a given y, we swap x_data and y_data
        f_interp = interp1d(y_data, x_data, kind='linear', bounds_error=False, fill_value="extrapolate")
        return f_interp(y_target).item()
    except Exception as e:
        print(f"Error during x-interpolation for y={y_target}: {e}")
        return None

def main():
    file_names = ["hist_45.txt", "hist_90.txt", "hist_120.txt", "hist_180.txt"]
    all_data = {}

    # Create dummy files for demonstration if they don't exist
    for fname in file_names:
        if not os.path.exists(fname):
            print(f"Creating dummy file: {fname}")
            with open(fname, 'w') as f:
                # Generate some simple linear data for demonstration
                # In a real scenario, these files would already exist with your actual data
                for i in range(10):
                    x_val = i * 0.5
                    y_val = i * 1.2 + (float(fname.split('_')[1].split('.')[0]) / 100.0) # Add some variation based on filename
                    f.write(f"{x_val}\t{y_val}\n")

    # Read data from all files
    for filename in file_names:
        print(f"\n--- Processing {filename} ---")
        x, y = read_gnuplot_data(filename)
        if x is not None and y is not None:
            all_data[filename] = {'x': x, 'y': y}
            print(f"Successfully loaded {len(x)} data points from {filename}.")
        else:
            print(f"Failed to load data from {filename}.")

    if not all_data:
        print("No data loaded from any file. Exiting.")
        return


    # --- Part 2: Find interpolated x for a given y ---
    user_y_input = float(input("\nEnter a y-value for x-interpolation: "))
    print(f"\n--- Interpolated X values for y = {user_y_input} ---")
    for filename, data in all_data.items():
        interpolated_x = interpolate_x_for_y(data['x'], data['y'], user_y_input)
        if interpolated_x is not None:
            print(f"File: {filename}, Interpolated X: {interpolated_x:.4f}")
        else:
            print(f"File: {filename}, X-interpolation failed.")

if __name__ == "__main__":
    main()

