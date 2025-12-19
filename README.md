docker network create booking-network

docker run --name booking_db \
    -p 6432:5432 \
    -e POSTGRES_USER=abcde \
    -e POSTGRES_PASSWORD=abcde \
    -e POSTGRES_DB=booking \
    --network=booking-network \
    --volume pg-booking-data:/var/lib/postgresql/data \
    -d postgres:16

docker run --name booking_cache \
    -p 7379:6379 \
    --network=booking-network \
    -d redis:7.4

docker run --name booking_back \
    -p 8080:8000 \
    --network=booking-network \
    booking_image


docker run --name booking_celery_worker \
    --network=booking-network \
    booking_image \
    celery --app=src.tasks.celery_app:celery_instance worker -l INFO


docker run --name booking_celery_beat \
    --network=booking-network \
    booking_image \
    celery --app=src.tasks.celery_app:celery_instance worker -l INFO -B


docker build -t booking_image .


docker run --name booking_nginx \
    --volume ./nginx.conf:/etc/nginx/nginx.conf \
    --volume /etc/letsencrypt:/etc/letsencrypt \
    --volume /var/lib/letsencrypt:/var/lib/letsencrypt \
    --network=booking-network \
    --rm -p 80:80 nginx
    --rm -p 80:80 -p 443:443 nginx



    # ✨ Backend Fastapi

[![Python](https://img.shields.io/badge/Python-3.x-blue.svg?logo=python&logoColor=white)](https://www.python.org/)
[![FastAPI](https://img.shields.io/badge/FastAPI-0.115.5-009688.svg?logo=fastapi&logoColor=white)](https://fastapi.tiangolo.com/)
[![Pydantic](https://img.shields.io/badge/Pydantic-2.10.2-green.svg?logo=pydantic&logoColor=white)](https://pydantic.dev/)
[![Uvicorn](https://img.shields.io/badge/Uvicorn-0.32.1-f7614d.svg?logo=uvicorn&logoColor=white)](https://www.uvicorn.org/)
[![GitHub stars](https://img.shields.io/github/stars/blackgyana/backend-fastapi?style=social)](https://github.com/blackgyana/backend-fastapi/stargazers)

> Repositori ini menampung layanan API backend dasar yang dikembangkan menggunakan kerangka kerja FastAPI berkinerja tinggi dalam Python.

---

## ✨ Fitur Utama

Proyek ini, meskipun ringkas, menerapkan praktik terbaik untuk membangun fondasi API backend yang kuat dan efisien:

*   **API Berkinerja Tinggi:** Memanfaatkan FastAPI untuk membangun endpoint RESTful yang efisien dan skalabel dengan validasi data otomatis dan serialisasi/deserialisasi.
*   **Validasi Data yang Robust:** Menggunakan Pydantic untuk mendefinisikan model data yang ketat, memastikan integritas input, dan memvalidasi struktur data dengan kuat.
*   **Konfigurasi Lingkungan yang Fleksibel:** Mengelola data sensitif dan konfigurasi spesifik lingkungan melalui file `.env` menggunakan `python-dotenv`.
*   **Server Gateway Asinkron:** Didukung oleh Uvicorn, sebuah server ASGI yang cepat, untuk menyajikan API dengan kemampuan asinkron yang memanfaatkan kekuatan Python.
*   **Validasi Alamat Email:** Mengintegrasikan `email_validator` untuk penanganan dan validasi yang tepat terhadap input alamat email.
*   **Alat CLI yang Ramah Pengembang:** Menampilkan `fastapi-cli` dan `Typer` untuk alur kerja pengembangan yang ditingkatkan dan interaksi baris perintah.

## 🛠️ Tumpukan Teknologi

Proyek ini dibangun di atas tumpukan teknologi modern dan efisien:

| Kategori              | Teknologi           | Catatan                                                              |
| :-------------------- | :------------------ | :------------------------------------------------------------------- |
| **Bahasa Pemrograman** | Python              | Bahasa inti untuk logika backend dan pengembangan API.               |
| **Kerangka Kerja Web** | FastAPI             | Kerangka kerja web berkinerja tinggi untuk membangun API RESTful.    |
| **Validasi Data**     | Pydantic            | Digunakan untuk validasi data, serialisasi, dan manajemen pengaturan. |
| **Server ASGI**       | Uvicorn             | Server ASGI yang sangat cepat untuk menjalankan aplikasi FastAPI.    |
| **Manajemen Env**     | python-dotenv       | Mengelola variabel lingkungan dari file `.env`.                      |
| **Alat CLI**          | fastapi-cli, Typer  | Memfasilitasi pengembangan dan interaksi baris perintah.             |
| **Validasi Email**    | email-validator     | Untuk memastikan format email yang valid.                            |
| **Klien HTTP**        | httpx               | Klien HTTP Python yang sepenuhnya asinkron.                         |

## 🏛️ Tinjauan Arsitektur

Aplikasi ini mengadopsi arsitektur API RESTful yang sederhana dan efisien, berpusat pada kerangka kerja FastAPI. Ini dirancang sebagai layanan backend mandiri, dengan `main.py` berfungsi sebagai titik masuk utama untuk aplikasi. Arsitektur ini mempromosikan modularitas, kemampuan pengujian, dan skalabilitas dengan memisahkan kekhawatiran dan memastikan bahwa setiap endpoint API dapat dengan mudah diidentifikasi dan dikelola. Python adalah bahasa utama, memastikan pengalaman pengembangan yang bersih dan ekspresif.

## 🚀 Memulai

Ikuti langkah-langkah ini untuk menjalankan proyek secara lokal di mesin Anda.

### Prasyarat

Pastikan Anda telah menginstal yang berikut ini:

*   [Python 3.x](https://www.python.org/downloads/)
*   [pip](https://pip.pypa.io/en/stable/installation/) (biasanya disertakan dengan Python)

### Instalasi

1.  **Kloning repositori:**

    ```bash
    git clone https://github.com/blackgyana/backend-fastapi.git
    cd backend-fastapi
    ```

2.  **Buat dan aktifkan lingkungan virtual:**

    ```bash
    python -m venv venv
    # Di Windows
    .\venv\Scripts\activate
    # Di macOS/Linux
    source venv/bin/activate
    ```

3.  **Instal dependensi:**

    ```bash
    pip install -r requirements.txt
    ```

4.  **Jalankan aplikasi FastAPI:**

    ```bash
    uvicorn main:app --reload
    ```
    Atau, jika Anda ingin menggunakan alat CLI FastAPI:
    ```bash
    fastapi dev
    ```

    Aplikasi akan tersedia di `http://127.0.0.1:8000`. Dokumentasi API interaktif (Swagger UI) dapat diakses di `http://127.0.0.1:8000/docs` dan Redoc di `http://127.0.0.1:8000/redoc`.

## 📂 Struktur File

```
/
├── .gitignore
├── main.py
└── requirements.txt
```

*   **`.gitignore`**: Menentukan file dan direktori yang harus diabaikan oleh Git.
*   **`main.py`**: File utama aplikasi, yang berisi definisi aplikasi FastAPI dan endpoint API Anda.
*   **`requirements.txt`**: Daftar semua dependensi Python yang diperlukan oleh proyek ini, yang digunakan untuk menginstal paket menggunakan `pip`.
