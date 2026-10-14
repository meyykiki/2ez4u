import os
import sys
import time

sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), ".."))
from backend.m1_pesanan import Array, Pesanan, baca_csv


# ======================= STACK =======================
class Stack:
    """Tumpukan (LIFO) di atas Array M1. push/pop/peek semuanya O(1)."""

    def __init__(self):
        self._a = Array()

    def __len__(self):
        return len(self._a)

    def kosong(self):
        return len(self._a) == 0

    def push(self, x):
        self._a.append(x)

    def pop(self):
        if len(self._a) == 0:
            raise IndexError("stack kosong")
        return self._a.remove(len(self._a) - 1)

    def peek(self):
        if len(self._a) == 0:
            raise IndexError("stack kosong")
        return self._a.get(len(self._a) - 1)

    def kosongkan(self):
        self._a = Array()

    def isi(self):
        """Dari dasar ke puncak."""
        return self._a.isi()


# ======================= BAGIAN A (1): KASIR =======================
def tokenisasi(ekspresi):
    """'( 3 * 12000 )' -> ['(', '3', '*', '12000', ')'].
    Angka berdigit banyak harus jadi SATU token."""
    hasil = []
    angka = ""
    for c in ekspresi:
        if ("0" <= c <= "9") or c == ".":
            angka += c
            continue
        if angka != "":
            hasil.append(angka)
            angka = ""
        if c == " " or c == "\t":
            continue
        if c in ("+", "-", "*", "/", "(", ")"):
            hasil.append(c)
        else:
            raise ValueError("karakter tidak dikenal: " + c)
    if angka != "":
        hasil.append(angka)
    return hasil


def _prioritas(op):
    if op == "*" or op == "/":
        return 2
    return 1


def _adalah_operator(t):
    return t in ("+", "-", "*", "/")


def _gabung(daftar):
    if len(daftar) == 0:
        return "kosong"
    s = ""
    for i in range(len(daftar)):
        if i > 0:
            s += " "
        s += str(daftar[i])
    return s


def ke_postfix(ekspresi):
    """Infix -> postfix (stack operator)."""
    token = tokenisasi(ekspresi)
    st = Stack()
    keluar = []
    langkah = []
    no = 0

    for t in token:
        no += 1
        if _adalah_operator(t):
            tindakan = ""
            while (not st.kosong()) and st.peek() != "(" \
                    and _prioritas(st.peek()) >= _prioritas(t):
                atas = st.pop()
                keluar.append(atas)
                if _prioritas(atas) == _prioritas(t):
                    tindakan += "pop %s (sama kuat), " % atas
                else:
                    tindakan += "pop %s (lebih kuat), " % atas
            st.push(t)
            tindakan += "push %s" % t
        elif t == "(":
            st.push(t)
            tindakan = "push ( ke stack"
        elif t == ")":
            ketemu = False
            while not st.kosong():
                atas = st.pop()
                if atas == "(":
                    ketemu = True
                    break
                keluar.append(atas)
            if not ketemu:
                raise ValueError("kurung tutup tanpa pasangan")
            tindakan = "pop sampai (, lalu buang ("
        else:
            keluar.append(t)
            tindakan = "operand, langsung ke output"
        langkah.append(("1.%d" % no, t, tindakan, _gabung(st.isi()), _gabung(keluar)))

    while not st.kosong():
        atas = st.pop()
        if atas == "(":
            raise ValueError("kurung buka tanpa pasangan")
        keluar.append(atas)
    langkah.append(("1.akhir", "-", "pop sisa stack", "kosong", _gabung(keluar)))
    return keluar, langkah


def _ke_angka(s):
    if "." in s:
        return float(s)
    return int(s)


def hitung(postfix):
    """Evaluasi postfix (stack angka)."""
    if isinstance(postfix, str):
        token = postfix.split()
    else:
        token = postfix
    st = Stack()
    langkah = []
    no = 0
    for t in token:
        no += 1
        if _adalah_operator(t):
            if len(st) < 2:
                raise ValueError("ekspresi tidak valid (operand kurang)")
            b = st.pop()          # operand KANAN keluar duluan
            a = st.pop()
            if t == "+":
                r = a + b
            elif t == "-":
                r = a - b
            elif t == "*":
                r = a * b
            else:
                if b == 0:
                    raise ValueError("pembagian dengan nol")
                if isinstance(a, int) and isinstance(b, int) and a % b == 0:
                    r = a // b
                else:
                    r = a / b
            st.push(r)
            tindakan = "pop %s dan %s -> %s%s%s = %s" % (b, a, a, t, b, r)
        else:
            st.push(_ke_angka(t))
            tindakan = "operand, push %s" % t
        langkah.append(("2.%d" % no, t, tindakan, _gabung(st.isi())))
    if len(st) != 1:
        raise ValueError("ekspresi tidak valid")
    return st.pop(), langkah


def hitung_struk(ekspresi):
    pf, l1 = ke_postfix(ekspresi)
    total, l2 = hitung(pf)
    return _gabung(pf), total, l1 + l2


def format_rupiah(n):
    s = str(int(n))
    hasil = ""
    hitung_digit = 0
    for i in range(len(s) - 1, -1, -1):
        if hitung_digit == 3:
            hasil = "." + hasil
            hitung_digit = 0
        hasil = s[i] + hasil
        hitung_digit += 1
    return "Rp " + hasil


# ======================= BAGIAN B: ANTREAN =======================
class AntreanNaif:
    """Antrean di atas Array biasa."""

    def __init__(self):
        self._a = Array()
        self.total_geseran = 0

    def __len__(self):
        return len(self._a)

    def kosong(self):
        return len(self._a) == 0

    def kapasitas(self):
        if hasattr(self._a, "kapasitas"):
            return self._a.kapasitas()
        return len(self._a)

    def enqueue(self, x):
        self._a.append(x)

    def dequeue(self):
        if len(self._a) == 0:
            return None
        x = self._a.remove(0)
        # Menghitung elemen yang digeser: setiap elemen setelah 0 bergeser 1 ke kiri.
        self.total_geseran += len(self._a) 
        return x

    def pop_belakang(self):
        if len(self._a) == 0:
            return None
        x = self._a.remove(len(self._a) - 1)
        # Menghapus dari belakang tidak menggeser sisa elemen
        return x

    def sisip_depan(self, daftar):
        k = len(daftar) - 1
        while k >= 0:
            self._a.insert(0, daftar[k])
            # Menyisipkan di indeks 0 menggeser seluruh elemen lama ke kanan
            self.total_geseran += len(self._a) - 1 
            k -= 1

    def isi(self):
        return self._a.isi() if hasattr(self._a, "isi") else list(self._a)


class AntreanMelingkar:
    """Circular buffer."""

    def __init__(self, kapasitas=8):
        self._k = kapasitas
        self._data = [None] * kapasitas
        self.front = 0
        self.rear = 0
        self.count = 0
        self.total_geseran = 0

    def __len__(self):
        return self.count

    def kosong(self):
        return self.count == 0

    def kapasitas(self):
        return self._k

    def _tumbuh(self):
        baru = [None] * (self._k * 2)
        for i in range(self.count):
            baru[i] = self._data[(self.front + i) % self._k]
        self._data = baru
        self._k *= 2
        self.front = 0
        self.rear = self.count

    def enqueue(self, x):
        if self.count == self._k:
            self._tumbuh()
        self._data[self.rear] = x
        self.rear = (self.rear + 1) % self._k
        self.count += 1

    def dequeue(self):
        if self.count == 0:
            return None
        x = self._data[self.front]
        self._data[self.front] = None
        self.front = (self.front + 1) % self._k
        self.count -= 1
        return x

    def pop_belakang(self):
        if self.count == 0:
            return None
        self.rear = (self.rear - 1) % self._k
        x = self._data[self.rear]
        self._data[self.rear] = None
        self.count -= 1
        return x

    def sisip_depan(self, daftar):
        k = len(daftar) - 1
        while k >= 0:
            if self.count == self._k:
                self._tumbuh()
            self.front = (self.front - 1) % self._k
            self._data[self.front] = daftar[k]
            self.count += 1
            k -= 1

    def isi(self):
        hasil = []
        for i in range(self.count):
            hasil.append(self._data[(self.front + i) % self._k])
        return hasil


# ======================= SISTEM: ANTREAN + UNDO/REDO =======================
class SistemAntrean:
    def __init__(self):
        self.naif = AntreanNaif()
        self.circ = AntreanMelingkar()
        self.undo = Stack()
        self.redo = Stack()
        self.next_id = 1

    def isi_dari(self, data):
        n = 0
        for p in data:
            if p.status == "ANTRE":
                self.naif.enqueue(p)
                self.circ.enqueue(p)
                n += 1
        self.next_id = len(data) + 1
        return n

    def pesanan_baru(self, nama):
        p = Pesanan("O-%06d" % self.next_id, nama, "kafe-teknik",
                    "roti-bakar", 12000, 3, 0, None, "ANTRE")
        self.next_id += 1
        return p

    def _antrean(self, jenis):
        if jenis == "naif":
            return self.naif
        if jenis == "circular":
            return self.circ
        raise ValueError("jenis harus 'naif' atau 'circular'")

    def enqueue(self, pesanan):
        self.naif.enqueue(pesanan)
        self.circ.enqueue(pesanan)
        self.undo.push(("ENQUEUE", pesanan))
        self.redo.kosongkan()

    def dequeue(self, jenis, n=1):
        q = self._antrean(jenis)
        g0 = q.total_geseran
        keluar = []
        for _ in range(n):
            x = q.dequeue()
            if x is None:
                break
            keluar.append(x)
        if len(keluar) > 0:
            self.undo.push(("DEQUEUE", jenis, keluar))
            self.redo.kosongkan()
        return keluar, q.total_geseran - g0

    def undo_last(self):
        if self.undo.kosong():
            return "tumpukan undo kosong, tidak ada yang dibatalkan"
        rec = self.undo.pop()
        if rec[0] == "ENQUEUE":
            self.naif.pop_belakang()
            self.circ.pop_belakang()
            pesan = ("Pembatalan enqueue: %s dikeluarkan lagi dari belakang."
                     % rec[1].oid)
        else:
            self._antrean(rec[1]).sisip_depan(rec[2])
            pesan = ("%d pesanan dikembalikan ke DEPAN antrean %s"
                     % (len(rec[2]), rec[1]))
        self.redo.push(rec)
        return pesan

    def redo_last(self):
        if self.redo.kosong():
            return "tumpukan redo kosong, tidak ada yang diulang"
        rec = self.redo.pop()
        if rec[0] == "ENQUEUE":
            self.naif.enqueue(rec[1])
            self.circ.enqueue(rec[1])
            pesan = "Enqueue dikerjakan lagi: %s masuk kembali ke belakang." \
                    % rec[1].oid
        else:
            q = self._antrean(rec[1])
            ulang = []
            for _ in range(len(rec[2])):
                ulang.append(q.dequeue())
            rec = ("DEQUEUE", rec[1], ulang)
            pesan = "%d pesanan keluar lagi dari antrean %s" \
                    % (len(ulang), rec[1])
        self.undo.push(rec)
        return pesan

    def history(self):
        isi = self.undo.isi()
        hasil = []
        i = len(isi) - 1
        while i >= 0:
            rec = isi[i]
            if rec[0] == "ENQUEUE":
                hasil.append("ENQUEUE %s" % rec[1].oid)
            else:
                hasil.append("DEQUEUE %s x%d" % (rec[1], len(rec[2])))
            i -= 1
        return hasil

    def stats(self):
        return [("queue_len_naif", len(self.naif)),
                ("queue_len_circular", len(self.circ)),
                ("queue_capacity_naif", self.naif.kapasitas()),
                ("queue_capacity_circular", self.circ.kapasitas()),
                ("total_geseran_naif", self.naif.total_geseran),
                ("total_geseran_circular", self.circ.total_geseran),
                ("undo_depth", len(self.undo)),
                ("redo_depth", len(self.redo))]


# ======================= DEMO =======================
def _ukur(f):
    t = time.perf_counter()
    h = f()
    return h, (time.perf_counter() - t) * 1000

def demo():
    print("> stack_postfix ( 3 * 12000 ) + ( 2 * 8500 ) - 5000")
    (pf, total, langkah), ms = _ukur(
        lambda: hitung_struk("( 3 * 12000 ) + ( 2 * 8500 ) - 5000"))
    print("  postfix:", pf)
    print("  TOTAL  :", format_rupiah(total), "  [M2 - stack] %.2f ms" % ms)
    for l in langkah:
        print("   %-7s %-6s %-40s %s" % (l[0], l[1], l[2], l[3]))

    path = os.path.join(os.path.dirname(os.path.abspath(__file__)),
                        "..", "data", "pesanan.csv")
    sis = SistemAntrean()
    n = sis.isi_dari(baca_csv(path))
    print("\n%d pesanan ANTRE dimuat ke KEDUA antrean" % n)

    p = sis.pesanan_baru("Pelanggan Baru")
    _, ms = _ukur(lambda: sis.enqueue(p))
    print("> queue_enqueue Pelanggan Baru\n  %s masuk paling belakang"
          "  [%.3f ms]" % (p.oid, ms))

    for jumlah in (1, 100):
        for jenis in ("naif", "circular"):
            (kel, g), ms = _ukur(lambda: sis.dequeue(jenis, jumlah))
            print("> queue_dequeue_%s %d\n  %d pesanan keluar | %d elemen "
                  "digeser  [%.3f ms]" % (jenis, jumlah, len(kel), g, ms))

    print("> stack_undo\n  ", sis.undo_last())
    print("> stack_redo\n  ", sis.redo_last())
    print("> queue_enqueue Pencabang (aksi BARU sesudah undo)")
    sis.enqueue(sis.pesanan_baru("Pencabang"))
    print("> stack_redo\n  ", sis.redo_last())
    print("\nhistory:", sis.history())
    print("stats  :", sis.stats())


if __name__ == "__main__":
    demo()