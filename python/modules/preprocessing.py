import pandas as pd

def preprocess_data(data):
    data.drop(columns=['duration (hours/min)', 'date posted'], inplace=True)
    data.columns = data.columns.str.strip().str.lower()

    data['duration (seconds)'] = pd.to_numeric(data['duration (seconds)'], errors='coerce')
    data['datetime'] = pd.to_datetime(data['datetime'], errors='coerce')
    data['latitude'] = pd.to_numeric(data['latitude'], errors='coerce')
    data['longitude'] = pd.to_numeric(data['longitude'], errors='coerce')

    data = data[data['country'] == 'us']

    data = data.dropna(subset=['datetime', 'latitude', 'longitude', 'city', 'state', 'shape'])

    data['year'] = data['datetime'].dt.year
    data['month'] = data['datetime'].dt.month
    data['hour'] = data['datetime'].dt.hour

    shape_counts = data['shape'].value_counts()
    common_shapes = shape_counts[shape_counts > 100].index
    data['shape_grouped'] = data['shape'].where(data['shape'].isin(common_shapes), 'other')

    return data