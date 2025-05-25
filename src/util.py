# src/util.py
import pandas as pd

def get_user_input(columns, st):
    user_input = {}
    nama_barang = st.text_input("Masukkan nama barang", value="")

    for col in columns:
        user_input[col] = st.number_input(f"Masukkan nilai untuk {col}", value=0.0)

    df = pd.DataFrame([user_input])
    df["nama_barang"] = nama_barang
    return df
