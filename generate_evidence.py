import cv2
import numpy as np
import os

EVIDENCE_DIR = 'experiment_evidence'
os.makedirs(EVIDENCE_DIR, exist_ok=True)

IMAGE_PATH = 'data/foto_wajah.jpg'
WATERMARK_PATH = 'data/input.png'
WM_SIZE = (64, 64)

# ==========================================
# EKSPERIMEN 1: Full Color LSB (Gagal Total di JPEG)
# ==========================================
def run_exp1_full_color():
    print("Menjalankan Eksperimen 1: Full Color LSB (Bit-0)")
    
    # Load host warna & watermark warna
    img = cv2.imread(IMAGE_PATH, cv2.IMREAD_COLOR)
    wm = cv2.imread(WATERMARK_PATH, cv2.IMREAD_COLOR)
    wm = cv2.resize(wm, WM_SIZE)
    
    # Binarize warna watermark hanya untuk penyisipan (0 atau 1)
    wm_bits = (wm > 127).astype(np.uint8)
    
    # Embed di Bit-0 semua channel
    marked = img.copy()
    h, w = WM_SIZE
    marked[0:h, 0:w] = (marked[0:h, 0:w] & 0xFE) | wm_bits
    
    # Simpan hasil embed (sebelum JPEG)
    cv2.imwrite(f"{EVIDENCE_DIR}/exp1_embedded_color.png", marked)
    
    # Kompresi JPEG (Quality menengah)
    encode_param = [int(cv2.IMWRITE_JPEG_QUALITY), 50]
    _, enc = cv2.imencode('.jpg', marked, encode_param)
    compressed = cv2.imdecode(enc, cv2.IMREAD_COLOR)
    cv2.imwrite(f"{EVIDENCE_DIR}/exp1_compressed_qf50.jpg", compressed)
    
    # Ekstrak dari Bit-0 (Akan hancur)
    extracted = (compressed[0:h, 0:w] & 1) * 255
    cv2.imwrite(f"{EVIDENCE_DIR}/exp1_extracted_failed.png", extracted.astype(np.uint8))
    print("-> Selesai! Cek exp1_extracted_failed.png (Pasti hancur)")

# ==========================================
# EKSPERIMEN 2: Full Grayscale LSB (Berhasil, tapi jelek)
# ==========================================
def run_exp2_full_grayscale():
    print("\nMenjalankan Eksperimen 2: Full Grayscale LSB")
    
    # Load host grayscale
    img_gray = cv2.imread(IMAGE_PATH, cv2.IMREAD_GRAYSCALE)
    wm_gray = cv2.imread(WATERMARK_PATH, cv2.IMREAD_GRAYSCALE)
    wm_gray = cv2.resize(wm_gray, WM_SIZE)
    
    # Binarize
    wm_bits = (wm_gray > 127).astype(np.uint8)
    
    # Embed di Bit-3 (Robust) tapi host-nya abu-abu
    marked_gray = img_gray.copy()
    h, w = WM_SIZE
    # Mask untuk clear bit 3: ~(1<<3) = 247
    marked_gray[0:h, 0:w] = (marked_gray[0:h, 0:w] & 247) | (wm_bits << 3)
    
    # Simpan hasil embed (Gambar jadi abu-abu)
    cv2.imwrite(f"{EVIDENCE_DIR}/exp2_embedded_grayscale.png", marked_gray)
    print("-> Selesai! Cek exp2_embedded_grayscale.png (Warna hilang)")

if __name__ == '__main__':
    run_exp1_full_color()
    run_exp2_full_grayscale()
