# app.py (utama)
import streamlit as st
from retriever import search_bm25_recursive

st.set_page_config(page_title="BPK Legal Document Recursive Retriever", layout="wide")
st.title("📚 BPK Legal Document Recursive Retriever")

st.markdown("""
Sistem ini memungkinkan Anda mencari **pasal dalam dokumen hukum** yang relevan dengan kueri Anda, menggunakan algoritma **BM25** dan pelacakan **referensi pasal secara rekursif**.
""")

query = st.text_input("🔍 Masukkan pertanyaan atau topik regulasi:", "")
col1, col2 = st.columns(2)
with col1:
    topk = st.slider("📄 Jumlah dokumen awal (Top-K):", min_value=5, max_value=100, value=10, step=5)
with col2:
    max_depth = st.slider("🧩 Kedalaman referensi maksimum:", min_value=0, max_value=5, value=2)

if query:
    st.info("Menjalankan pencarian, mohon tunggu...")
    results = search_bm25_recursive(query, topk=topk, max_depth=max_depth)

    for r in results:
        depth_level = r['nomor'].count('-')
        sumber_text = (
            f"**Sumber:** Dokumen sesuai query"
            if depth_level == 0
            else f"**Dokumen Sumber:** _{r['judul']}_  \n**Pasal Sumber:** {r['tipe'].split('Pasal')[-1].strip()}"
        )

        with st.expander(f"📘 {r['nomor']} - **{r['judul']}** - Pasal **{r['pasal']}**"):
            st.markdown(f"{sumber_text}")
            st.markdown(f"**Kedalaman Referensi:** {depth_level}")
            st.markdown("**Isi:**")
            st.markdown(r['text'])
