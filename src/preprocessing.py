from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler

def handle_missing_values(df):
    df = df.dropna()
    return df

def split_features_target(df, target_column='harga_kelas'):
    X = df.drop(columns=[target_column])
    y = df[target_column]
    return X, y    

def train_test_split_data(X, y, test_size=0.2, random_state=42):
    return train_test_split(X, y, test_size=test_size, random_state=random_state)

def drop_unused_columns(df, columns_to_drop):
    df.drop(columns=columns_to_drop, axis=1, inplace=True)
    return df

def encode_target(df, target_column):
    df[target_column] = df[target_column].map({'Murah': 0, 'Mahal': 1})
    return df

def scale_columns(df, columns):
    scaler = StandardScaler()
    df[[columns]] = scaler.fit_transform(df[[columns]])
    return df, scaler