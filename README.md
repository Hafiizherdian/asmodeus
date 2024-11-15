# Implementasi AI untuk Generate Butir Soal Otomatis 📚🤖

Proyek ini bertujuan untuk mengembangkan aplikasi berbasis AI yang dapat menghasilkan butir soal otomatis (pilihan ganda dan esai singkat) berdasarkan teks yang diberikan. Aplikasi ini menggunakan **Streamlit** sebagai antarmuka pengguna dan model generatif dari **Google Generative AI**.

---

## Fitur ✨
- **Input Teks**: Masukkan teks sebagai referensi untuk pembuatan soal.
- **Generasi Soal**: AI akan menghasilkan soal pilihan ganda dan esai berdasarkan input teks.
- **Format Output**: Soal dihasilkan dalam format rapi dan dapat diunduh sebagai file `.txt`.
- **Antarmuka Sederhana**: Aplikasi berbasis web dengan tampilan yang mudah digunakan.

---

## Tools 🛠️
- **Python**: Bahasa pemrograman utama.
- **Streamlit**: Untuk membangun antarmuka web.
- **Google Generative AI (Gemini)**: Model generatif untuk pembuatan soal otomatis.
- **Streamlit Cloud**: Untuk hosting aplikasi.

---

## Cara Menjalankan Aplikasi 🚀

### 1. Menjalankan di Lokal
1. **Clone repositori**:
    ```console
    - git clone https://github.com/Hafiizherdian/asmodeus.git
    - cd asmodeus
    ```
2. **Buat virtual environment**:
    ```console
    - python -m venv venv
    - source venv/bin/activate  # Untuk Linux/Mac
    - venv\Scripts\activate     # Untuk Windows
    ```

3. **Instal dependensi**:
    ```console
    - pip install -r requirements.txt
    ```
4. **Tambahkan file `secrets.toml` : Buat folder `.streamlit` di direktori utama, lalu buat file `secrets.toml`**:
    - [GOOGLE_API_KEY]
    - GOOGLE_API_KEY = "YOUR_API_KEY"
    - ❗ API dapatkan di https://aistudio.google.com/apikey

5. **Jalankan aplikasi**:
    ```console
    - streamlit run app.py
    ```
### 2. Menjalankan di Streamlit Cloud
1. **Upload project ke GitHub.**

2. **Deploy ke Streamlit Cloud**:
    - Masuk ke Streamlit Cloud.
    - Hubungkan dengan repositori GitHub.
    - Tambahkan Google API Key di Settings > Secrets.

---

## Cara Menggunakan 🖥️
1. Buka aplikasi melalui link yang diberikan.
2. Masukkan teks di kolom input.
3. Klik tombol Generate Soal.
4. Lihat hasilnya di layar, atau unduh sebagai file teks.

---

## Struktur Folder 📂
```console
asmodeus/
- ├── app.py                 # File utama aplikasi
- ├── requirements.txt       # Dependensi Python
- ├── .streamlit/
- │   └── secrets.toml       # File API Key (lokal)
- ├── README.md              # Dokumentasi
```
---

## Masalah Umum ❗
1. ## FileNotFoundError: No secrets files found
    - Pastikan `GOOGLE_API_KEY` telah ditambahkan di **secrets Streamlit** Cloud atau file `secrets.toml` untuk **lokal**.
2. ## Invalid API Key
    - Periksa kembali `API key` yang digunakan dan pastikan sudah valid.

---

### ???
---
> When I wrote this code, 
only God and I understood what I did. 
Now only God knows.  
> – Anonymous
