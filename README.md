# MyoDiacker

Proyek MyoDiacker adalah sistem skrining stres siswa berbasis portable dan multimodal machine learning.

## Struktur Direktori

- `firmware/`
  - `platformio.ini` - konfigurasi build ESP32-S3
  - `src/` - kode C++ / Arduino untuk ESP32-S3
    - `main.cpp` - entry point firmware
    - `sensor_manager.h/cpp` - inisialisasi dan pembacaan EMG, HRV, GSR
    - `signal_processor.h/cpp` - preprocessing, ekstraksi fitur, dan classification stub
    - `led_controller.h/cpp` - kontrol LED RGB untuk status stres
    - `comm_manager.h/cpp` - komunikasi serial / data output
    - `data_types.h` - struktur data dan state

- `backend/`
  - `requirements.txt` - dependency Python
  - `app/`
    - `main.py` - FastAPI app
    - `api.py` - endpoint decision fusion
    - `schemas.py` - Pydantic request/response models
    - `decision_fusion.py` - logika fusion probabilitas
    - `models/`
      - `biosignal_model.py` - loader model Random Forest
      - `text_model.py` - loader model Naive Bayes
    - `data/`
      - `train_models.py` - kerangka training model

- `frontend/`
  - `index.html` - dashboard web
  - `styles.css` - gaya antarmuka
  - `app.js` - fetch API dan render data

## Modul Utama

1. `firmware/src/sensor_manager.*` - membaca sensor biosinyal.
2. `firmware/src/signal_processor.*` - preprocessing dan stub klasifikasi.
3. `firmware/src/led_controller.*` - output LED merah/kuning/hijau.
4. `firmware/src/comm_manager.*` - kirim status ke host via serial.
5. `backend/app/decision_fusion.py` - gabungkan model biosinyal dan teks.
6. `frontend/app.js` - panggil backend dan tampilkan hasil.

## Panduan Singkat Integrasi di VS Code

1. Buka folder `c:\Users\LENOVO\Documents\MyoDiacker` sebagai workspace.
2. Pasang ekstensi:
   - PlatformIO IDE / C/C++
   - Python
   - Pylance
   - Live Server (opsional untuk frontend)
3. `firmware/`:
   - Buka `platformio.ini`.
   - Build dan upload untuk board `esp32-s3-devkitc-1`.
4. `backend/`:
   - Buat virtual environment Python.
   - Install dependencies: `pip install -r requirements.txt`.
   - Jalankan: `uvicorn app.main:app --reload --host 0.0.0.0 --port 8000`.
5. `frontend/`:
   - Buka `frontend/index.html` dengan Live Server, atau host statis.
   - Pastikan `app.js` memanggil backend di `http://localhost:8000/api/fuse`.

## Catatan

- Semua modul saat ini masih berupa boilerplate/stub; logika sensor dan model harus diimplementasikan sesuai hardware dan dataset nyata.
- Backend menggunakan file pickle model sebagai placeholder di `app/data/`.
- Untuk integrasi akhir, sensor ESP32 dapat mengirim JSON ke backend via Wi-Fi atau BLE dan dashboard menerima hasilnya.
