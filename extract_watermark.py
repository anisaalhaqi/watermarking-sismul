"""
extract_specific.py — Script untuk mengekstrak watermark dari file tertentu.
"""

import cv2
import numpy as np
import os
from utils import extract_lsb

# Konfigurasi
TARGET_FILE = 'data/watermarked_BASE-q50.jpg'
WM_SIZE = (64, 64)
LOCATION = 'top-left'
OUTPUT_FILE = 'results/extracted_from_q50.png'

os.makedirs('results', exist_ok=True)

if not os.path.exists(TARGET_FILE):
    print(f"Error: File {TARGET_FILE} tidak ditemukan!")
    exit()

print(f"Sedang mengekstrak watermark dari: {TARGET_FILE}...")

# Load gambar (Color)
image = cv2.imread(TARGET_FILE, cv2.IMREAD_COLOR)

if image is None:
    print(f"Error: Gagal membaca file {TARGET_FILE}.")
    exit()

# Ekstrak menggunakan logika robust yang sudah ada (Bit 3, Channel Hijau, Blok 3x3)
extracted = extract_lsb(image, WM_SIZE, location=LOCATION)

# Simpan hasil (Biner -> Visual 0/255)
cv2.imwrite(OUTPUT_FILE, (extracted * 255).astype(np.uint8))

print(f"✓ Ekstraksi Selesai!")
print(f"→ Hasil ekstraksi disimpan di: {OUTPUT_FILE}")
