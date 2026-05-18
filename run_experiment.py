"""
run_experiment.py — Eksperimen 1: Pengaruh Quality Factor JPEG (Optimized Version)
Membuktikan grafik penurunan kualitas watermark seiring turunnya QF JPEG.
"""

import cv2
import numpy as np
import matplotlib.pyplot as plt
import os
from utils import (
    load_image, load_watermark,
    embed_lsb, extract_lsb,
    calculate_psnr, calculate_ber, get_file_size_kb,
    show_watermark_comparison, plot_metrics_table,
    apply_manual_jpeg
)

IMAGE_PATH     = 'data/foto_wajah.jpg'
WATERMARK_PATH = 'data/input.png'
WM_SIZE        = (64, 64)
LOCATION       = 'top-left'
QUALITY_FACTORS = [100, 90, 80, 70, 50, 30, 10]

os.makedirs('results/watermarked', exist_ok=True)
os.makedirs('results/compressed', exist_ok=True)
os.makedirs('results/extracted/qf_experiment', exist_ok=True)

print("=" * 65)
print("RUNNING: EKSPERIMEN 1 — Pengaruh Quality Factor JPEG (MANUAL DCT)")
print("=" * 65)

# KUNCI UTAMA: Kita load sebagai COLOR untuk mempertahankan warna asli
image = load_image(IMAGE_PATH, mode='color')

# Load watermark
if os.path.exists(WATERMARK_PATH):
    watermark = load_watermark(WATERMARK_PATH, WM_SIZE)
else:
    print(f"Error: {WATERMARK_PATH} tidak ditemukan.")
    exit()

# --- EMBEDDING ---
watermarked = embed_lsb(image, watermark, location=LOCATION)
wm_png_path = 'results/watermarked/watermarked_BASE.png'
cv2.imwrite(wm_png_path, watermarked)

# Verifikasi Awal (Wajib 0.0)
extracted_verify = extract_lsb(watermarked, WM_SIZE, location=LOCATION)
ber_verify = calculate_ber(watermark, extracted_verify)
print(f"[VERIFIKASI] BER In-Memory Array: {ber_verify}")
if ber_verify != 0.0:
    print("✗ PERINGATAN: Deteksi kegagalan fungsi dasar LSB!")
    exit()
print("✓ Fungsi dasar aman. Memulai proses kompresi JPEG MANUAL...\n")

results = []
extracted_wms = []
qf_labels = []

print(f"{'QF':>5} | {'PSNR Img':>10} | {'BER':>8} | {'Error Bits':>11} | {'File Size':>10} | Status")
print("-" * 75)

for qf in QUALITY_FACTORS:
    compressed_path = f'results/compressed/compressed_qf{qf}.jpg'

    # KOMPRESI MANUAL: Menggunakan DCT dan Kuantisasi di blok 8x8
    compressed = apply_manual_jpeg(watermarked, quality=qf)

    # Simpan fisik ke disk (untuk estimasi ukuran file hasil kompresi)
    encode_param = [int(cv2.IMWRITE_JPEG_QUALITY), qf]
    cv2.imwrite(compressed_path, compressed, encode_param)

    # Ekstraksi
    extracted = extract_lsb(compressed, WM_SIZE, location=LOCATION)

    # Metrik
    psnr_img   = calculate_psnr(watermarked, compressed)
    ber        = calculate_ber(watermark, extracted)
    error_bits = int(ber * WM_SIZE[0] * WM_SIZE[1])
    file_size  = get_file_size_kb(compressed_path)

    # Simpan hasil ekstraksi gambar
    extracted_img_path = f'results/extracted/qf_experiment/extracted_qf{qf}.png'
    cv2.imwrite(extracted_img_path, (extracted * 255).astype(np.uint8))

    results.append([qf, psnr_img, ber, error_bits, f"{file_size} KB"])
    extracted_wms.append(extracted)
    qf_labels.append(f"QF={qf}\nBER={ber}")

    if ber == 0.0: status = "✓ SEMPURNA"
    elif ber < 0.08: status = "✓ Sangat Baik"
    elif ber < 0.20: status = "✓ Masih Terbaca"
    elif ber < 0.38: status = "~ Rusak Sebagian"
    else: status = "✗ Hancur / Noise"

    print(f"{qf:>5} | {psnr_img:>10} | {ber:>8} | {error_bits:>11} | {file_size:>6} KB  {status}")

# --- VISUALISASI ---
fig1 = show_watermark_comparison(
    original_wm=watermark, extracted_wms=extracted_wms, labels=qf_labels,
    title="Eksperimen 1: Kualitas Watermark Hasil Ekstraksi vs QF JPEG (Manual DCT)"
)
fig1.savefig('results/exp1_watermark_extraction.png', dpi=150, bbox_inches='tight')

qf_vals   = [r[0] for r in results]
ber_vals  = [r[2] for r in results]
psnr_vals = [r[1] for r in results]

fig2, (ax1, ax2) = plt.subplots(1, 2, figsize=(12, 4.5))
fig2.suptitle('Analisis Karakteristik Ketahanan Watermarking LSB (Manual DCT)', fontsize=13, fontweight='bold')

ax1.plot(qf_vals, ber_vals, 'ro-', linewidth=2, markersize=7)
ax1.axhline(y=0.5, color='gray', linestyle='--', alpha=0.5, label='BER 0.5 (Noise)')
ax1.set_xlabel('Quality Factor (QF)')
ax1.set_ylabel('Bit Error Rate (BER)')
ax1.set_title('Kurva BER vs Quality Factor')
ax1.set_ylim(-0.05, 0.55)
ax1.invert_xaxis()
ax1.grid(True, alpha=0.3)
ax1.legend()

ax2.plot(qf_vals, psnr_vals, 'bs-', linewidth=2, markersize=7)
ax2.set_xlabel('Quality Factor (QF)')
ax2.set_ylabel('PSNR (dB)')
ax2.set_title('Kualitas Gambar (PSNR) vs Quality Factor')
ax2.invert_xaxis()
ax2.grid(True, alpha=0.3)

plt.tight_layout()
fig2.savefig('results/exp1_ber_psnr_chart.png', dpi=150, bbox_inches='tight')

columns = ['QF', 'PSNR Gambar (dB)', 'BER', 'Bit Error', 'Ukuran File']
data_rows = [[str(r[0]), str(r[1]), str(r[2]), str(r[3]), r[4]] for r in results]
fig3 = plot_metrics_table(data_rows, columns, title="Tabel Hasil Pengujian Kuantitatif (Manual DCT)")
fig3.savefig('results/exp1_table.png', dpi=150, bbox_inches='tight')

print("\n" + "=" * 65)
print("PROSES SELESAI! Tiga file visualisasi sukses disimpan di folder 'results/'")
print("=" * 65)
# plt.show()
