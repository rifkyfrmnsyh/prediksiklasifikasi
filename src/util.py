
import pandas as pd

def get_user_input(columns, st):
    user_input = {}
    for col in columns:
        user_input[col] = st.number_input(f"Masukkan nilai untuk {col}", value=0)
    return pd.DataFrame([user_input])
