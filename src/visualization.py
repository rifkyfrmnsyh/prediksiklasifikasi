# src/visualization.py

import matplotlib.pyplot as plt
import seaborn as sns
import streamlit as st
import pandas

def data_table(df):
    st.dataframe(df.head())

def plot_class_distribution(df, target_column='harga_kelas'):
    st.subheader("Distribusi Harga Kelas")
    fig, ax = plt.subplots()
    sns.countplot(x=target_column, data=df, ax=ax)
    st.pyplot(fig)

def plot_price_boxplot(df, price_column='harga', target_column='harga_kelas'):
    if price_column in df.columns:
        st.subheader("Boxplot modal per Harga Kelas")
        fig, ax = plt.subplots()
        sns.boxplot(x=target_column, y=price_column, data=df, ax=ax)
        st.pyplot(fig)
    else:
        st.warning(f"Kolom '{price_column}' tidak ditemukan.")
