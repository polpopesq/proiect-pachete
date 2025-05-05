#fisier care ia 30 de observatii din datele initiale pentru a lucra cu ceva mai light pt test

import pandas as pd
from modules.load_data import load_ufo_data
from modules.preprocessing import preprocess_data

try:
    data = load_ufo_data()
    data = preprocess_data(data)
    print("conversion successful")
    data_us = data[data['country'] == 'us']
    missing_values = data_us.isna().sum()
    print("Coloane cu valori lipsă:")
    print(missing_values[missing_values > 0])

    shape_counts = data_us['shape'].value_counts()
    print("număr forme unice (US):")
    print(shape_counts)
    common_shapes = shape_counts[shape_counts > 100].index
    data_us.loc[:, 'shape_grouped'] = data_us['shape'].where(data_us['shape'].isin(common_shapes), 'other')
    print("\nDistribuție formă grupată:")
    print(data_us['shape_grouped'].value_counts())

    sample_us = data_us.sample(n=30, random_state=42)
    sample_us.to_csv('../data/ufo_us_sample.csv', index=False)
    data_us.to_csv('../data/ufo_us.csv', index=False)
    data.to_csv('../data/ufo_all.csv', index=False)
    print("saving CSV successful")

    total_obs = len(data)
    us_obs = len(data_us)
    percentage_obs = us_obs / total_obs * 100

    print(f"Observații totale: {total_obs}")
    print(f"Observații din SUA: {us_obs}")
    print(f"Procent din SUA: {percentage_obs:.2f}%")



except Exception as e:
    print(e)
