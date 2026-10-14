# 2EZ4U Food Delivery - Backend Engine & UI System 🛵🍔

Dokumentasi resmi proyek akhir mata kuliah **Struktur Data dan Analisis Algoritma (EC234303)**. Proyek ini mengembangkan *engine backend* layanan pesan-antar makanan/barang versi mini (*GoFood/GrabFood/ShopeeFood*) secara mandiri menggunakan Python murni serta antarmuka grafis (*GUI*) berbasis Tkinter[cite: 3].

---

## 📋 Daftar Isi
1. [Deskripsi Proyek](#-deskripsi-proyek)
2. [Aturan Main & Batasan Teknis](#-aturan-main--batasan-teknis)
3. [Alat & Teknologi](#️-alat--teknologi-yang-digunakan)
4. [Struktur Direktori & Penjelasan](#-struktur-direktori-dan-penjelasan)
5. [Diagram Arsitektur Sistem](#-diagram-arsitektur-sistem)
6. [Cara Menjalankan Aplikasi](#-cara-menjalankan-aplikasi)
7. [Penjelasan Detail Milestone & Fitur (M1 - M3)](#-penjelasan-detail-milestone--fitur-m1---m3)
   * [Milestone 1: Array vs Linked List (M1)](#m1-data-pesanan-array-vs-linked-list)
   * [Milestone 2: Stack & Queue + Undo/Redo (M2)](#m2-stack--queue--undoredo)
   * [Milestone 3: Sort & Search + Analisis Kompleksitas (M3)](#m3-sort--search--analisis-kompleksitas)
8. [Kontributor](#-kontributor)

---

## 📖 Deskripsi Proyek
**2EZ4U** dirancang untuk menangani trafik sistem pemesanan berskala besar dengan simulasi basis data mencapai **200.000 baris data CSV**[cite: 3, 26]. Titik berat penilaian bukan pada estetika tampilan *frontend*, melainkan pada **implementasi murni struktur data dan algoritma buatan sendiri** untuk menguji performa, efisiensi memori, serta kompleksitas waktu eksekusi (*Time Complexity*)[cite: 3].

---

## ⚙️ Aturan Main & Batasan Teknis
Sesuai dengan spesifikasi proyek, pengembangan backend mematuhi aturan ketat berikut:
* **Proyek Individu**: Dikembangkan sepenuhnya secara mandiri[cite: 4].
* **Larangan Penggunaan Fungsi Instan**: Dilarang keras menggunakan fungsi bawaan Python seperti `dict`, `set`, `sorted()`, `.sort()`, `heapq`, `bisect`, modul `collections`, literatur kurung kurawal `{}` untuk kamus, serta *dictionary/set comprehension*[cite: 4].
* **Pengecualian yang Diizinkan**: Penggunaan struktur data `list` bawaan dibatasi hanya sebagai array primitif, serta diperbolehkan menggunakan `tuple`, operasi aritmetika dasar, dan fungsi *I/O* standar[cite: 4].

---

## 🛠️ Alat & Teknologi yang Digunakan
* **Bahasa Pemrograman**: Python versi 3.11+[cite: 3]
* **Antarmuka (GUI)**: Pustaka standar Python Tkinter[cite: 4]
* **Manajemen Data**: Berkas CSV mentah[cite: 4] (*Comma Separated Values*)
* **IDE**: Visual Studio Code

---

## 📁 Struktur Direktori & Penjelasan
Repositori ini diorganisasikan menjadi tiga *layer* utama untuk memisahkan data, logika komputasi, dan antarmuka pengguna[cite: 3]:

```text
2ez4u/
├── README.md               # Dokumentasi lengkap proyek
├── data/
│   ├── pesanan.csv         # Database utama berisi 200.000 baris data pesanan[cite: 3]
│   └── peta.csv            # Data peta wilayah untuk Milestone 6 (M6)[cite: 4]
├── backend/
│   ├── m1_pesanan.py       # (M1) Modul struktur data Array dinamis & Linked List[cite: 4]
│   ├── m2_antrean.py       # (M2) Modul Stack, Postfix Kasir, Antrean Naif & Circular[cite: 4]
│   └── m3_pesanan.py       # (M3) Modul Algoritma Sorting (Insertion/Merge) & Searching[cite: 4]
└── frontend/
    └── ui.py               # Modul GUI Tkinter untuk interaksi dan visualisasi performa[cite: 4]