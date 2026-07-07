# Aplikasi Todo Manager

Aplikasi web untuk mengelola daftar tugas (todo list) yang dibangun dengan **Flask** dan **SQLAlchemy**.

## 📋 Fitur Utama

- ✅ **Tambah Tugas** - Buat tugas baru dengan judul dan deskripsi
- 📝 **Edit Tugas** - Ubah judul dan deskripsi tugas yang ada
- ✓ **Tandai Selesai** - Tandai tugas sebagai selesai atau belum selesai
- 🗑️ **Hapus Tugas** - Hapus tugas individual atau semua tugas yang selesai
- 🔍 **Filter Tugas** - Tampilkan semua tugas, tugas aktif, atau tugas selesai
- 📊 **Statistik** - Lihat jumlah tugas total, aktif, dan selesai

---

## 🛠️ Persyaratan Sistem

Sebelum memulai, pastikan Anda telah menginstal:

- **Python 3.7 atau lebih tinggi**
- **pip** (package manager untuk Python)
- **git** (opsional, untuk clone repository)

**Cek versi Python:**
```bash
python --version
```

---

## 📦 Instalasi

### 1. Clone atau Download Project
```bash
# Jika menggunakan git
git clone <repository-url>
cd projek ap2b

# Atau buka folder project secara langsung
cd "c:\Users\yudis\projek ap2b"
```

### 2. Buat Virtual Environment (Opsional tetapi Disarankan)

**Di Windows (CMD atau PowerShell):**
```bash
python -m venv venv
venv\Scripts\activate
```

**Di macOS/Linux:**
```bash
python3 -m venv venv
source venv/bin/activate
```

### 3. Install Dependencies

Buat file `requirements.txt` dengan isi berikut:
```
Flask==2.3.0
Flask-SQLAlchemy==3.0.0
```

Kemudian install:
```bash
pip install -r requirements.txt
```

Atau install langsung:
```bash
pip install Flask Flask-SQLAlchemy
```

---

## 🚀 Menjalankan Program

### Cara 1: Menggunakan Terminal/Command Prompt

1. **Buka Terminal/Command Prompt**
   - Windows: Tekan `Win + R`, ketik `cmd` atau `powershell`
   - macOS/Linux: Buka Terminal

2. **Navigasi ke folder project:**
   ```bash
   cd c:\Users\yudis\projek ap2b
   ```

3. **Aktifkan virtual environment (jika digunakan):**
   ```bash
   # Windows
   venv\Scripts\activate
   
   # macOS/Linux
   source venv/bin/activate
   ```

4. **Jalankan aplikasi:**
   ```bash
   python app.py
   ```

5. **Buka browser:**
   - Pergi ke: `http://localhost:5000`

### Cara 2: Menggunakan VS Code

1. **Buka folder project di VS Code**
2. **Buka Terminal di VS Code** (`Ctrl + ~`)
3. **Jalankan:**
   ```bash
   python app.py
   ```
4. **Klik link di terminal atau buka browser ke `http://localhost:5000`**

### Cara 3: Menggunakan Python Run Extension

- Di VS Code, buka `app.py`
- Klik tombol **▶ Run** di sudut kanan atas
- Buka browser ke `http://localhost:5000`

---

## 📂 Struktur Project

```
projek ap2b/
│
├── app.py                 # File utama aplikasi Flask
├── requirements.txt       # Daftar dependency Python (buat sendiri)
├── todo.db               # File database SQLite (dibuat otomatis)
│
├── templates/            # Folder template HTML
│   ├── index.html        # Halaman utama (daftar tugas)
│   └── edit.html         # Halaman edit tugas
│
└── instance/             # Folder instance (folder internal Flask)
```

---

## 🔧 Konfigurasi

### Environment Variables (Opsional)

Anda bisa mengatur variabel lingkungan untuk production:

```bash
# Windows (PowerShell)
$env:SECRET_KEY = "your-secret-key"
$env:DATABASE_URL = "sqlite:///todo.db"

# Windows (CMD)
set SECRET_KEY=your-secret-key
set DATABASE_URL=sqlite:///todo.db

# macOS/Linux
export SECRET_KEY="your-secret-key"
export DATABASE_URL="sqlite:///todo.db"
```

### Konfigurasi Default

- **Secret Key:** `dev-secret-key-change-in-production` (ubah di production!)
- **Database:** `sqlite:///todo.db` (SQLite lokal)
- **Port:** `5000`
- **Debug Mode:** `True` (ubah ke `False` di production)

---

## 📖 Penggunaan

1. **Buka aplikasi** di browser: `http://localhost:5000`

2. **Tambah Tugas:**
   - Ketik judul dan deskripsi tugas
   - Klik tombol "Tambah Tugas"

3. **Edit Tugas:**
   - Klik ikon edit pada tugas
   - Ubah judul/deskripsi
   - Klik "Simpan"

4. **Tandai Selesai:**
   - Klik checkbox di samping tugas
   - Tugas akan pindah ke daftar selesai

5. **Hapus Tugas:**
   - Klik ikon hapus untuk menghapus tugas individual
   - Atau klik "Hapus Semua Selesai" untuk menghapus semua tugas selesai

6. **Filter Tugas:**
   - Gunakan tab filter: **Semua | Aktif | Selesai**

---

## 🐛 Troubleshooting

### Error: `ModuleNotFoundError: No module named 'flask'`
**Solusi:** Instal dependencies
```bash
pip install Flask Flask-SQLAlchemy
```

### Error: `Address already in use`
**Solusi:** Port 5000 sudah digunakan. Ubah port di `app.py`:
```python
if __name__ == '__main__':
    app.run(debug=True, port=5001)  # Ubah ke port lain
```

### Database tidak bisa diakses
**Solusi:** Hapus file `todo.db` dan jalankan lagi (akan membuat database baru)
```bash
del todo.db
python app.py
```

### Virtual environment tidak aktif
**Solusi:** Pastikan Anda menjalankan command aktivasi untuk OS Anda:
```bash
# Windows
venv\Scripts\activate

# macOS/Linux
source venv/bin/activate
```

---

## 📝 Catatan

- Aplikasi menggunakan **SQLite** yang cocok untuk development
- Untuk production, pertimbangkan database seperti **PostgreSQL** atau **MySQL**
- Ubah `SECRET_KEY` di production untuk keamanan lebih baik
- Atur `debug=False` di production

---

## 🤝 Kontribusi

Jika ingin melakukan perubahan atau perbaikan, silakan edit file sesuai kebutuhan.

---

## 📜 Lisensi

Aplikasi ini bebas digunakan untuk tujuan pembelajaran dan pengembangan pribadi.

---

## ❓ FAQ

**Q: Berapa lama aplikasi bisa berjalan?**
A: Selama proses Python aktif. Untuk menghentikan, tekan `Ctrl + C` di terminal.

**Q: Apakah data tersimpan?**
A: Ya, data disimpan di file `todo.db` (database SQLite).

**Q: Bisa diakses dari komputer lain?**
A: Untuk development lokal hanya bisa dari `localhost`. Untuk network lain, ubah di `app.py`:
```python
app.run(debug=True, host='0.0.0.0', port=5000)
```

---

**Selamat menggunakan Aplikasi Todo Manager! 🎉**
