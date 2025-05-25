import streamlit as st

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

from src.db import save_prediction, fetch_predictions
from src.model import get_models, tune_model, evaluate_model
from src.util import get_user_input
from src.visualization import data_table, plot_class_distribution, plot_price_boxplot

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
menu = st.sidebar.radio("Pilih halaman", ["Visualisasi", "Prediksi", "Riwayat Prediksi"])

if menu == "Visualisasi":
    st.title("📑 Tabel Data")
    data_table(df)

    st.title("📊 Statistik Deskriptif")
    st.write(df.describe())

    st.title("📈 Visualisasi Data")
    plot_class_distribution(df)
    st.write(df['harga_kelas'].value_counts())
    plot_price_boxplot(df)

elif menu == "Prediksi":
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
                st.session_state["username"],
                input_df,
                pred_label,
            )


elif menu == "Riwayat Prediksi":
    st.title("🕒 Riwayat Prediksi")

    if "username" not in st.session_state:
        st.warning("Anda belum login.")
        st.stop()

    from src.db import fetch_predictions

    username = st.session_state["username"]
    results = fetch_predictions(username)

    if not results:
        st.info("Belum ada prediksi yang tersimpan.")
    else:
        import pandas as pd
        df_pred = pd.DataFrame(results, columns=["nama_barang", "harga", "diskon", "prediction_label"])
        st.dataframe(df_pred)

