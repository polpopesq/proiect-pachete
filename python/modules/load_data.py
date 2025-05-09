from pathlib import Path
import pandas as pd

raw_data_csv = 'ufo_sightings_scrubbed.csv'

def load_ufo_data():
    base_path = Path(__file__).resolve().parent.parent.parent/'data'
    data = pd.read_csv(base_path/raw_data_csv, low_memory=False)
    return data
