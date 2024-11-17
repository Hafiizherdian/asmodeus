import streamlit as st
import google.generativeai as genai
import re

# Set page config
st.set_page_config(page_title="Implementasi AI Generate butir soal otomatis", layout="wide")

# Initialize session state
if 'chat_history' not in st.session_state or not isinstance(st.session_state.chat_history, list):
    st.session_state.chat_history = []
if 'chat_session' not in st.session_state:
    st.session_state.chat_session = None

def initialize_gemini():
    try:
        # Cek apakah API key ada di secrets
        if "GOOGLE_API_KEY" not in st.secrets:
            st.error("API Key tidak ditemukan. Silakan tambahkan API Key di Streamlit Secrets.")
            return None
        
        # Mengambil API key dari secrets
        api_key = st.secrets["GOOGLE_API_KEY"]
        
        # Configure API
        genai.configure(api_key=api_key)
        
        # Model configuration
        generation_config = {
            "temperature": 1,
            "top_p": 0.95,
            "top_k": 40,
            "max_output_tokens":  4096,
        }
        
        # Create model
        model = genai.GenerativeModel(
            model_name="gemini-1.5-flash",
            generation_config=generation_config,
        )
        
        # Start chat dengan systems prompt
        chat = model.start_chat(history=[])
        chat.send_message(
        "Anda adalah asisten yang akan membuat soal pilihan ganda dan esai singkat berdasarkan teks yang diberikan. "
        "Berikan output dengan format:\n"
        "A. Soal Pilihan Ganda\n"
        "   1. [Pertanyaan]\n"
        "       A). [Pilihan A]\n"
        "       B). [Pilihan B]\n"
        "       C). [Pilihan C]\n"
        "       D). [Pilihan D]\n\n"
        "B. Soal Esai Singkat\n"
        "   1. [Pertanyaan]\n\n"
        "C. Kunci Jawaban\n"
        "   Jawaban Pilihan Ganda:\n"
        "   [Daftar jawaban yang benar, nomor dan huruf pilihan]\n"
        "   Jawaban Esai Singkat:\n"
        "   [Daftar jawaban esai singkat]\n\n"
        "Berikan nomor urut untuk setiap soal dan pisahkan setiap bagian dengan jelas."
        )

        
        return chat
    except Exception as e:
        st.error(f"Error initializing Gemini: {str(e)}")
        return None

def format_response(text):
    """
    Memformat respons model ke dalam format yang diinginkan.
    """
    # Memisahkan setiap opsi jawaban (a., b., c., d.) ke baris baru
    formatted_text = re.sub(r'([a-d]\.)', r'\n\1', text.strip())

    # Tambahkan dua spasi di akhir setiap baris untuk mendukung line break di Markdown
    formatted_text = formatted_text.replace("\n", "  \n")

    # Memisahkan bagian soal dan kunci jawaban
    soal_bagian = formatted_text.split("Kunci Jawaban:")
    soal_dan_jawaban = soal_bagian[0].strip()
    kunci_jawaban = soal_bagian[1].strip() if len(soal_bagian) > 1 else "Kunci jawaban tidak ditemukan."

    # Format ulang menjadi output rapi
    return f"""
    **Soal Pilihan Ganda dan Esai**  
    {soal_dan_jawaban}  

    **Kunci Jawaban**  
    {kunci_jawaban}
    """
    

def main():
    st.title("HERD :owl:")

    # Chat container sebagai placeholder untuk update secara real-time
    chat_container = st.empty()

    # menampilkan chat history secara dinamis
    with chat_container.container():
        for chat in st.session_state.chat_history:
            if isinstance(chat, dict) and "message" in chat:
                if chat["role"] == "user":
                    st.chat_message("user").markdown(chat["message"])
                else:
                    st.chat_message("assistant").markdown(format_response(chat["message"]))
            else:
                st.warning("Item chat tanpa kunci 'message' ditemukan.")

    # Input area dengan st.chat_input
    prompt = st.chat_input("Masukkan teks untuk generate soal...")
    if prompt:
        # Append user message to chat history
        st.session_state.chat_history.append({"role": "user", "message": prompt})
        
        # Initialize the model if not yet initialized
        if st.session_state.chat_session is None:
            st.session_state.chat_session = initialize_gemini()
            if st.session_state.chat_session is None:
                st.error("Gagal menginisialisasi model.")
                return
        
        try:
            # Get response dari model
            response = st.session_state.chat_session.send_message(prompt)
            st.session_state.chat_history.append({"role": "assistant", "message": response.text})

            # update otomatis chat setelah response
            with chat_container.container():
                for chat in st.session_state.chat_history:
                    if isinstance(chat, dict) and "message" in chat:
                        if chat["role"] == "user":
                            st.chat_message("user").markdown(chat["message"])
                        else:
                            st.chat_message("assistant").markdown(format_response(chat["message"]))
                    else:
                        st.warning("Item chat tanpa kunci 'message' ditemukan.")
        
        except Exception as e:
            st.error(f"Terjadi kesalahan: {str(e)}")

if __name__ == "__main__":
    main()