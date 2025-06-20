from supabase import create_client
import streamlit as st
import os
import pandas as pd

SUPABASE_URL = 'https://aqompvrswnzqkluqeybm.supabase.co'
SUPABASE_KEY = 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6ImFxb21wdnJzd256cWtsdXFleWJtIiwicm9sZSI6ImFub24iLCJpYXQiOjE3NTA0MjY0NjEsImV4cCI6MjA2NjAwMjQ2MX0.Oj9xAmCThp_9e1_pXwWNLGKSJbkNmLrpeAU2MQRNi0s'

supabase = create_client(SUPABASE_URL, SUPABASE_KEY)

def check_user_credentials(username, password):
    result = supabase.table("account") \
        .select("role") \
        .eq("username", username) \
        .eq("password", password) \
        .execute()
    
    st.write("DEBUG:", result)

    if result.data:
        return result.data[0]["role"]
    return None


def save_prediction(input_df, prediction_label):
    data = {
        "nama_barang": input_df["nama_barang"].values[0],
        "harga": float(input_df["harga"].values[0]),
        "diskon": float(input_df["diskon"].values[0]),
        "prediction_label": prediction_label
    }

    supabase.table("predictions").insert(data).execute()

def fetch_predictions():
    response = supabase.table("predictions").select("*").order("id", desc=True).execute()
    return pd.DataFrame(response.data)

def delete_prediction(id):
    supabase.table("predictions").delete().eq("id", id).execute()

def update_prediction(id, nama_barang, harga, diskon, label):
    supabase.table("predictions").update({
        "nama_barang": nama_barang,
        "harga": float(harga),
        "diskon": float(diskon),
        "prediction_label": label
    }).eq("id", id).execute()
