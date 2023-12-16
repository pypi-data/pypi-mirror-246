import numpy as np
from dtaidistance import dtw
import pandas as pd

def calculate_dtw_batch(time_series_batch):
    # Initialize an empty matrix to store DTW distances for the batch
    dtw_distances_batch = np.zeros((len(time_series_batch), len(time_series_batch)))

    for i, series_i in enumerate(time_series_batch):
        for j, series_j in enumerate(time_series_batch[i+1:], start=i+1):
            # Ensure series_i and series_j are 1-D arrays
            series_i_1d = np.asarray(series_i).reshape(-1)
            series_j_1d = np.asarray(series_j).reshape(-1)

            # Remove NaN values at the beginning or at the end of the series
            series_i_1d = series_i_1d[~np.isnan(series_i_1d)]
            series_j_1d = series_j_1d[~np.isnan(series_j_1d)]

            # Calculate DTW distance
            distance = dtw.distance_fast(series_i_1d, series_j_1d)
            dtw_distances_batch[i][j] = distance
            dtw_distances_batch[j][i] = distance  # Reflect the distance in the symmetric position

    return dtw_distances_batch

def calculate_distances(sample_size, dataset):
    # Convert the dataset to NumPy array if it's a DataFrame
    if isinstance(dataset, pd.DataFrame):
        time_series = dataset.values
    else:
        time_series = np.array(dataset)

    # Sample a subset of your data
    total_indices = np.arange(len(time_series))
    sample_indices = np.random.choice(total_indices, sample_size, replace=False)
    left_out_indices = np.setdiff1d(total_indices, sample_indices)
    
    sample_time_series = time_series[sample_indices]

    # Calculate the DTW distances for the sample
    distances = calculate_dtw_batch(sample_time_series)

    return distances, sample_indices, left_out_indices

def save_distances_to_csv(distances, file_name):
    # Convert the distances matrix to a pandas DataFrame
    distances_df = pd.DataFrame(distances)

    # Save the DataFrame to a CSV file
    distances_df.to_csv(file_name, index=False)

# if this script is called directly, run the following code
if __name__ == '__main__':
    time_series_df = pd.read_csv('./empresa4/time_series_dataset.csv', index_col=[0,1])
    distances, sampled_indices, left_out_indices = calculate_distances(len(time_series_df) // 10, time_series_df)
    print("Distance matrix calculated for the sample.")
    
    # Save the distances to a CSV file
    save_distances_to_csv(distances, '~/buckets/b1/datasets/distances.csv')
    print("Distances saved to 'distances.csv'.")
