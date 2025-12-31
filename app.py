# app.py

import streamlit as st
import pandas as pd

from src.data_loader import load_data
from src.preprocessing import (
    encode_target,
    scale_columns,
    handle_missing_values,
    split_features_target,
    train_test_split_data,
    transform_input
)

from src.db import save_prediction, fetch_predictions, update_prediction, delete_prediction
from src.model import tune_model, evaluate_model
from src.util import get_user_input, get_harga_modal

from page.login import login
from page.crud_page import show_crud_page # <-- Impor fungsi halaman CRUD

if "authenticated" not in st.session_state:
    st.session_state["authenticated"] = False

if not st.session_state["authenticated"]:
    login()
    st.stop()  

df = load_data('data/DataSparePart.xlsx')

df.columns = df.columns.str.strip().str.lower().str.replace(" ", "_")

# Hapus 'nama_barang' dari drop_unused_columns karena akan digunakan di input
# df = drop_unused_columns(df, ['nama_barang'])
df = handle_missing_values(df)

df = encode_target(df, 'harga_kelas')

st.sidebar.title("Navigasi")

role = st.session_state.get("role", "user") 
if role == "admin":
    # Tambahkan opsi "Kelola Barang" untuk admin
    options = ["List Barang", "Prediksi", "Riwayat Prediksi", "Kelola Barang"]
else:
    options = ["List Barang"]

menu = st.sidebar.radio("Pilih halaman", options)

if st.sidebar.button("🔒 Keluar"):
    for key in ["authenticated", "username", "role"]:
        if key in st.session_state:
            del st.session_state[key]
    st.success("Anda telah keluar.")
    st.rerun()

# --- Logika Navigasi ---
if menu == "Prediksi":
    st.title("🎯 Prediksi Kelas Harga")

    # Kolom numerik yang akan di-scale
    numeric_cols = ['harga', 'diskon']
    df, scaler_dict = scale_columns(df, numeric_cols)
    
    # Pisahkan fitur dan target
    # 'nama_barang' tidak boleh ada di X saat melatih model
    X, y = split_features_target(df.drop(columns=['nama_barang']), 'harga_kelas')

    # Dapatkan input dari pengguna
    input_df = get_user_input(X.columns, st)
    
    # Siapkan input untuk model (tanpa 'nama_barang')
    input_df_model = input_df.drop(columns=['nama_barang'], errors="ignore")
    input_df_model = transform_input(input_df_model, scaler_dict)

    X_train, X_test, y_train, y_test = train_test_split_data(X, y, test_size=0.2, random_state=42)

    model_name = "Gaussian Naive Bayes"

    if st.button("Prediksi"):
        st.spinner("Melatih model...") 

        harga_jual = input_df["harga"].values[0]
        nama_barang = input_df["nama_barang"].values[0]
        harga_modal = get_harga_modal(nama_barang)

        keuntungan = ((harga_jual - harga_modal) / harga_modal) * 100

        if keuntungan < 10:
            label_profit = "Murah"
        else:
            label_profit = "Mahal"

        from src.model import get_models, evaluate_model

        model = get_models()[model_name]  # Ambil model default
        model.fit(X_train, y_train)       # Latih model

        accuracy, _ = evaluate_model(model, X_test, y_test)
        prediction = model.predict(input_df_model)[0]

        label_map = {0: 'Murah', 1: 'Mahal'}
        pred_label = label_map.get(prediction, 'Tidak diketahui')

        st.success(f"✅ Prediksi kelas: **{pred_label}**")
        st.info(f"📊 Akurasi model: **{accuracy:.2f}**")

        st.write(f"💰 Harga Modal: Rp {harga_modal:,.0f}")
        st.write(f"📈 Keuntungan: {keuntungan:.2f}%")
        st.success(f"📌 Klasifikasi Keuntungan: **{label_profit}**")

        if "username" in st.session_state:
            save_prediction(
                input_df,
                pred_label,
            )


elif menu == "Riwayat Prediksi":
    st.title("📜 Riwayat Prediksi")

    if "username" not in st.session_state:
        st.warning("Anda belum login.")
        st.stop()

    df_predictions = fetch_predictions()

    if df_predictions.empty:
        st.info("Tidak ada riwayat prediksi yang ditemukan.")
    else:
        edited_df = st.data_editor(
            df_predictions,
            column_config={
                "id": st.column_config.Column(disabled=True),
                # Anda bisa menambahkan konfigurasi lain di sini
            },
            num_rows="dynamic",
            use_container_width=True,
            key="data_editor_riwayat"
        )

        if st.button("Simpan Perubahan"):
            for _, row in edited_df.iterrows():
                update_prediction(
                    row["id"],
                    row["nama_barang"],
                    row["harga"],
                    row["diskon"],
                    row["prediction_label"]
                )
            st.success("Semua data berhasil diperbarui.")
            st.rerun()

        # Opsi Hapus
        if not edited_df.empty:
            delete_id = st.selectbox("Pilih ID untuk dihapus:", edited_df["id"])
            if st.button("Hapus Baris", type="primary"):
                delete_prediction(delete_id)
                st.warning("Data berhasil dihapus.")
                st.rerun()


elif menu == "Kelola Barang":
    show_crud_page()


elif menu == "List Barang":
    if "username" not in st.session_state:
        st.warning("Anda belum login.")
        st.stop()
    st.success("Selamat Datang! Di SparePart Aldi Motor",   icon="👋")
    st.title("List Barang")
    df_display = load_data('data/DataSparePart.xlsx')
    df_display = df_display.drop(columns=['harga_kelas'], errors='ignore')

    st.dataframe(df_display.head(9))
