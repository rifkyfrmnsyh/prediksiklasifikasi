import streamlit as st
import pandas as pd

from src.data_loader import load_data
from src.preprocessing import (
    encode_target,
    scale_columns,
    handle_missing_values,
    drop_unused_columns,
    split_features_target,
    train_test_split_data,
    transform_input
)

from src.db import save_prediction, fetch_predictions, update_prediction, delete_prediction
from src.model import tune_model, evaluate_model
from src.util import get_user_input

from page.login import login 

if "authenticated" not in st.session_state:
    st.session_state["authenticated"] = False

if not st.session_state["authenticated"]:
    login()
    st.stop()  

df = load_data('data/DataSparePart.xlsx')

df.columns = df.columns.str.strip().str.lower().str.replace(" ", "_")

df = drop_unused_columns(df, ['nama_barang'])
df = handle_missing_values(df)

df = encode_target(df, 'harga_kelas')

st.sidebar.title("Navigasi")

role = st.session_state.get("role", "user") 
if role == "admin":
    options = ["List Barang","Prediksi", "Riwayat Prediksi"]
else:
    options = ["List Barang"]

menu = st.sidebar.radio("Pilih halaman", options)

if st.sidebar.button("🔒 Keluar"):
    for key in ["authenticated", "username", "role"]:
        if key in st.session_state:
            del st.session_state[key]
    st.success("Anda telah keluar.")
    st.rerun()

if menu == "Prediksi":
    st.title("🎯 Prediksi Kelas Harga")

    df, scaler_dict = scale_columns(df, ['harga', 'diskon'])
    X, y = split_features_target(df, 'harga_kelas')

    input_df = get_user_input(X.columns, st)
    input_df_model = input_df.drop(columns=['nama_barang'], errors="ignore")
    input_df_model = transform_input(input_df_model, scaler_dict)

    X_train, X_test, y_train, y_test = train_test_split_data(X, y, test_size=0.2, random_state=42)

    model_name = "Gaussian Naive Bayes"

    if st.button("Tuning dan Prediksi"):
        with st.spinner("Melakukan hyperparameter tuning untuk Gaussian Naive Bayes ..."):
            model, best_params = tune_model(model_name, X_train, y_train)
        st.success("Tuning selesai!")
        st.write(f"Best params: {best_params}")

        accuracy, _ = evaluate_model(model, X_test, y_test)
        prediction = model.predict(input_df_model)[0]

        label_map = {0: 'Murah', 1: 'Mahal'}
        pred_label = label_map.get(prediction, 'Tidak diketahui')

        st.success(f"✅ Prediksi kelas: **{pred_label}**")
        st.info(f"📊 Akurasi model: **{accuracy:.2f}**")

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

    df = fetch_predictions()

    if df.empty:
        st.info("Tidak ada riwayat prediksi yang ditemukan.")
    else:
        edited_df = st.data_editor(
            df,
            column_config={"id": st.column_config.Column(disabled=True)},
            num_rows="dynamic",
            use_container_width=True
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

        delete_id = st.selectbox("Pilih ID untuk dihapus:", df["id"])
        if st.button("Hapus Baris"):
            delete_prediction(delete_id)
            st.warning("Data berhasil dihapus.")
            st.rerun()

elif menu == "List Barang":
    if "username" not in st.session_state:
        st.warning("Anda belum login.")
        st.stop()
    st.success("Selamat Datang! Di SparePart Aldi Motor",   icon="👋")
    st.title("List Barang")
    df = load_data('data/DataSparePart.xlsx')
    df = df.drop(columns=['harga_kelas'], errors='ignore')


    st.dataframe(df.head(9))

