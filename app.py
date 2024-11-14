import streamlit as st
import google.generativeai as genai

# Set page config
st.set_page_config(page_title="Generator Soal AI", layout="wide")

# Initialize session state
if 'chat_session' not in st.session_state:
    st.session_state.chat_session = None
if 'api_key' not in st.session_state:
    st.session_state.api_key = None

def initialize_gemini(api_key):
    # Configure API
    genai.configure(api_key=api_key)
    
    # Model configuration
    generation_config = {
        "temperature": 1,
        "top_p": 0.95,
        "top_k": 40,
        "max_output_tokens": 8192,
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

def main():
    st.title("Generator Soal dengan AI")
    
    # Sidebar untuk input API key
    with st.sidebar:
        st.header("Pengaturan")
        
        if st.button("Reset Chat"):
            st.session_state.chat_session = None
            st.experimental_rerun()
    
    # Main content
    st.write("Masukkan teks untuk generate soal:")
    
    # Text input area
    user_input = st.text_area("Teks Input", height=200)
    
    # Generate button
    if st.button("Generate Soal"):
        if not st.session_state.api_key:
            st.error("Mohon masukkan API Key terlebih dahulu!")
            return
            
        if user_input:
            try:
                # Initialize model if not already done
                if st.session_state.chat_session is None:
                    st.session_state.chat_session = initialize_gemini(st.session_state.api_key)
                
                # Prepare prompt
                prompt = f"""
                Berdasarkan teks berikut, buatkan soal-soal beserta jawabannya:

                {user_input}

                Buatkan kombinasi soal pilihan ganda dan esai singkat. 
                Format output:
                A. Soal Pilihan Ganda
                1. [Pertanyaan]
                   a. [Pilihan A]
                   b. [Pilihan B]
                   c. [Pilihan C]
                   d. [Pilihan D]
                   Jawaban: [Jawaban yang benar]

                B. Soal Esai Singkat
                1. [Pertanyaan]
                   Jawaban: [Jawaban yang benar]
                """
                
                # Generate response
                response = st.session_state.chat_session.send_message(prompt)
                
                # Display response
                st.subheader("Hasil Generate:")
                st.write(response.text)
                
                # Download button for results
                st.download_button(
                    label="Download Hasil",
                    data=response.text,
                    file_name="hasil_generate_soal.txt",
                    mime="text/plain"
                )
                
            except Exception as e:
                st.error(f"Terjadi kesalahan: {str(e)}")
                if "invalid api key" in str(e).lower():
                    st.error("API Key tidak valid. Mohon periksa kembali API Key Anda.")
        else:
            st.warning("Mohon masukkan teks terlebih dahulu!")

if __name__ == "__main__":
    main()