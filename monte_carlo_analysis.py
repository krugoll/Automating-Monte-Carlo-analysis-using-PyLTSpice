import numpy as np
import matplotlib.pyplot as plt
import csv
from scipy.signal import find_peaks
from PyLTSpice import RawRead

# --- Configuration ---
# 1. Set the path to your LTspice output file
RAW_FILE_PATH = "first_proposed_inductor_oscillator.raw"  

# 2. Set the name of the signal you want to analyze (e.g., V(out), V(n001))
SIGNAL_NAME = "V(out)"
OUTPUT_CSV_FILE = "frequencies.csv"

# --- Script ---

def calculate_frequency_peak_finding(time_data, signal_data):
    """Calculates the average frequency of a signal using peak finding."""
    # Find the indices of all the peaks in the signal
    # We set the height to the signal's mean to avoid issues with DC offsets
    try:
        peaks, _ = find_peaks(signal_data, height=np.mean(signal_data))
        
        # If fewer than 2 peaks are found, oscillation is unstable or not present
        if len(peaks) < 2:
            return None # Return None to indicate failure

        # Calculate the time differences between consecutive peaks
        periods = np.diff(time_data[peaks])
        
        # Calculate the average period and then the frequency
        avg_period = np.mean(periods)
        frequency = 1 / avg_period
        return frequency
    except Exception:
        return None # Return None on any error during calculation

def main():
    """
    Main function to run the Monte Carlo analysis.
    """
    print(f"Reading Monte Carlo data from: {RAW_FILE_PATH}")
    
    try:
        # Open and parse the .raw file
        ltr = RawRead(RAW_FILE_PATH)
        num_steps = ltr.get_steps()
        print(f"Found {len(num_steps)} simulation steps.")

        frequencies = []
        failed_runs = 0

        # Loop through each step of the Monte Carlo simulation
        for i in num_steps:
            # Get the time and signal data for the current step
            time = ltr.get_trace('time').get_wave(step=i)
            signal = ltr.get_trace(SIGNAL_NAME).get_wave(step=i)
            
            # Calculate frequency for the current run
            freq = calculate_frequency_peak_finding(time, signal)
            
            if freq is not None:
                frequencies.append(freq)
            else:
                failed_runs += 1

        print(f"\nSuccessfully analyzed {len(frequencies)} runs.")
        if failed_runs > 0:
            print(f"Warning: {failed_runs} runs failed to produce a stable oscillation.")

        # --- Plotting the Histogram ---
        if frequencies:
    # Convert list of frequencies from Hz to MHz
          frequencies_mhz = [f / 1e6 for f in frequencies]
          with open(OUTPUT_CSV_FILE, 'w', newline='') as csvfile:
                writer = csv.writer(csvfile)
                # Write a header row
                writer.writerow(['Frequency (MHz)'])
                # Write the frequency data, each value on a new row
                for freq_mhz in frequencies_mhz:
                    writer.writerow([freq_mhz])
            
          print(f"\nSuccessfully saved {len(frequencies_mhz)} data points to {OUTPUT_CSV_FILE}")
          

          plt.figure(figsize=(10, 6))
          plt.hist(frequencies_mhz, bins='auto', color='skyblue', edgecolor='black')
    
    # --- UPDATED SECTION ---
    # Calculate statistics in MHz
          mean_freq_mhz = np.mean(frequencies_mhz)
          std_dev_mhz = np.std(frequencies_mhz)
    
    # Update the plot to use MHz values and labels
          plt.axvline(mean_freq_mhz, color='red', linestyle='dashed', linewidth=2, label=f'Mean: {mean_freq_mhz:.3f} MHz')
    
          plt.title('Monte Carlo Analysis of Oscillator Frequency')
          plt.xlabel('Frequency (MHz)') # Changed label to MHz
          plt.ylabel('Number of Runs')
          plt.legend()
          plt.grid(axis='y', alpha=0.75)
    
    # Update the print statements to show MHz
          print(f"\nMean Frequency: {mean_freq_mhz:.3f} MHz")
          print(f"Standard Deviation: {std_dev_mhz:.3f} MHz")
    
          plt.show()

    except FileNotFoundError:
        print(f"Error: The file '{RAW_FILE_PATH}' was not found.")
    except Exception as e:
        print(f"An error occurred: {e}")

if __name__ == "__main__":
    main()