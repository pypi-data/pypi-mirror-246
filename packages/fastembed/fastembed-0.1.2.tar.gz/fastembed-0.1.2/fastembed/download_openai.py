import numpy as np
import pandas as pd
import requests


# Function to fetch data
def fetch_data(base_url: str, offset: int, length: int) -> pd.DataFrame:
    """Fetch data from the provided URL and return a DataFrame."""
    response = requests.get(f"{base_url}&offset={offset}&length={length}")
    response.raise_for_status()  # Raises an HTTPError if the HTTP request returned an unsuccessful status code
    return pd.DataFrame(response.json())


# Function to save DataFrame as Parquet
def save_as_parquet(df: pd.DataFrame, filename: str):
    """Save DataFrame as a Parquet file."""
    df.to_parquet(filename, index=False)


# Base URL without offset and length parameters
base_url = "https://datasets-server.huggingface.co/rows?dataset=KShivendu%2Fdbpedia-entities-openai-1M&config=default&split=train"

# Parameters
total_rows = 500
batch_size = 100  # Number of rows per request
parquet_files = []  # List to keep track of parquet file names

# Fetch data in batches and save as Parquet files
for offset in range(0, total_rows, batch_size):
    length = min(batch_size, total_rows - offset)  # Adjust length for the last batch if necessary
    df = fetch_data(base_url, offset, length)
    filename = f"data_{offset}_{offset+length}.parquet"
    save_as_parquet(df, filename)
    parquet_files.append(filename)

# Read the Parquet files, concatenate them into a single DataFrame, and convert to NumPy array
combined_df = pd.concat([pd.read_parquet(file) for file in parquet_files], ignore_index=True)
np_array = combined_df.to_numpy()

# Save NumPy array as a pickle file
np.save("combined_data.npy", np_array)  # The file is saved in the current working directory
np.save("combined_data.npy", np_array)  # The file is saved in the current working directory
