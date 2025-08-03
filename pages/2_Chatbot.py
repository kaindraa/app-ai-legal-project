import streamlit as st
import fitz  # PyMuPDF

st.set_page_config(page_title="Chatbot PDF", layout="wide")
st.title("Chatbot Dokumen Hukum")

st.markdown("Unggah dokumen hukum (.pdf) lalu ajukan pertanyaan untuk memahami isinya.")

uploaded_file = st.file_uploader("Unggah PDF", type=["pdf"])
query = st.text_input("Pertanyaan:")

def extract_pdf_text(file):
    with fitz.open(stream=file.read(), filetype="pdf") as doc:
        return "\n".join([page.get_text() for page in doc])

if uploaded_file:
    full_text = extract_pdf_text(uploaded_file)
    st.success("Dokumen berhasil diproses")
    
    if query:
        st.markdown("**Jawaban (sementara dummy):**")
        st.markdown(f"Pertanyaan kamu: _{query}_")
        st.markdown("Fitur pemrosesan PDF akan ditambahkan.")
