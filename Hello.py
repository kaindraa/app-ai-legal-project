import streamlit as st

st.set_page_config(page_title="BPK Legal Assistant", layout="wide")
st.title("AI Legal Assistant")

with st.container():
    st.info("""
    Selamat datang di **BPK Legal Assistant** — sistem berbasis AI untuk menelusuri dan memahami dokumen hukum.

    📌 Silakan pilih menu di **sidebar** sebelah kiri:
    - `Legal BPK Retriever` → untuk pencarian pasal dengan BM25 dan referensi rekursif
    - `Chatbot` → untuk konsultasi langsung terhadap isi dokumen PDF yang diunggah
    """)
