import pandas as pd
from sklearn.linear_model import LogisticRegression
from sklearn.preprocessing import OneHotEncoder
from sklearn.model_selection import train_test_split

def create_hotspot_labels(data: pd.DataFrame, top_n=100) -> pd.DataFrame:
    location_counts = data.groupby(['city', 'state']).size().reset_index(name='count')
    top_locations = location_counts.nlargest(top_n, 'count')[['city', 'state']]
    top_set = set([tuple(x) for x in top_locations.values])
    data['hotspot'] = data.apply(lambda row: 1 if (row['city'], row['state']) in top_set else 0, axis=1)
    return data

def prepare_training_data(data: pd.DataFrame):
    features = ['month', 'hour', 'duration (seconds)', 'shape_grouped', 'state']
    X = data[features]
    y = data['hotspot']

    categorical = ['shape_grouped', 'state']
    encoder = OneHotEncoder(sparse_output=False, handle_unknown='ignore')
    encoded = encoder.fit_transform(X[categorical])
    encoded_df = pd.DataFrame(encoded, columns=encoder.get_feature_names_out(categorical), index=X.index)

    X_final = pd.concat([X.drop(columns=categorical), encoded_df], axis=1)
    return X_final, y

def train_model(X, y):
    model = LogisticRegression(max_iter=1000)
    X_train, _, y_train, _ = train_test_split(X, y, test_size=0.2, random_state=42)
    model.fit(X_train, y_train)
    return model

def run_simple_logistic(data: pd.DataFrame):
    data = create_hotspot_labels(data)
    X, y = prepare_training_data(data)
    model = train_model(X, y)
    return data, X, y, model
