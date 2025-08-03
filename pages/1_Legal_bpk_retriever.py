import streamlit as st
from retriever import search_bm25_recursive

st.set_page_config(page_title="BPK Legal Document Recursive Retriever", layout="wide")
st.title("BPK Legal Document Recursive Retriever")

st.markdown("""
Sistem ini memungkinkan Anda mencari **pasal dalam dokumen hukum dari Badan Pengelola Keuangan Tema 49** yang relevan dengan kueri Anda, menggunakan algoritma **BM25** dan pelacakan **referensi pasal secara rekursif**.
""")

if "results" not in st.session_state:
    st.session_state.results = None
if "last_query" not in st.session_state:
    st.session_state.last_query = ""

with st.form("query_form", clear_on_submit=True):
    query = st.text_input("🔍 Masukkan pertanyaan atau topik regulasi:")
    col1, col2 = st.columns([1, 1])
    with col1:
        topk = st.slider("📄 Jumlah dokumen awal (Top-K):", min_value=5, max_value=100, value=10, step=5)
    with col2:
        max_depth = st.slider("🧩 Kedalaman referensi maksimum:", min_value=0, max_value=5, value=2)
    submitted = st.form_submit_button("Cari")

if submitted and query:
    st.session_state.last_query = query
    st.session_state.results = search_bm25_recursive(query, topk=topk, max_depth=max_depth)

if st.session_state.results and st.session_state.last_query:
    st.subheader(f"Hasil untuk: _{st.session_state.last_query}_")
    for r in st.session_state.results:
        depth_level = r['nomor'].count('-')
        sumber_text = (
            f"**Sumber:** Dokumen sesuai query"
            if depth_level == 0
            else f"**Dokumen Sumber:** _{r['judul']}_  \n**Pasal Sumber:** {r['tipe'].split('Pasal')[-1].strip()}"
        )

        with st.expander(f"{r['nomor']} - {r['judul']} - Pasal {r['pasal']}"):
            st.markdown(sumber_text)
            st.markdown(f"**Kedalaman Referensi:** {depth_level}")
            st.markdown(r['text'])
