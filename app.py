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
    options = ["List Barang","Prediksi", "Kelola Barang"]
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

elif menu == "Kelola Barang":
    st.title("📦 Kelola Data Barang")

    tab_riwayat ,tab_ubah, tab_hapus = st.tabs([ "📜 Riwayat Prediksi","✏️ Ubah Barang", "❌ Hapus Barang"])
 
    try:
        all_items_df = fetch_predictions()
    except Exception as e:
        st.error(f"Gagal memuat data barang: {e}")
        all_items_df = pd.DataFrame() 
    
    with tab_riwayat:
        st.header("Riwayat Prediksi Barang")
        if all_items_df.empty:
            st.info("Tidak ada riwayat prediksi. Silakan lakukan prediksi terlebih dahulu.")
        else:
            st.dataframe(all_items_df, use_container_width=True)
            st.download_button(
                label="Unduh Riwayat Prediksi",
                data=all_items_df.to_csv(index=False).encode('utf-8'),
                file_name='riwayat_prediksi.csv',
                mime='text/csv'
            )

    with tab_ubah:
        st.header("Pilih dan Ubah Data Barang")
        if all_items_df.empty:
            st.info("Tidak ada data barang yang bisa diubah. Silakan tambah barang terlebih dahulu.")
        else:
            item_to_edit_id = st.selectbox(
                "Pilih barang yang akan diubah:",
                options=all_items_df["id"],
                format_func=lambda x: f"ID: {x} - {all_items_df.loc[all_items_df['id'] == x, 'nama_barang'].values[0]}",
                key="select_edit"
            )
            
            selected_item = all_items_df[all_items_df["id"] == item_to_edit_id].iloc[0]

            with st.form("form_ubah_barang"):
                st.write(f"**Mengubah Data untuk ID:** {selected_item['id']}")
                
                updated_nama = st.text_input("Nama Barang", value=selected_item["nama_barang"])

                update_submitted = st.form_submit_button("Simpan Perubahan")
                if update_submitted:
                    update_prediction(
                        item_to_edit_id, updated_nama
                    )
                    st.success(f"Data barang '{updated_nama}' berhasil diperbarui!", icon="🔄")
                    st.rerun() 

    with tab_hapus:
        st.header("Hapus Data Barang")
        if all_items_df.empty:
            st.info("Tidak ada data barang yang bisa dihapus.")
        else:
            with st.form("form_hapus_barang"):
                item_to_delete_id = st.selectbox(
                    "Pilih barang yang akan dihapus:",
                    options=all_items_df["id"],
                    format_func=lambda x: f"ID: {x} - {all_items_df.loc[all_items_df['id'] == x, 'nama_barang'].values[0]}",
                    key="select_delete"
                )
                            
                delete_submitted = st.form_submit_button("Hapus Barang Ini Secara Permanen", type="primary")
                
                if delete_submitted:
                    delete_prediction(item_to_delete_id)
                    st.success(f"Barang dengan ID {item_to_delete_id} telah dihapus.", icon="🗑️")
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
