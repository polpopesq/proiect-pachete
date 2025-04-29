import pandas as pd

def load_ufo_data(filepath):
    data = pd.read_csv(filepath, low_memory=False)
    return data
