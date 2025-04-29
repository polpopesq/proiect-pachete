#fisier care ia 30 de observatii din datele initiale pentru a lucra cu ceva mai light pt test

import pandas as pd

try:
    data = pd.read_csv('../data/ufo_sightings_scrubbed.csv', low_memory=False)
    data_us = data[data['country'] == 'us']
    sample_us = data_us.sample(n=30, random_state=42)
    sample_us.to_csv('../data/ufo_us_sample.csv', index=False)
    print("success")

except Exception as e:
    print(e)
