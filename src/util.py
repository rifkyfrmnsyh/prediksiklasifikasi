# util.py

import pandas as pd
from src.db import get_item_names # Impor fungsi baru

def get_user_input(columns, st):
    user_input = {}

    list_nama_barang = get_item_names()
    
    if not list_nama_barang:
        st.warning("Tidak ada data barang di database. Silakan tambahkan melalui halaman 'Kelola Barang'.")
        st.stop()

    nama_barang = st.selectbox("Pilih nama barang", options=list_nama_barang)

    for col in columns:
        if col != 'nama_barang': 
             user_input[col] = st.number_input(f"Masukkan nilai untuk {col}", value=0.0)

    df = pd.DataFrame([user_input])
    df["nama_barang"] = nama_barang
    
    if 'nama_barang' in df.columns:
        cols = ['nama_barang'] + [col for col in df.columns if col != 'nama_barang']
        df = df[cols]
        
    return df