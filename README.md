# Robust LSB Watermarking System

Sistem watermarking foto wajah yang kokoh terhadap kompresi JPEG menggunakan metode LSB yang dioptimasi (Bit-3, redundansi blok 3x3, dan sistem voting).

## Fitur
- **Foto Berwarna**: Foto utama tetap mempertahankan warna aslinya (RGB).
- **Watermark Biner**: Menggunakan gambar biner (hitam-putih) untuk ketahanan maksimal.
- **Optimasi Robustness**: Menggunakan channel Hijau (Green) dan Bit-3 agar tahan terhadap kompresi JPEG hingga QF rendah.
- **Evaluasi Otomatis**: Menghitung PSNR dan BER secara otomatis untuk berbagai tingkat kualitas JPEG.

## Struktur Folder
```
.
├── data/               # Input: Letakkan foto utama dan watermark di sini
├── results/            # Output: Hasil eksperimen dan ekstraksi
├── run_experiment.py   # Script utama untuk menjalankan simulasi & evaluasi
├── extract_watermark.py # Script untuk mengekstrak watermark dari file tertentu
├── utils.py            # Fungsi inti watermarking
├── requirements.txt    # Library yang diperlukan
└── README.md           # Dokumentasi ini
```

## Persiapan
1. Pastikan Anda memiliki Python 3.x.
2. Install library yang dibutuhkan:
   ```bash
   pip install -r requirements.txt
   ```
3. Siapkan file di folder `data/`:
   - Foto utama: `foto_wajah.jpg`
   - Watermark: `input.png`

## Cara Penggunaan

### 1. Menjalankan Eksperimen & Evaluasi
Jalankan script ini untuk menyisipkan watermark dan menguji ketahanannya terhadap berbagai kualitas JPEG (QF 100 sampai 10):
```bash
python run_experiment.py
```
Hasil visualisasi dan data metrik akan muncul di folder `results/`.

### 2. Mengekstrak Watermark dari File Tertentu
Untuk mengekstrak watermark dari file gambar tertentu (misal file yang sudah dikompres):
1. Buka `extract_watermark.py`.
2. Sesuaikan variabel `TARGET_FILE` dengan path file Anda.
3. Jalankan:
```bash
python extract_watermark.py
```
Hasil ekstraksi akan disimpan di `results/extracted_from_...png`.

## Metrik
- **PSNR (Peak Signal-to-Noise Ratio)**: Mengukur kualitas visual gambar (makin tinggi makin baik).
- **BER (Bit Error Rate)**: Mengukur tingkat kesalahan ekstraksi watermark (makin rendah makin baik, 0.0 = sempurna).
