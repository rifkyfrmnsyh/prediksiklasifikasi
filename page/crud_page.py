import streamlit as st
import pandas as pd
from src.db import fetch_items, create_item, update_item_name, delete_item

def show_crud_page():
    st.title("📦 Kelola Daftar Barang")

    st.cache_data.clear()
    
    try:
        items_df = fetch_items()
    except Exception as e:
        st.error(f"Gagal memuat data barang: {e}")
        items_df = pd.DataFrame(columns=['id', 'nama_barang']) 

    tab1, tab2, tab3, tab4 = st.tabs([
        "➕ Tambah Barang", 
        "📜 Lihat Semua Barang", 
        "✏️ Ubah Barang", 
        "🗑️ Hapus Barang"
    ])

    with tab1:
        st.header("Tambah Barang Baru")
        with st.form("create_form", clear_on_submit=True):
            new_item_name = st.text_input("Nama Barang Baru", placeholder="Contoh: Busi Iridium")
            submitted_create = st.form_submit_button("Tambah Barang")
            
            if submitted_create and new_item_name:
                try:
                    create_item(new_item_name)
                    st.success(f"Berhasil menambahkan '{new_item_name}'!")
                    st.rerun() 
                except Exception as e:
                    st.error(f"Gagal menambahkan barang: {e}")

    with tab2:
        st.header("Daftar Barang Saat Ini")
        if items_df.empty:
            st.info("Belum ada barang di database.")
        else:
            st.dataframe(items_df, use_container_width=True)

    with tab3:
        st.header("Ubah Nama Barang")
        if not items_df.empty:
            with st.form("update_form"):
                item_to_update_id = st.selectbox(
                    "Pilih ID Barang yang akan diubah", 
                    options=items_df['id'], 
                    format_func=lambda x: f"{x} - {items_df.loc[items_df['id'] == x, 'nama_barang'].iloc[0]}"
                )
                updated_item_name = st.text_input("Nama Barang Baru", key="update_name")
                submitted_update = st.form_submit_button("Simpan Perubahan")

                if submitted_update and item_to_update_id and updated_item_name:
                    try:
                        update_item_name(item_to_update_id, updated_item_name)
                        st.success(f"Berhasil mengubah data barang ID {item_to_update_id}!")
                        st.rerun()
                    except Exception as e:
                        st.error(f"Gagal mengubah data: {e}")
        else:
            st.info("Tidak ada barang yang bisa diubah. Silakan tambahkan barang terlebih dahulu.")

    with tab4:
        st.header("Hapus Barang")
        if not items_df.empty:
            with st.form("delete_form"):
                item_to_delete_id = st.selectbox(
                    "Pilih ID Barang yang akan dihapus", 
                    options=items_df['id'], 
                    format_func=lambda x: f"{x} - {items_df.loc[items_df['id'] == x, 'nama_barang'].iloc[0]}",
                    key="delete_select"
                )
                submitted_delete = st.form_submit_button("Hapus Barang", type="primary")

                if submitted_delete and item_to_delete_id:
                    try:
                        delete_item(item_to_delete_id)
                        st.warning(f"Berhasil menghapus barang ID {item_to_delete_id}!")
                        st.rerun()
                    except Exception as e:
                        st.error(f"Gagal menghapus data: {e}")
        else:
            st.info("Tidak ada barang yang bisa dihapus.")
