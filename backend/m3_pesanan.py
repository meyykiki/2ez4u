import time

# ==========================================
# 1. ALGORITMA SORT & SEARCH (INTI M3)
# ==========================================

def insertion_sort(larik, indeks_kunci):
    """
    O(n^2), In-place, Stabil.
    Menolak memproses jika jumlah data > 20.000 baris.
    """
    n = len(larik)
    
    # Syarat M3: Tolak data terlalu besar agar program tidak freeze
    if n > 20000:
        raise ValueError("DITOLAK: batasnya 20.000 baris, pakai merge sort untuk data penuh")
    
    perbandingan = 0
    pemindahan = 0
    
    for i in range(1, n):
        kunci_item = larik[i]
        j = i - 1
        
        # Menggunakan '>' memastikan algoritma stabil (stable)
        while j >= 0:
            perbandingan += 1
            val_j = larik[j][indeks_kunci]
            val_kunci = kunci_item[indeks_kunci]
            
            # Penanganan aman jika terjadi ketidakcocokan tipe data (int vs str)
            if type(val_j) != type(val_kunci):
                val_j = str(val_j)
                val_kunci = str(val_kunci)
                
            if val_j > val_kunci:
                larik[j + 1] = larik[j]
                pemindahan += 1
                j -= 1
            else:
                break
                
        larik[j + 1] = kunci_item
        pemindahan += 1
        
    return larik, perbandingan, pemindahan


def merge_sort(larik, indeks_kunci):
    """
    O(n log n), Stabil.
    Mampu memproses data skala besar (200.000+ baris).
    """
    if len(larik) <= 1:
        return larik, 0, 0
    
    mid = len(larik) // 2
    
    kiri, banding_kiri, pindah_kiri = merge_sort(larik[:mid], indeks_kunci)
    kanan, banding_kanan, pindah_kanan = merge_sort(larik[mid:], indeks_kunci)
    
    hasil, banding_merge, pindah_merge = merge(kiri, kanan, indeks_kunci)
    
    total_banding = banding_kiri + banding_kanan + banding_merge
    total_pindah = pindah_kiri + pindah_kanan + pindah_merge
    
    return hasil, total_banding, total_pindah


def merge(kiri, kanan, indeks_kunci):
    hasil = []
    i = 0
    j = 0
    perbandingan = 0
    pemindahan = 0
    
    while i < len(kiri) and j < len(kanan):
        perbandingan += 1
        val_kiri = kiri[i][indeks_kunci]
        val_kanan = kanan[j][indeks_kunci]
        
        # Penanganan aman tipe data
        if type(val_kiri) != type(val_kanan):
            val_kiri = str(val_kiri)
            val_kanan = str(val_kanan)
            
        # Menggunakan '<=' memastikan stabil (kiri didahulukan jika nilai sama)
        if val_kiri <= val_kanan:
            hasil.append(kiri[i])
            pemindahan += 1
            i += 1
        else:
            hasil.append(kanan[j])
            pemindahan += 1
            j += 1
            
    while i < len(kiri):
        hasil.append(kiri[i])
        pemindahan += 1
        i += 1
        
    while j < len(kanan):
        hasil.append(kanan[j])
        pemindahan += 1
        j += 1
        
    return hasil, perbandingan, pemindahan


def linear_search(larik, target, indeks_kunci):
    """
    O(n), mencari satu per satu dari awal.
    Tidak mensyaratkan data terurut.
    """
    perbandingan = 0
    for i in range(len(larik)):
        perbandingan += 1
        val = larik[i][indeks_kunci]
        if str(val) == str(target):
            return i, perbandingan
            
    return -1, perbandingan


def binary_search(larik, target, indeks_kunci):
    """
    O(log n), membuang separuh kemungkinan tiap iterasi.
    Mensyaratkan data dalam 'larik' SUDAH TERURUT.
    """
    lo = 0
    hi = len(larik) - 1
    perbandingan = 0
    
    while lo <= hi:
        perbandingan += 1
        mid = (lo + hi) // 2
        val_mid = larik[mid][indeks_kunci]
        
        target_cmp = target
        if type(val_mid) != type(target_cmp):
            val_mid = str(val_mid)
            target_cmp = str(target_cmp)
            
        if val_mid == target_cmp:
            return mid, perbandingan
        elif val_mid < target_cmp:
            lo = mid + 1
        else:
            hi = mid - 1
            
    return -1, perbandingan


# ==========================================
# 2. SIMULASI TERMINAL COMMAND & BACA DATA
# ==========================================

def format_ribuan(angka):
    return f"{angka:,}".replace(',', '.')

def format_waktu(ms):
    return f"{ms:.2f}".replace('.', ',')

def baca_data_csv(nama_file):
    data_pesanan = []
    try:
        with open(nama_file, 'r', encoding='utf-8') as f:
            header = f.readline()  # Lewati baris header
            for baris in f:
                baris = baris.strip()
                if not baris:
                    continue
                kolom = baris.split(',')
                if len(kolom) >= 5:
                    # Konversi harga (indeks 4) ke integer secara aman
                    try:
                        kolom[4] = int(kolom[4].strip())
                    except ValueError:
                        kolom[4] = 0
                        
                    # Konversi prioritas (indeks 5) ke integer jika ada
                    if len(kolom) > 5:
                        try:
                            kolom[5] = int(kolom[5].strip())
                        except ValueError:
                            kolom[5] = 3
                            
                    data_pesanan.append(kolom)
    except FileNotFoundError:
        print(f"File {nama_file} tidak ditemukan!")
    return data_pesanan


if __name__ == "__main__":
    # Path file disesuaikan dengan struktur folder proyek (data/pesanan.csv)
    NAMA_FILE = 'data/pesanan.csv'
    
    print("Membaca data dari", NAMA_FILE, "...")
    data_asli = baca_data_csv(NAMA_FILE)
    
    if not data_asli:
        print("Data kosong atau gagal dibaca. Program berhenti.")
        exit()
        
    print(f"Data berhasil dimuat: {format_ribuan(len(data_asli))} baris.\n")
    print("=" * 60)
    print(" SIMULASI COMMAND PANEL M3 (SORT & SEARCH)".center(60))
    print("=" * 60 + "\n")

    # --- SIMULASI 1: INSERTION SORT (2.000 data) ---
    jumlah_uji = 2000
    if len(data_asli) >= jumlah_uji:
        print(f"> insertion_sort jumlah={jumlah_uji} kunci=harga")
        data_uji_1 = [row.copy() for row in data_asli[:jumlah_uji]]
        
        start = time.perf_counter()
        _, banding_ins, _ = insertion_sort(data_uji_1, 4) # indeks 4 = harga
        end = time.perf_counter()
        waktu_ms = (end - start) * 1000
        
        print(f"{format_ribuan(jumlah_uji)} pesanan terurut | {format_ribuan(banding_ins)} perbandingan [M3 - insertion sort] {format_waktu(waktu_ms)} ms\n")

    # --- SIMULASI 2: MERGE SORT (2.000 data) ---
    if len(data_asli) >= jumlah_uji:
        print(f"> merge_sort jumlah={jumlah_uji} kunci=harga")
        data_uji_2 = [row.copy() for row in data_asli[:jumlah_uji]]
        
        start = time.perf_counter()
        _, banding_mrg, _ = merge_sort(data_uji_2, 4)
        end = time.perf_counter()
        waktu_ms = (end - start) * 1000
        
        print(f"{format_ribuan(jumlah_uji)} pesanan terurut | {format_ribuan(banding_mrg)} perbandingan [M3 - merge sort] {format_waktu(waktu_ms)} ms\n")

    # --- SIMULASI 3: PENOLAKAN INSERTION SORT (> 20.000 data) ---
    print("> insertion_sort jumlah=200000")
    try:
        # Jika data kurang dari 20.000, buat data dummy berukuran 20.001
        if len(data_asli) > 20000:
            data_uji_3 = [row.copy() for row in data_asli]
        else:
            data_uji_3 = [['O-000000', 'Dummy', 'Resto', 'Menu', 10000]] * 20001
            
        insertion_sort(data_uji_3, 4)
    except ValueError as e:
        print(f"{e}\n")

    # --- SIMULASI 4: LINEAR SEARCH ---
    target_oid = "O-000010" if len(data_asli) < 100 else data_asli[min(137441, len(data_asli)-1)][0]
    print(f"> linear_search {target_oid}")
    
    start = time.perf_counter()
    idx_lin, banding_lin = linear_search(data_asli, target_oid, 0) # Indeks 0 = oid
    end = time.perf_counter()
    waktu_ms = (end - start) * 1000
    
    if idx_lin != -1:
        print(f"ditemukan di indeks {format_ribuan(idx_lin)} | {format_ribuan(banding_lin)} perbandingan [M3 - linear] {format_waktu(waktu_ms)} ms\n")
    else:
        print(f"tidak ditemukan | {format_ribuan(banding_lin)} perbandingan [M3 - linear] {format_waktu(waktu_ms)} ms\n")

    # --- SIMULASI 5: BINARY SEARCH ---
    print(f"> binary_search {target_oid}")
    print("daftar terurut oid dibangun sekali (merge sort)...")
    
    start_sort = time.perf_counter()
    data_terurut_oid, _, _ = merge_sort(data_asli, 0) # Indeks 0 = oid
    end_sort = time.perf_counter()
    waktu_sort_ms = (end_sort - start_sort) * 1000
    
    start_search = time.perf_counter()
    idx_bin, banding_bin = binary_search(data_terurut_oid, target_oid, 0)
    end_search = time.perf_counter()
    waktu_ms = (end_search - start_search) * 1000
    
    if idx_bin != -1:
        print(f"ditemukan di baris {format_ribuan(idx_bin)} | {format_ribuan(banding_bin)} perbandingan [M3 - binary] {format_waktu(waktu_ms)} ms\n")
    else:
        print(f"tidak ditemukan | {format_ribuan(banding_bin)} perbandingan [M3 - binary] {format_waktu(waktu_ms)} ms\n")