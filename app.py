import streamlit as st
import google.generativeai as genai

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
            "max_output_tokens": 2048,
        }
        
        # Create model
        model = genai.GenerativeModel(
            model_name="gemini-1.5-flash",
            generation_config=generation_config,
        )
        
        # Start chat with system prompt
        chat = model.start_chat(history=[])
        chat.send_message(
            "Anda adalah asisten yang akan generate pertanyaan dan jawaban berdasarkan teks yang diberikan. "
            "Jenis pertanyaan dan jawaban bisa berupa pilihan ganda dan esai singkat. "
            "Selalu berikan output dalam format yang rapi dengan nomor urut untuk setiap soal."
        )
        
        return chat
    except Exception as e:
        st.error(f"Error initializing Gemini: {str(e)}")
        return None

def format_response(text):
    """Membuat respons lebih rapi
    Hasilkan soal pilihan ganda dan esai dengan format rapi Pilihan jawaban pilihan ganda berada dibawah soal dan pisahkan antar pilihan dengan jarak 1 line.
    Beri jarak 2 line antara soal dan jawaban esai.
    Format output:
                A. Soal Pilihan Ganda
                1. [Pertanyaan]
                   a. [Pilihan A]
                   b. [Pilihan B]
                   c. [Pilihan C]
                   d. [Pilihan D]

                   

                B. Soal Esai Singkat
                1. [Pertanyaan]

                C. Kunci Jawaban
                   Jawaban Pilihan Ganda: [Jawaban yang benar]
                   Jawaban Pilihan Esai: [Jawaban yang benar]
    """
    
    return text

def main():
    st.title("HERD :owl:")

    # Chat container as a placeholder to update in real-time
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

    # Input area with st.chat_input
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