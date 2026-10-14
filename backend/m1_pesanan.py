import os
import time

# ====================================================================
# Model data
# ====================================================================
class Pesanan:
    """Satu baris pesanan dari CSV."""

    def __init__(self, oid, pelanggan, resto, menu, harga,
                 prioritas, t_masuk, t_selesai, status):
        self.oid = oid
        self.pelanggan = pelanggan
        self.resto = resto
        self.menu = menu
        self.harga = harga            # int
        self.prioritas = prioritas    # 1 VIP, 2 PRIORITAS, 3 REGULER
        self.t_masuk = t_masuk        # detik (int)
        self.t_selesai = t_selesai    # detik (int) atau None
        self.status = status          # DONE / CANCEL / ANTRE

    def __repr__(self):
        return "Pesanan(%s, %s, p=%d, %s)" % (
            self.oid, self.pelanggan, self.prioritas, self.status)


# ====================================================================
# Pembaca CSV manual (menangani koma di dalam tanda kutip)
# ====================================================================
def _pecah_baris(baris):
    """Pecah satu baris CSV menjadi larik field. Return (larik, jumlah)."""
    field = [None] * 16
    jumlah = 0
    buf = ""
    dalam_kutip = False
    i = 0
    n = len(baris)
    while i < n:
        c = baris[i]
        if dalam_kutip:
            if c == '"':
                if i + 1 < n and baris[i + 1] == '"':   # "" -> "
                    buf += '"'
                    i += 1
                else:
                    dalam_kutip = False
            else:
                buf += c
        else:
            if c == '"':
                dalam_kutip = True
            elif c == ",":
                field[jumlah] = buf
                jumlah += 1
                buf = ""
            elif c != "\n" and c != "\r":
                buf += c
        i += 1
    field[jumlah] = buf
    jumlah += 1
    return field, jumlah


def _ke_pesanan(f):
    t_selesai = None
    if f[7] != "":
        t_selesai = int(f[7])
    return Pesanan(f[0], f[1], f[2], f[3], int(f[4]),
                   int(f[5]), int(f[6]), t_selesai, f[8])


def baca_csv(path):
    """
    Fungsi tambahan untuk M2: Membaca CSV dan mengembalikan list of Pesanan.
    Sesuai aturan M1: Tidak memakai list.append(), menggunakan alokasi statis.
    """
    # 1. Hitung total baris terlebih dahulu untuk alokasi memori
    total_baris = 0
    with open(path, "r", encoding="utf-8") as fh:
        for _ in fh:
            total_baris += 1

    # 2. Buat larik statis dengan ukuran total_baris
    hasil = [None] * total_baris
    idx = 0

    # 3. Baca ulang dan isi larik
    with open(path, "r", encoding="utf-8") as fh:
        pertama = True
        for baris in fh:
            if pertama:
                pertama = False
                continue
            if baris.strip() == "":
                continue
            f, k = _pecah_baris(baris)
            if k < 9:
                continue
            hasil[idx] = _ke_pesanan(f)
            idx += 1

    # Kembalikan hanya bagian array yang terisi data valid (memotong elemen None sisa)
    return hasil[:idx]


def muat_csv(path, array, linked):
    """
    Baca CSV, isi Array dan LinkList dengan data yang sama
    (urutan sama, lewat append / REGULER supaya O(1) per baris).
    Return jumlah baris yang dimuat.
    """
    jumlah = 0
    with open(path, "r", encoding="utf-8") as fh:
        pertama = True
        for baris in fh:
            if pertama:              # lewati header
                pertama = False
                continue
            if baris.strip() == "":
                continue
            f, k = _pecah_baris(baris)
            if k < 9:
                continue
            p = _ke_pesanan(f)
            array.append(p)
            linked.append(p)
            jumlah += 1
    return jumlah


# ====================================================================
# 1) ARRAY: sepetak memori berukuran tetap, tumbuh 2x saat penuh
# ====================================================================
class Array:
    def __init__(self, kapasitas=4):
        if kapasitas < 1:
            cap = 1
        else:
            cap = kapasitas
        self.data = [None] * cap
        self._kapasitas = cap
        self.n = 0
        self.total_geser = 0     
        self.total_salin = 0     
        self.jumlah_resize = 0

    def __len__(self):
        return self.n

    def kapasitas(self):
        return self._kapasitas

    def _tumbuh(self):
        baru = [None] * (self._kapasitas * 2)
        i = 0
        while i < self.n:
            baru[i] = self.data[i]
            i += 1
        self.total_salin += self.n
        self.jumlah_resize += 1
        self.data = baru
        self._kapasitas = self._kapasitas * 2

    def get(self, i):
        if i < 0 or i >= self.n:
            raise IndexError("indeks %d di luar jangkauan (0..%d)" % (i, self.n - 1))
        return self.data[i]

    def append(self, v):
        if self.n == self._kapasitas:
            self._tumbuh()
        self.data[self.n] = v
        self.n += 1

    def insert(self, i, v):
        if i < 0 or i > self.n:
            raise IndexError("posisi sisip %d di luar jangkauan (0..%d)" % (i, self.n))
        if self.n == self._kapasitas:
            self._tumbuh()
        j = self.n
        while j > i:
            self.data[j] = self.data[j - 1]
            j -= 1
            self.total_geser += 1
        self.data[i] = v
        self.n += 1

    def remove(self, i):
        if i < 0 or i >= self.n:
            raise IndexError("indeks %d di luar jangkauan (0..%d)" % (i, self.n - 1))
        nilai = self.data[i]
        j = i
        while j < self.n - 1:
            self.data[j] = self.data[j + 1]
            j += 1
            self.total_geser += 1
        self.data[self.n - 1] = None
        self.n -= 1
        return nilai

    def isi(self):
        """Tambahan untuk M2: kembalikan list representasi isi saat ini"""
        hasil = [None] * self.n
        i = 0
        while i < self.n:
            hasil[i] = self.data[i]
            i += 1
        return hasil

    def tambah_reguler(self, v):
        self.append(v)
        return self.n - 1

    def tambah_prioritas(self, v):
        pos = self.n // 2
        self.insert(pos, v)
        return pos

    def tambah_vip(self, v):
        self.insert(0, v)
        return 0

    def tambah(self, v):
        if v.prioritas == 1:
            return self.tambah_vip(v)
        if v.prioritas == 2:
            return self.tambah_prioritas(v)
        return self.tambah_reguler(v)

    def hapus(self, i):
        return self.remove(i)

    def stats(self):
        return (
            ("array_len", self.n),
            ("array_capacity", self._kapasitas),
            ("array_total_geser", self.total_geser),
            ("array_total_salin", self.total_salin),
            ("array_resize", self.jumlah_resize),
        )


# ====================================================================
# 2) LINKED LIST: simpul = (nilai, next), simpan head + tail + n
# ====================================================================
class Node:
    def __init__(self, nilai):
        self.nilai = nilai
        self.next = None


class LinkList:
    def __init__(self):
        self.head = None
        self.tail = None
        self.n = 0
        self.total_telusur = 0   

    def __len__(self):
        return self.n

    def _node_ke(self, i):
        cur = self.head
        k = 0
        while k < i:
            cur = cur.next
            k += 1
            self.total_telusur += 1
        return cur

    def get(self, i):
        if i < 0 or i >= self.n:
            raise IndexError("indeks %d di luar jangkauan (0..%d)" % (i, self.n - 1))
        return self._node_ke(i).nilai

    def append(self, v):
        baru = Node(v)
        if self.tail is None:
            self.head = baru
            self.tail = baru
        else:
            self.tail.next = baru
            self.tail = baru
        self.n += 1

    def prepend(self, v):
        baru = Node(v)
        baru.next = self.head
        self.head = baru
        if self.tail is None:
            self.tail = baru
        self.n += 1

    def insert(self, i, v):
        if i < 0 or i > self.n:
            raise IndexError("posisi sisip %d di luar jangkauan (0..%d)" % (i, self.n))
        if i == 0:
            self.prepend(v)
        elif i == self.n:
            self.append(v)
        else:
            sebelum = self._node_ke(i - 1)
            baru = Node(v)
            baru.next = sebelum.next
            sebelum.next = baru
            self.n += 1

    def remove(self, i):
        if i < 0 or i >= self.n:
            raise IndexError("indeks %d di luar jangkauan (0..%d)" % (i, self.n - 1))
        if i == 0:
            target = self.head
            self.head = target.next
            if self.head is None:
                self.tail = None
        else:
            sebelum = self._node_ke(i - 1)
            target = sebelum.next
            sebelum.next = target.next
            if target is self.tail:          
                self.tail = sebelum
        self.n -= 1
        return target.nilai

    def isi(self):
        """Tambahan opsional untuk mengintip isi linked list"""
        out = [None] * self.n
        cur = self.head
        i = 0
        while cur is not None:
            out[i] = cur.nilai
            cur = cur.next
            i += 1
        return out

    def tambah_reguler(self, v):
        self.append(v)
        return self.n - 1

    def tambah_prioritas(self, v):
        pos = self.n // 2
        self.insert(pos, v)
        return pos

    def tambah_vip(self, v):
        self.prepend(v)
        return 0

    def tambah(self, v):
        if v.prioritas == 1:
            return self.tambah_vip(v)
        if v.prioritas == 2:
            return self.tambah_prioritas(v)
        return self.tambah_reguler(v)

    def hapus(self, i):
        return self.remove(i)

    def stats(self):
        return (
            ("linked_len", self.n),
            ("linked_total_telusur", self.total_telusur),
        )


# ====================================================================
# Pengujian dan Integrasi
# ====================================================================
def _buat(oid, prio):
    return Pesanan(oid, "tes", "resto", "menu", 10000, prio, 0, None, "ANTRE")

def _isi_array(a):
    out = [None] * a.n
    i = 0
    while i < a.n:
        out[i] = a.data[i].oid
        i += 1
    return out

def _isi_linked(l):
    out = [None] * l.n
    cur = l.head
    i = 0
    while cur is not None:
        out[i] = cur.nilai.oid
        cur = cur.next
        i += 1
    return out

def _uji_kecil():
    a, l = Array(4), LinkList()
    for k in range(1, 6):
        p = _buat("R%d" % k, 3)
        a.tambah(p)
        l.tambah(p)
    assert a.kapasitas() == 8 and a.jumlah_resize == 1
    p = _buat("P1", 2); a.tambah(p); l.tambah(p)
    p = _buat("V1", 1); a.tambah(p); l.tambah(p)
    harapan = ["V1", "R1", "R2", "P1", "R3", "R4", "R5"]
    assert _isi_array(a) == harapan, _isi_array(a)
    assert _isi_linked(l) == harapan, _isi_linked(l)
    assert a.get(3).oid == "P1" and l.get(3).oid == "P1"
    assert a.hapus(0).oid == l.hapus(0).oid
    assert a.hapus(2).oid == l.hapus(2).oid
    assert a.hapus(a.n - 1).oid == l.hapus(l.n - 1).oid
    assert _isi_array(a) == _isi_linked(l)
    assert l.tail.nilai.oid == _isi_linked(l)[-1]
    while a.n > 0:
        a.hapus(0); l.hapus(0)
    assert l.head is None and l.tail is None
    p = _buat("Z", 3); a.tambah(p); l.tambah(p)
    assert _isi_array(a) == ["Z"] == _isi_linked(l)
    for fn in (lambda: a.get(5), lambda: l.get(5),
               lambda: a.hapus(-1), lambda: l.hapus(9)):
        try:
            fn()
            assert False
        except IndexError:
            pass
    print("[v] Uji kecil: LULUS")


def _bandingkan(path):
    a, l = Array(), LinkList()
    t0 = time.perf_counter()
    n = muat_csv(path, a, l)
    
    print("\n" + "="*50)
    print(" HASIL INTEGRASI DATA (M1)")
    print("="*50)
    print("Status Muat : Berhasil")
    print("Total Baris : %d baris" % n)
    print("Waktu Muat  : %.2f detik" % (time.perf_counter() - t0))
    print("Info Array  : kapasitas=%d, resize=%dx, salin=%d elemen" 
          % (a.kapasitas(), a.jumlah_resize, a.total_salin))
    
    print("-" * 50)
    print(" BENCHMARK INSERT (Array vs Linked List)")
    print("-" * 50)
    
    for nama, fn_a, fn_l in (
        ("REGULER   (Akhir) ", a.tambah_reguler, l.tambah_reguler),
        ("PRIORITAS (Tengah)", a.tambah_prioritas, l.tambah_prioritas),
        ("VIP       (Depan) ", a.tambah_vip, l.tambah_vip),
    ):
        p = _buat("X-TES", 3)
        t = time.perf_counter(); fn_a(p); ta = (time.perf_counter() - t) * 1000
        t = time.perf_counter(); fn_l(p); tl = (time.perf_counter() - t) * 1000
        print("%s => Array: %8.3f ms | Linked List: %8.3f ms" % (nama, ta, tl))
    print("="*50 + "\n")


if __name__ == "__main__":
    import sys
    
    print("=== Menjalankan Uji Kecil ===")
    _uji_kecil()

    nama_file = "pesanan.csv"
    base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    path_data = os.path.join(base_dir, 'data', nama_file)

    if os.path.exists(path_data):
        target_path = path_data
    elif os.path.exists(nama_file):
        target_path = nama_file
    elif len(sys.argv) > 1 and os.path.exists(sys.argv[1]):
        target_path = sys.argv[1]
    else:
        target_path = None

    if target_path:
        print(f"\nMembaca file dari: {target_path}")
        _bandingkan(target_path)
    else:
        print(f"\n[!] Peringatan: File '{nama_file}' tidak ditemukan di lokasi manapun.")
        print(f"Path yang dicari: {path_data}")