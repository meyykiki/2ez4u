
# 2EZ4U Food Delivery - Backend Engine & UI System 

Dokumentasi resmi proyek akhir mata kuliah **Struktur Data dan Analisis Algoritma **. Proyek ini mengembangkan *engine backend* layanan pesan-antar makanan/barang versi mini (*GoFood/GrabFood/ShopeeFood*) secara mandiri menggunakan Python  serta antarmuka grafis (*GUI*) berbasis Tkinter.



---
##  Kontributor / Kolaborator

* **Nama**: MELLY KIKI AGUSTINA
* **NRP**: 5024251008
* **Mata Kuliah**: Struktur Data dan Analisis Algoritma
---

##  Deskripsi Proyek
**2EZ4U** dirancang untuk menangani trafik sistem pemesanan berskala besar dengan simulasi basis data mencapai **200.000 baris data CSV**. Titik berat penilaian bukan pada estetika tampilan *frontend*, melainkan pada **implementasi murni struktur data dan algoritma** untuk menguji performa, efisiensi memori, serta kompleksitas waktu eksekusi (*Time Complexity*).

---

##  Batasan Teknis
Sesuai dengan spesifikasi proyek, pengembangan backend mematuhi aturan ketat berikut:
* **Proyek Individu**: Dikembangkan secara mandiri.
* **Larangan Penggunaan Fungsi Instan**: Dilarang keras menggunakan fungsi bawaan Python seperti `dict`, `set`, `sorted()`, `.sort()`, `heapq`, `bisect`, modul `collections`, literatur kurung kurawal `{}` untuk kamus, serta *dictionary/set comprehension*.
* **Pengecualian yang Diizinkan**: Penggunaan struktur data `list` bawaan dibatasi hanya sebagai array primitif, serta diperbolehkan menggunakan `tuple`, operasi aritmetika dasar, dan fungsi *I/O* standar.

---

##  Alat & Teknologi yang Digunakan
* **Bahasa Pemrograman**: Python versi 3.11+
* **Antarmuka (GUI)**: Pustaka standar Python Tkinter
* **Manajemen Data**: Berkas CSV mentah (*Comma Separated Values*)
* **IDE**: Visual Studio Code

---
## Cara Menjalankan & Menggunakan Aplikasi

### 1. Menjalankan Program di Komputer Lokal

Pastikan Anda sudah menginstal Python (versi 3.11 atau terbaru) di perangkat Anda. Buka terminal di direktori utama proyek, lalu jalankan perintah berikut:

```bash
python frontend/ui.py

```

### 2. Panduan Penggunaan Menu di Antarmuka (GUI)

* **Memuat Data (*Load Data CSV*)**:
1. Klik tombol **Load Data CSV** di panel menu sebelah kiri.
2. Pilih file `pesanan.csv` di dalam folder `data/`.
3. Sistem akan memuat ribuan data pesanan, menampilkannya ke tabel utama, dan mencatat waktu eksekusi (*milidetik*) di panel bawah (**COMMAND**).


* **Navigasi Milestone (M1 - M3)**:
* Pilih fitur yang ingin diuji melalui tombol-tombol pada *sidebar* sebelah kiri (seperti melihat struktur Array/Linked List, menjalankan mesin kasir *Postfix*, *Enqueue/Dequeue* antrean, hingga pengujian *Insertion/Merge Sort* serta *Linear/Binary Search*).
* Masukkan parameter yang diminta pada form bagian atas, lalu klik tombol aksi (misal: **TAMBAH**, **HITUNG**, **URUTKAN**, atau **CARI**).
* Hasil eksekusi, waktu proses, serta statistik perbandingan akan langsung ditampilkan secara *real-time* pada tabel dan panel log.



---
##  Penjelasan Detail Milestone & Fitur (M1 - M3)

### M1: Data Pesanan (Array vs Linked List)

Modul `m1_pesanan.py` mengelola data pesanan ke dalam dua struktur data berbeda secara bersamaan untuk menguji performa:

* **Array Dinamis**: Menggunakan blok memori kontigu. Ketika penuh, array melakukan *resize* dengan mengalokasikan petak baru berukuran 2 kali lipat lalu menyalin seluruh data lama ($O(n)$ pada saat *resize*, namun berbiaya *amortized* $O(1)$ untuk penambahan biasa).
* **Linked List**: Menggunakan simpul berantai yang dihubungkan melalui *pointer* `next` dengan menyimpan referensi `head` dan `tail`.
* **Aturan Tiga Jenis Pesanan**:
* **REGULER (Prioritas 3)**: Masuk ke antrean paling belakang ($O(1)$ pada Array dan Linked List).
* **PRIORITAS (Prioritas 2)**: Menyerobot masuk ke bagian tengah antrean ($O(n)$ karena butuh pergeseran array atau penelusuran simpul).
* **VIP (Prioritas 1)**: Langsung menempati urutan paling depan. Array memerlukan waktu $O(n)$ untuk menggeser seluruh elemen, sedangkan Linked List sangat efisien $O(1)$ karena hanya memindahkan penunjuk `head`.



### M2: Stack & Queue + Undo/Redo

Modul `m2_antrean.py` menyelesaikan dua masalah operasional utama di restoran:

1. **Mesin Kasir (Infix ke Postfix)**: Menggunakan struktur **Stack** untuk mengubah ekspresi matematika kasir (misal: `(3 * 12000) + (2 * 8500) - 5000`) menjadi bentuk *postfix*, lalu mengevaluasi total harganya secara bertahap tanpa melanggar prioritas operator.
2. **Sistem Undo & Redo**: Memanfaatkan dua buah tumpukan (*Stack*) untuk mencatat riwayat aksi. Tombol *Undo* membatalkan aksi terakhir dengan menjalankan operasi kebalikannya, sedangkan *Redo* mengembalikan aksi yang sempat dibatalkan.
3. **Antrean Dapur (Naif vs Circular Queue)**:
* **Queue Naif**: Menggunakan larik biasa di mana operasi *dequeue* mengambil elemen indeks ke-0 dan **menggeser seluruh sisa elemen ke kiri**. Berbiaya mahal $O(n)$.
* **Queue Circular (Melingkar)**: Menggunakan *buffer* melingkar dengan penunjuk `front`, `rear`, dan variabel `count` yang diatur menggunakan operasi modulo. Operasi *dequeue* hanya memajukan penunjuk `front` **tanpa menggeser satu pun data di dalam larik**, sehingga kinerjanya konsisten di angka $O(1)$.



### M3: Sort & Search + Analisis Kompleksitas

Modul `m3_periksa.py` menyediakan fungsi laporan harian terurut dan pencarian data spesifik, dengan kewajiban melacak **jumlah perbandingan** (*comparison count*) untuk membuktikan teori kompleksitas secara empiris:

* **Insertion Sort ($O(n^2)$)**: Mengurutkan data secara *in-place* dan stabil dengan cara menggeser elemen ke kiri. Sangat efisien untuk data kecil atau data yang hampir terurut, namun dibatasi maksimal 20.000 baris pada aplikasi untuk mencegah pembekuan (*freezing*) sistem.
* **Merge Sort ($O(n \log n)$)**: Algoritma *Divide and Conquer* yang membelah larik menjadi dua bagian secara rekursif dan menggabungkannya kembali. Stabil dan sangat tangguh menangani skala data penuh hingga 200.000 baris.
* **Linear Search ($O(n)$)**: Mencari target dengan memeriksa elemen satu per satu dari awal tanpa mensyaratkan data dalam keadaan terurut.
* **Binary Search ($O(\log n)$)**: Teknik pencarian cepat dengan membuang separuh sisa rentang data pada tiap langkah perbandingan. Menuntut data harus diurutkan terlebih dahulu (menggunakan Merge Sort di awal).

---
##  Struktur Direktori & Penjelasan
Repositori ini diorganisasikan menjadi tiga *layer* utama untuk memisahkan data, logika komputasi, dan antarmuka pengguna:

```text
2ez4u/
├── README.md               # Dokumentasi lengkap proyek
├── data/
│   ├── pesanan.csv         # Database utama berisi 200.000 baris data pesanan
│   └── peta.csv            # Data peta wilayah untuk Milestone 6 (M6)
├── backend/
│   ├── m1_pesanan.py       # (M1) Modul struktur data Array dinamis & Linked List
│   ├── m2_antrean.py       # (M2) Modul Stack, Postfix Kasir, Antrean Naif & Circular
│   └── m3_periksa.py       # (M3) Modul Algoritma Sorting (Insertion/Merge) & Searching
└── frontend/
    └── ui.py               # Modul GUI Tkinter untuk interaksi dan visualisasi performa

```
---

