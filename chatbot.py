import streamlit as st
import fitz  # PyMuPDF
import tiktoken

st.set_page_config(page_title="Legal Chatbot", layout="wide")
st.title("🤖 Chatbot Konsultasi Regulasi")

st.markdown("Unggah dokumen hukum (.pdf) dan ajukan pertanyaan seputar isinya.")

uploaded_file = st.file_uploader("📎 Unggah Dokumen PDF", type=["pdf"])
query = st.text_input("❓ Ajukan pertanyaan:")

def extract_pdf_text(file):
    with fitz.open(stream=file.read(), filetype="pdf") as doc:
        return "\n".join([page.get_text() for page in doc])

if uploaded_file:
    full_text = extract_pdf_text(uploaded_file)
    st.success("✅ Dokumen berhasil diproses")
    
    if query:
        # Untuk saat ini, tampilkan dummy response
        st.markdown("**Jawaban (dummy):**")
        st.markdown(f"Kamu bertanya: _{query}_")
        st.markdown("Namun fitur pemahaman konteks belum diaktifkan (butuh LangChain/OpenAI integration).")
