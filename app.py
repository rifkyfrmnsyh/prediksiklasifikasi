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
from src.model import get_models, tune_model, evaluate_model
from src.util import get_user_input
from src.visualization import data_table, plot_class_distribution, plot_price_boxplot

# from page.login import login 

# if "authenticated" not in st.session_state:
#     st.session_state["authenticated"] = False

# if not st.session_state["authenticated"]:
#     login()
#     st.stop()  

df = load_data('data/DataSparePart.xlsx')

df.columns = df.columns.str.strip().str.lower().str.replace(" ", "_")

df = drop_unused_columns(df, ['nama_barang'])
df = handle_missing_values(df)

df = encode_target(df, 'harga_kelas')

st.sidebar.title("Navigasi")
menu = st.sidebar.radio("Pilih halaman", ["Visualisasi", "Prediksi"])

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
    st.title("🎯 Prediksi Kelas Harga dengan Beberapa Algoritma")
    df, scaler_dict = scale_columns(df, ['harga', 'diskon'])

    X, y = split_features_target(df, 'harga_kelas')
    

    input_df = get_user_input(X.columns, st)
    input_df = transform_input(input_df, scaler_dict) 


    data_table(input_df)
    data_table(df)

    X_train, X_test, y_train, y_test = train_test_split_data(X, y, test_size=0.2, random_state=42)

    model_names = list(get_models().keys())
    model_name = st.selectbox("Pilih algoritma", model_names)

    if st.button("Tuning dan Prediksi"):
        with st.spinner(f"Melakukan hyperparameter tuning untuk {model_name} ..."):
            model, best_params = tune_model(model_name, X_train, y_train)
        st.success("Tuning selesai!")
        st.write(f"Best params: {best_params}")

        accuracy, _ = evaluate_model(model, X_test, y_test)
        prediction = model.predict(input_df)[0]

        label_map = {0: 'Murah', 1: 'Mahal'}
        pred_label = label_map.get(prediction, 'Tidak diketahui')

        st.success(f"✅ Prediksi kelas dengan {model_name}: **{pred_label}**")
        st.info(f"📊 Akurasi model (test set): **{accuracy:.2f}**")
