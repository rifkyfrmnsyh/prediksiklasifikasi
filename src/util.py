import pandas as pd

def get_user_input(columns, st):
    user_input = {}

    list_nama_barang = [
        "Kampas Rem", 
        "Oli Mesin", 
        "Busi", 
        "Filter Udara", 
        "Aki", 
        "Lampu Depan"
    ]

    nama_barang = st.selectbox("Pilih nama barang", options=list_nama_barang)

    for col in columns:
        user_input[col] = st.number_input(f"Masukkan nilai untuk {col}", value=0.0)

    df = pd.DataFrame([user_input])
    df["nama_barang"] = nama_barang
    return df
