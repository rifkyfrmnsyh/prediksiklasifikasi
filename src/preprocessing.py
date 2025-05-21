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
    scaler_dict = {}
    for col in columns:
        scaler = StandardScaler()
        df[[col]] = scaler.fit_transform(df[[col]])
        scaler_dict[col] = scaler
    return df, scaler_dict


def transform_input(input_df, scaler_dict):
    for col, scaler in scaler_dict.items():
        if col in input_df.columns:
            input_df[[col]] = scaler.transform(input_df[[col]])
    return input_df