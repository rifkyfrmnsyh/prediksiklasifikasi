# src/db.py
import mysql.connector

def get_connection():
    return mysql.connector.connect(
        host="localhost",
        user="root",
        password="",
        database="prediksiklasifikasi"
    )

def check_user_credentials(username, password):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM users WHERE username=%s AND password=%s", (username, password))
    result = cursor.fetchone()
    cursor.close()
    conn.close()
    return result is not None

def save_prediction(username, input_df, prediction_label):
    conn = get_connection()
    cursor = conn.cursor()

    nama_barang = input_df["nama_barang"].values[0]
    harga = input_df["harga"].values[0]
    diskon = input_df["diskon"].values[0]

    sql = """
        INSERT INTO predictions (username, nama_barang, harga, diskon, prediction_label)
        VALUES (%s, %s, %s, %s, %s)
    """
    cursor.execute(sql, (
        username,
        nama_barang,
        harga,
        diskon,
        prediction_label
    ))

    conn.commit()
    cursor.close()
    conn.close()

def fetch_predictions(username):
    conn = get_connection()
    cursor = conn.cursor()

    query = """
        SELECT nama_barang, harga, diskon, prediction_label
        FROM predictions
        WHERE username = %s
        ORDER BY timestamp DESC
    """
    cursor.execute(query, (username,))
    results = cursor.fetchall()

    cursor.close()
    conn.close()
    return results
