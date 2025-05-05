import pandas as pd
from sklearn.preprocessing import OneHotEncoder
from sklearn.compose import ColumnTransformer
from sklearn.pipeline import Pipeline
from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import train_test_split

def create_hotspot_labels(data: pd.DataFrame, top_n=100) -> pd.DataFrame:
    # Asigurare date valide
    data = data.dropna(subset=['city', 'state'])

    # Grupare pe locație și numărare
    location_counts = data.groupby(['city', 'state']).size().reset_index(name='count')
    top_locations = location_counts.nlargest(top_n, 'count')[['city', 'state']]

    # Etichetare binară
    data['hotspot'] = data.apply(
        lambda row: 1 if (row['city'], row['state']) in set([tuple(x) for x in top_locations.values]) else 0,
        axis=1
    )

    return data

def prepare_training_data(data: pd.DataFrame):
    # Extract hour from datetime
    data['hour'] = data['datetime'].dt.hour

    features = ['month', 'hour', 'shape_grouped', 'duration (seconds)', 'state']
    X = data[features]
    y = data['hotspot']

    categorical_features = ['shape_grouped', 'state']
    numeric_features = ['month', 'hour', 'duration (seconds)']

    preprocessor = ColumnTransformer(
        transformers=[
            ('cat', OneHotEncoder(handle_unknown='ignore'), categorical_features)
        ],
        remainder='passthrough'  # păstrează numeric_features
    )

    return X, y, preprocessor

def train_model(X, y, preprocessor):
    model = LogisticRegression(max_iter=1000)
    pipeline = Pipeline(steps=[
        ('preprocessing', preprocessor),
        ('classifier', model)
    ])

    # Train/test split (opțional, poți păstra totul pentru antrenare)
    X_train, _, y_train, _ = train_test_split(X, y, test_size=0.2, random_state=42)

    pipeline.fit(X_train, y_train)
    return pipeline

def run_pipeline(data: pd.DataFrame):
    data = create_hotspot_labels(data)
    X, y, preprocessor = prepare_training_data(data)
    model = train_model(X, y, preprocessor)
    return data, X, y, model
