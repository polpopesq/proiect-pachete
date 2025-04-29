import pandas as pd

def preprocess_data(data):
    # longitude avea spatiu la final
    data.columns = data.columns.str.strip().str.lower()

    data['datetime'] = pd.to_datetime(data['datetime'], errors='coerce')
    data['month'] = data['datetime'].dt.month
    data['latitude'] = pd.to_numeric(data['latitude'], errors='coerce')
    data['longitude'] = pd.to_numeric(data['longitude'], errors='coerce')
    return data.dropna(subset=['latitude', 'longitude'])
