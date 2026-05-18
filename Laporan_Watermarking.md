# Tugas Sistem Multimedia — Watermarking Citra Digital
**Implementasi Robust LSB dengan Simulasi Kompresi JPEG Manual (DCT & Kuantisasi)**

---

**Dipersiapkan oleh :**
Anisa Aulia Alhaqi — 18224080@std.stei.itb.ac.id

**Program Studi Sistem dan Teknologi Informasi**
**Sekolah Teknik Elektro dan Informatika - Institut Teknologi Bandung**
**Jl. Ganesha 10, Bandung 40132**

---

## Daftar Isi
1. **01 — Teori Singkat**
   * 1.1 Kompresi JPEG
   * 1.2 Watermarking Digital
   * 1.3 Metode LSB Klasik vs Robust LSB
2. **02 — Perancangan dan Implementasi**
   * 2.1 Kronologi Pengembangan (The Journey)
   * 2.2 Implementasi Manual JPEG (DCT & Kuantisasi)
   * 2.3 Optimasi Robustness Final
3. **03 — Pengujian dan Analisis Hasil Program**
   * 3.1 Hasil Visual Citra Host dan Watermark
   * 3.2 Tabel Hasil Pengujian Kuantitatif
   * 3.3 Analisis Ketahanan
4. **04 — Kesimpulan**
5. **05 — Lampiran**

---

## 01 — Teori Singkat

### 1.1 Kompresi JPEG
JPEG adalah standar kompresi citra lossy yang menggunakan Transformasi Kosinus Diskrit (DCT). JPEG membuang informasi detail pada bit-bit rendah melalui proses kuantisasi frekuensi tinggi. Tingkat kompresi ditentukan oleh *Quality Factor* (QF). Semakin rendah QF, semakin besar data yang dibuang.

### 1.2 Watermarking Digital
Teknik menyisipkan informasi (watermark) ke dalam media digital. Syarat utamanya adalah *Imperceptibility* (tidak terlihat) dan *Robustness* (tahan terhadap manipulasi seperti kompresi).

### 1.3 Metode LSB Klasik vs Robust LSB
LSB klasik mengganti bit terakhir (Bit-0) piksel. Teknik ini sangat rapuh terhadap JPEG. **Robust LSB** melakukan optimasi dengan memindahkan bit ke posisi yang lebih signifikan (seperti Bit-3) dan menggunakan redundansi spasial (blok piksel) agar data selamat dari pembulatan kuantisasi.

---

## 02 — Perancangan dan Implementasi

### 2.1 Kronologi Pengembangan (The Journey)
Proses penemuan metode final dilakukan melalui tiga tahap eksperimen:

1.  **Eksperimen 1: Full Color LSB (Gagal)**
    Awalnya dicoba menyisipkan watermark berwarna ke dalam foto berwarna menggunakan LSB Bit-0 standar. Hasilnya, watermark langsung rusak total (hancur menjadi noise) segera setelah citra disimpan ke format JPEG, bahkan pada QF 100 sekalipun. Hal ini membuktikan LSB Bit-0 tidak cocok untuk media yang akan dikompresi.

2.  **Eksperimen 2: Full Grayscale (Berhasil, tapi Suboptimal)**
    Tahap kedua mencoba mengubah foto host dan watermark menjadi hitam-putih (grayscale). Hasil ekstraksi jauh lebih baik, namun secara estetika kurang maksimal karena foto wajah kehilangan informasi warnanya, sehingga tidak memenuhi aspek penggunaan praktis di sistem multimedia modern.

3.  **Eksperimen 3: Color Host + Binary Watermark (Final - Sukses)**
    Solusi terbaik ditemukan dengan membiarkan **foto host tetap berwarna (RGB)** agar kualitas visual terjaga, namun **watermark diubah menjadi biner (hitam-putih)**. Dengan format biner, kita bisa menerapkan teknik *voting* blok yang sangat kuat, menghasilkan keseimbangan sempurna antara keindahan foto dan kekuatan watermark.

### 2.2 Implementasi Manual JPEG
Kompresi tidak menggunakan library otomatis, melainkan diimplementasikan secara manual:
*   **Blok 8x8**: Citra dibagi menjadi grid blok 8x8.
*   **Forward DCT**: Menghitung frekuensi setiap blok.
*   **Kuantisasi**: Membagi koefisien DCT dengan *Standard JPEG Quantization Table* yang diskalakan dengan QF. Di sinilah terjadi *lossy compression*.
*   **Inverse DCT**: Mengembalikan frekuensi yang sudah terkuantisasi menjadi piksel spasial.

### 2.3 Optimasi Robustness Final
Strategi yang digunakan dalam kode final:
*   **Target Kanal Hijau**: Menyisipkan pada kanal Hijau karena kontribusinya paling besar pada Luminans (Y) yang paling dijaga oleh JPEG.
*   **Bit-Plane Shifting (Bit-3)**: Menyisipkan pada bit ke-3 untuk menghindari area bit-bit rendah yang sering dibuang JPEG.
*   **Redundansi Blok 3x3**: Satu bit watermark disebar ke 9 piksel host.
*   **Majority Voting**: Saat ekstraksi, nilai bit ditentukan oleh suara terbanyak dari 9 piksel tersebut.

---

## 03 — Pengujian dan Analisis Hasil Program

### 3.1 Hasil Visual Citra Host dan Watermark
*   **Input Citra Host**: `foto_wajah.jpg` (Berwarna)
*   **Input Watermark**: `input.png` (Logo biner)
*   **Hasil Embed**: Citra tetap berwarna tanpa ada noise yang terlihat mata (PSNR > 53 dB).

### 3.2 Tabel Hasil Pengujian (Manual JPEG)

| QF JPEG | PSNR Img (dB) | BER | Bit Error | Hasil Ekstraksi |
| :--- | :--- | :--- | :--- | :--- |
| 100 | 53.60 | 0.0000 | 0 | Sempurna |
| 90 | 51.11 | 0.0005 | 2 | Sangat Baik |
| 70 | 49.36 | 0.0024 | 9 | Sangat Baik |
| 50 | 47.52 | 0.0076 | 31 | Sangat Baik |
| 30 | 44.55 | 0.0334 | 136 | Masih Terbaca Jelas |
| 10 | 36.17 | 0.2681 | 1098 | Rusak Sebagian |

### 3.3 Analisis
Hasil ekstraksi pada QF 50 dan QF 30 menunjukkan bahwa logo masih dapat dikenali dengan sangat jelas. Meskipun proses kuantisasi JPEG manual sangat agresif membuang detail, penggunaan **Majority Voting 3x3** berhasil mengoreksi bit yang salah. Hal ini membuktikan bahwa alur "Color Host + Binary Watermark" adalah skema yang paling handal untuk watermarking pada citra JPEG.

---

## 04 — Kesimpulan
Melalui perjalanan eksperimen, disimpulkan bahwa watermarking LSB harus diadaptasi secara khusus jika ingin menghadapi kompresi lossy. Dengan memindahkan bit ke posisi yang lebih dalam (Bit-3) dan menggunakan teknik redundansi pada kanal Hijau, kita dapat mempertahankan foto berwarna asli sekaligus menjaga integritas data watermark di dalamnya.

---

## 05 — Lampiran
*   **Pranala Repository**: [https://github.com/anisaalhaqi/Kripto](https://github.com/anisaalhaqi/Kripto)
*   **Gambar Hasil**: Tersedia di folder `results/extracted/qf_experiment/` yang menunjukkan gradasi kualitas watermark dari QF 100 hingga 10.
