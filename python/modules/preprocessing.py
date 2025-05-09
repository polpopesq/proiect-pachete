import pandas as pd
from sklearn.preprocessing import StandardScaler
from sklearn.experimental import enable_iterative_imputer  # noqa
from sklearn.impute import IterativeImputer


def standardize_features(X, columns_to_scale):
    scaler = StandardScaler()
    X_scaled = X.copy()
    X_scaled[columns_to_scale] = scaler.fit_transform(X[columns_to_scale])
    return X_scaled

# MICE
def impute_missing_values(X, columns_to_impute):
    imputer = IterativeImputer(random_state=0)
    X_imputed = X.copy()
    X_imputed[columns_to_impute] = imputer.fit_transform(X[columns_to_impute])
    return X_imputed


def preprocess_data(data):
    # Stergere coloane inutile
    columns_to_drop = ['duration (hours/min)', 'date posted']
    data.drop(columns=[col for col in columns_to_drop if col in data.columns], inplace=True, errors='ignore')

    # Normalizare nume coloane
    data.columns = data.columns.str.strip().str.lower()

    # Conversii de tip
    data['duration (seconds)'] = pd.to_numeric(data.get('duration (seconds)'), errors='coerce')
    data['datetime'] = pd.to_datetime(data.get('datetime'), errors='coerce')
    data['latitude'] = pd.to_numeric(data.get('latitude'), errors='coerce')
    data['longitude'] = pd.to_numeric(data.get('longitude'), errors='coerce')

    # Filtru pentru SUA
    data = data[data['country'] == 'us']

    # Extragere componente temporale
    data['year'] = data['datetime'].dt.year
    data['month'] = data['datetime'].dt.month
    data['hour'] = data['datetime'].dt.hour

    # Grupare forme rare(< 100 aparitii)
    shape_counts = data['shape'].value_counts()
    common_shapes = shape_counts[shape_counts > 100].index
    data['shape_grouped'] = data['shape'].where(data['shape'].isin(common_shapes), 'other')
    data.drop(columns=['shape'], inplace=True)

    shape_values = data['shape_grouped'].dropna().unique()
    shape_encoding = {shape: idx for idx, shape in enumerate(sorted(shape_values))}
    data['shape_encoded'] = data['shape_grouped'].map(shape_encoding)

    # Imputare MICE pe coloana 'shape'
    data = impute_missing_values(data, ['shape_encoded'])

    return data
