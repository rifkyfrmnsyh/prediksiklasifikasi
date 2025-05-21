
import pandas as pd

def get_user_input(columns, st):
    user_input = {}
    st.text_input("Masukkan nama barang", value="")
    for col in columns:
        user_input[col] = st.number_input(f"Masukkan nilai untuk {col}", value=0.0)
    df = pd.DataFrame([user_input])

    return df
