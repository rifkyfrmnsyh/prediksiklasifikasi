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

def update_prediction(id, nama_barang):
    supabase.table("predictions").update({
        "nama_barang": nama_barang,
    }).eq("id", id).execute()

def fetch_items():
    response = supabase.table("items").select("id, nama_barang").order("id").execute()
    return pd.DataFrame(response.data)

def create_item(nama_barang):
    data = {"nama_barang": nama_barang}
    supabase.table("items").insert(data).execute()

def update_item_name(item_id, new_nama_barang):
    supabase.table("items").update({"nama_barang": new_nama_barang}).eq("id", item_id).execute()

def delete_item(item_id):
    supabase.table("items").delete().eq("id", item_id).execute()

def get_item_names():
    response = supabase.table("items").select("nama_barang").execute()
    if response.data:
        return [item['nama_barang'] for item in response.data]
    return []
