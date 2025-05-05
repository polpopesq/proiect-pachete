from pathlib import Path
import pandas as pd

raw_data_csv = 'ufo_sightings_scrubbed.csv'
data_csv = 'ufo_us.csv'

def load_ufo_data(raw=False):
    base_path = Path(__file__).resolve().parent.parent.parent/'data'
    if raw:
        data = pd.read_csv(base_path/raw_data_csv, low_memory=False)
    else:
        data = pd.read_csv(base_path/data_csv, low_memory=False)
    return data
