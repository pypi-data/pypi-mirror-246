import numpy as np
from dtaidistance import dtw
import pandas as pd
import time




def calculate_dtw_batch(time_series_batch, all_time_series):
    # Initialize an empty matrix to store DTW distances for the batch
    dtw_distances_batch = np.zeros((len(time_series_batch), len(all_time_series)))

    for i, series_i in enumerate(time_series_batch):
        for j, series_j in enumerate(all_time_series[i+1:], start=i+1):
            # Ensure series_i and series_j are 1-D arrays
            series_i_1d = np.asarray(series_i).reshape(-1)
            series_j_1d = np.asarray(series_j).reshape(-1)

            # if there are NaN at the beginning or at the end of the series, remove them
            series_i_1d = series_i_1d[~np.isnan(series_i_1d)]
            series_j_1d = series_j_1d[~np.isnan(series_j_1d)]           

            # Calculate DTW distance
            distance = dtw.distance_fast(series_i_1d, series_j_1d)
            dtw_distances_batch[i][j] = distance
            dtw_distances_batch[j][i] = distance  # Reflect the distance in the symmetric position

    return dtw_distances_batch

def calculate_time(sample_size, dataset, dataset_divisor = 1):
    time_series = dataset.values

    # Sample a subset of your data
    len_dataset = len(time_series)  // dataset_divisor + 1
    sample_time_series = time_series[:sample_size]  # Assuming 'time_series' is your full dataset

    # Time the computation for the sample
    start_time = time.time()
    sample_distances = calculate_dtw_batch(sample_time_series, sample_time_series)
    end_time = time.time()
    time_for_sample = end_time - start_time

    # Number of comparisons for the sample and the full dataset
    num_comparisons_sample = sample_size * (sample_size - 1) / 2
    num_comparisons_full = len_dataset * (len_dataset - 1) / 2

    # Extrapolate to estimate total time
    estimated_total_time = time_for_sample / num_comparisons_sample * num_comparisons_full

    print(f"Time taken for sample: {time_for_sample} seconds")
    print(f"Estimated total time: {estimated_total_time / 60 } minutes")
    print(f"Estimated total time: {estimated_total_time / 60 / 60 } hours")
    print(f"Estimated total time: {estimated_total_time / 60 / 60 / 24 } days")
    
    return estimated_total_time

# if this script is called directly, run the following code
if __name__ == '__main__':
    time_series_df = pd.read_csv('./empresa4/time_series_dataset.csv', index_col=[0,1])
    calculate_time(2500, time_series_df, 10)
