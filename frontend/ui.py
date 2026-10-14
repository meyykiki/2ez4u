import os
import sys
import time
import tkinter as tk
from tkinter import ttk, messagebox, filedialog

# Tambahkan path parent agar folder backend bisa di-import
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), ".."))

try:
    from backend.m1_pesanan import Array, LinkList, Pesanan, baca_csv
    from backend.m2_antrean import SistemAntrean, hitung_struk
    from backend.m3_periksa import insertion_sort, merge_sort, linear_search, binary_search
except ImportError as e:
    print(f"Error import backend: {e}")
    print("Pastikan script ini dijalankan di dalam folder 'frontend' dan folder 'backend' ada di parent direktori.")
    sys.exit(1)


class Aplikasi2EZ4U(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("2EZ4U Food Delivery")
        # Perbaikan geometry: pastikan tidak ada spasi di sekitar 'x'
        self.geometry("1200x800")
        self.configure(bg="#f0f0f0")

        # ==========================================
        # STATE & STRUKTUR DATA (M1, M2, M3)
        # ==========================================
        self.m1_array = Array()
        self.m1_linklist = LinkList()
        self.m2_sistem = SistemAntrean()
        self.m3_data_raw = [] # Format list of list untuk M3
        
        self.active_module = ""
        
        self._konfigurasi_style()
        self._buat_layout_utama()

    def _konfigurasi_style(self):
        style = ttk.Style()
        style.theme_use("clam")
        
        # Gaya untuk Header utama
        style.configure("Header.TFrame", background="#1e3d59")
        style.configure("Header.TLabel", background="#1e3d59", foreground="white", font=("Arial", 16, "bold"))
        
        # Gaya Treeview
        style.configure("Treeview", rowheight=25, font=("Consolas", 9))
        style.configure("Treeview.Heading", font=("Arial", 10, "bold"))
        
        # Gaya Tombol Menu Kiri
        style.configure("Menu.TButton", font=("Arial", 9), anchor="w")
        style.configure("MenuTitle.TLabel", font=("Arial", 9, "bold"), foreground="#1e3d59", padding=(5, 10, 5, 2))

    def _buat_layout_utama(self):
        # 1. Header (Biru Tua)
        header_frame = ttk.Frame(self, style="Header.TFrame", padding=10)
        header_frame.pack(side=tk.TOP, fill=tk.X)
        ttk.Label(header_frame, text="2EZ4U Food Delivery", style="Header.TLabel").pack(side=tk.LEFT)

        # 2. Area Utama (Split Pane Kiri & Kanan)
        main_pane = ttk.PanedWindow(self, orient=tk.HORIZONTAL)
        main_pane.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)

        # -- PANEL KIRI (Menu Sidebar) --
        left_frame = ttk.Frame(main_pane, width=250)
        main_pane.add(left_frame, weight=0)
        self._buat_sidebar_menu(left_frame)

        # -- PANEL KANAN (Konten Dinamis, Tabel, Log) --
        right_frame = ttk.Frame(main_pane)
        main_pane.add(right_frame, weight=1)

        # Panel Kanan Atas: Kontrol / Form Dinamis
        self.top_control_frame = ttk.Frame(right_frame, padding=10, relief=tk.GROOVE)
        self.top_control_frame.pack(side=tk.TOP, fill=tk.X, pady=(0, 5))
        
        # Teks Judul Dinamis
        self.lbl_judul_menu = ttk.Label(self.top_control_frame, text="Pilih menu di samping", font=("Arial", 14, "bold"))
        self.lbl_judul_menu.pack(anchor=tk.W)
        self.lbl_desc_menu = ttk.Label(self.top_control_frame, text="", font=("Arial", 10), foreground="gray")
        self.lbl_desc_menu.pack(anchor=tk.W, pady=(0, 10))
        
        # Container untuk form dinamis (entry, combobox, tombol aksi)
        self.form_container = ttk.Frame(self.top_control_frame)
        self.form_container.pack(fill=tk.X, expand=True)

        # Panel Kanan Tengah: Treeview (Tabel)
        tree_frame = ttk.Frame(right_frame)
        tree_frame.pack(fill=tk.BOTH, expand=True, pady=5)
        
        self.tree = ttk.Treeview(tree_frame, show="headings", selectmode="browse")
        vsb = ttk.Scrollbar(tree_frame, orient="vertical", command=self.tree.yview)
        hsb = ttk.Scrollbar(tree_frame, orient="horizontal", command=self.tree.xview)
        self.tree.configure(yscrollcommand=vsb.set, xscrollcommand=hsb.set)
        
        self.tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        vsb.pack(side=tk.RIGHT, fill=tk.Y)
        hsb.pack(side=tk.BOTTOM, fill=tk.X)

        # Panel Kanan Bawah: Command Log (Terminal Simulasi)
        log_frame = ttk.LabelFrame(right_frame, text="COMMAND", padding=5)
        log_frame.pack(side=tk.BOTTOM, fill=tk.X)
        
        self.txt_log = tk.Text(log_frame, height=6, font=("Consolas", 9), bg="#fdfdfd")
        self.txt_log.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        
        log_vsb = ttk.Scrollbar(log_frame, orient="vertical", command=self.txt_log.yview)
        log_vsb.pack(side=tk.RIGHT, fill=tk.Y)
        self.txt_log.configure(yscrollcommand=log_vsb.set)
        
        # Status bar
        self.status_var = tk.StringVar(value="[Ready] Silakan muat data.")
        ttk.Label(self, textvariable=self.status_var, background="#1e3d59", foreground="white", font=("Consolas", 9)).pack(side=tk.BOTTOM, fill=tk.X)

    def _buat_sidebar_menu(self, parent):
        # Frame bisa digulir jika menu banyak
        canvas = tk.Canvas(parent, highlightthickness=0)
        scroll = ttk.Scrollbar(parent, orient="vertical", command=canvas.yview)
        menu_frame = ttk.Frame(canvas)

        menu_frame.bind("<Configure>", lambda e: canvas.configure(scrollregion=canvas.bbox("all")))
        canvas.create_window((0, 0), window=menu_frame, anchor="nw")
        canvas.configure(yscrollcommand=scroll.set)

        canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scroll.pack(side=tk.RIGHT, fill=tk.Y)

        # ================= DATA =================
        ttk.Label(menu_frame, text="DATA", style="MenuTitle.TLabel").pack(fill=tk.X)
        ttk.Button(menu_frame, text="Load Data CSV", style="Menu.TButton", command=self._load_data).pack(fill=tk.X, padx=5, pady=1)

        # ================= M1 =================
        ttk.Label(menu_frame, text="M1 - DATA PESANAN", style="MenuTitle.TLabel").pack(fill=tk.X)
        m1_menus = [
            ("ARRAY - LIHAT PESANAN", lambda: self._tampil_form_m1("array", "lihat")),
            ("ARRAY - TAMBAH PESANAN REGULER", lambda: self._tampil_form_m1("array", "tambah_reguler")),
            ("ARRAY - TAMBAH PESANAN PRIORITAS", lambda: self._tampil_form_m1("array", "tambah_prioritas")),
            ("ARRAY - TAMBAH PESANAN VIP", lambda: self._tampil_form_m1("array", "tambah_vip")),
            ("LINKEDLIST - LIHAT PESANAN", lambda: self._tampil_form_m1("linkedlist", "lihat")),
        ]
        for teks, cmd in m1_menus:
            ttk.Button(menu_frame, text=teks, style="Menu.TButton", command=cmd).pack(fill=tk.X, padx=5, pady=1)

        # ================= M2 =================
        ttk.Label(menu_frame, text="M2 - STACK DAN QUEUE", style="MenuTitle.TLabel").pack(fill=tk.X)
        m2_menus = [
            ("STACK - POSTFIX (MESIN KASIR)", self._tampil_form_m2_postfix),
            ("STACK - UNDO", self._aksi_m2_undo),
            ("STACK - REDO", self._aksi_m2_redo),
            ("QUEUE - ENQUEUE", self._tampil_form_m2_enqueue),
            ("QUEUE - DEQUEUE NAIF", lambda: self._tampil_form_m2_dequeue("naif")),
            ("QUEUE - DEQUEUE CIRCULAR", lambda: self._tampil_form_m2_dequeue("circular"))
        ]
        for teks, cmd in m2_menus:
            ttk.Button(menu_frame, text=teks, style="Menu.TButton", command=cmd).pack(fill=tk.X, padx=5, pady=1)

        # ================= M3 =================
        ttk.Label(menu_frame, text="M3 - SORT DAN SEARCH", style="MenuTitle.TLabel").pack(fill=tk.X)
        m3_menus = [
            ("SORT - INSERTION SORT", lambda: self._tampil_form_m3_sort("insertion")),
            ("SORT - MERGE SORT", lambda: self._tampil_form_m3_sort("merge")),
            ("SEARCH - LINEAR SEARCH", lambda: self._tampil_form_m3_search("linear")),
            ("SEARCH - BINARY SEARCH", lambda: self._tampil_form_m3_search("binary")),
        ]
        for teks, cmd in m3_menus:
            ttk.Button(menu_frame, text=teks, style="Menu.TButton", command=cmd).pack(fill=tk.X, padx=5, pady=1)

    # ====================================================================
    # HELPER FUNGSI GUI
    # ====================================================================
    def _bersihkan_form(self):
        for widget in self.form_container.winfo_children():
            widget.destroy()

    def _setup_kolom_pesanan(self):
        cols = ["#", "oid", "pelanggan", "resto", "menu", "harga", "prioritas", "masuk", "selesai", "status"]
        self.tree.config(columns=cols)
        
        widths = [40, 80, 150, 120, 120, 80, 60, 80, 80, 70]
        for c, w in zip(cols, widths):
            self.tree.heading(c, text=c.upper())
            self.tree.column(c, width=w, anchor=tk.W if c in ["pelanggan", "resto", "menu"] else tk.CENTER)

    def _isi_tabel_pesanan(self, data_list, start_idx=1):
        self.tree.delete(*self.tree.get_children())
        for i, item in enumerate(data_list):
            if isinstance(item, Pesanan):
                val = (i + start_idx, item.oid, item.pelanggan, item.resto, item.menu, 
                       f"{item.harga:,}", item.prioritas, item.t_masuk, item.t_selesai or "-", item.status)
            else:
                # Format raw list (M3)
                # item index: 0=oid, 1=pelanggan, 2=resto, 3=menu, 4=harga, 5=prioritas, 6=t_masuk, 7=t_selesai, 8=status
                val = (i + start_idx, item[0], item[1], item[2], item[3], 
                       f"{item[4]:,}", item[5] if len(item)>5 else 3, 
                       item[6] if len(item)>6 else "-", 
                       item[7] if len(item)>7 and item[7] else "-", 
                       item[8] if len(item)>8 else "-")
            self.tree.insert("", tk.END, values=val)

    def log(self, cmd, modul, ms, extra=""):
        teks = f"{cmd:<20} -> {modul:<20} {ms:7.2f} ms {extra}\n"
        self.txt_log.insert(tk.END, teks)
        self.txt_log.see(tk.END)
        self.status_var.set(f"[{modul}] {ms:.2f} ms")

    # ====================================================================
    # LOAD DATA
    # ====================================================================
    def _load_data(self):
        # Gunakan path relatif fallback jika dialog batal
        base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        default_path = os.path.join(base_dir, 'data', 'pesanan.csv')
        
        filepath = filedialog.askopenfilename(initialdir=base_dir, filetypes=[("CSV", "*.csv")], title="Pilih pesanan.csv")
        if not filepath:
            filepath = default_path
            
        if not os.path.exists(filepath):
            messagebox.showerror("Error", f"File tidak ditemukan:\n{filepath}")
            return
            
        try:
            self.lbl_judul_menu.config(text="Memuat Data...")
            self.update()
            
            t0 = time.perf_counter()
            # 1. Load ke M1 (Array & LinkedList)
            data_m1 = baca_csv(filepath)
            self.m1_array = Array(len(data_m1) + 10)
            self.m1_linklist = LinkList()
            for p in data_m1:
                self.m1_array.append(p)
                self.m1_linklist.append(p)
            
            # 2. Load ke M2 (Sistem Antrean)
            self.m2_sistem = SistemAntrean()
            self.m2_sistem.isi_dari(data_m1)
            
            # 3. Load ke M3 (Raw list)
            # Konversi objek M1 ke raw list untuk konsistensi di M3
            self.m3_data_raw = [
                [p.oid, p.pelanggan, p.resto, p.menu, p.harga, p.prioritas, p.t_masuk, p.t_selesai, p.status]
                for p in data_m1
            ]
            
            t_ms = (time.perf_counter() - t0) * 1000
            msg = f"Berhasil memuat {len(data_m1):,} baris pesanan."
            self.lbl_judul_menu.config(text="Data Berhasil Dimuat")
            self.lbl_desc_menu.config(text=msg)
            self.log("load_data", "I/O", t_ms)
            messagebox.showinfo("Sukses", msg)
            
            self._setup_kolom_pesanan()
            # Tampilkan 1000 baris pertama untuk preview agar UI tidak freeze
            self._isi_tabel_pesanan(data_m1[:1000]) 
            
        except Exception as e:
            messagebox.showerror("Gagal Memuat Data", f"Terjadi kesalahan: {e}")

    # ====================================================================
    # M1 LOGIC
    # ====================================================================
    def _tampil_form_m1(self, struktur, aksi):
        self._bersihkan_form()
        self._setup_kolom_pesanan()
        
        is_array = (struktur == "array")
        ds_obj = self.m1_array if is_array else self.m1_linklist
        
        if aksi == "lihat":
            self.lbl_judul_menu.config(text=f"{struktur.capitalize()}: Lihat Pesanan")
            self.lbl_desc_menu.config(text=f"Total data di {struktur}: {len(ds_obj):,}")
            # Render maks 1000 di UI
            self._isi_tabel_pesanan(ds_obj.isi()[:1000] if is_array else ds_obj.isi()[:1000])
            self.log(f"{struktur}_lihat", "M1 - pesanan", 0.0)
            
        elif "tambah" in aksi:
            prio = 1 if "vip" in aksi else (2 if "prioritas" in aksi else 3)
            prio_teks = ["VIP (Depan)", "PRIORITAS (Tengah)", "REGULER (Belakang)"][prio-1]
            
            self.lbl_judul_menu.config(text=f"{struktur.capitalize()}: Tambah Pesanan {prio_teks}")
            self.lbl_desc_menu.config(text=f"Menyisipkan pada posisi yang sesuai dengan prioritas.")
            
            ttk.Label(self.form_container, text="Nama Pelanggan:").grid(row=0, column=0, padx=5, pady=5)
            ent_nama = ttk.Entry(self.form_container, width=30)
            ent_nama.grid(row=0, column=1, padx=5, pady=5)
            
            def do_tambah():
                nama = ent_nama.get().strip() or "Pelanggan Baru"
                oid_baru = f"O-{len(ds_obj) + 100000}"
                p = Pesanan(oid_baru, nama, "kafe-teknik", "menu-tes", 15000, prio, 0, None, "ANTRE")
                
                t0 = time.perf_counter()
                ds_obj.tambah(p)
                ms = (time.perf_counter() - t0) * 1000
                
                self.log(f"{struktur}_tambah", "M1 - pesanan", ms)
                self._isi_tabel_pesanan(ds_obj.isi()[:1000] if is_array else ds_obj.isi()[:1000])
                self.lbl_desc_menu.config(text=f"Pesanan {oid_baru} ditambahkan. Waktu eksekusi: {ms:.3f} ms")
                
            ttk.Button(self.form_container, text="TAMBAH", command=do_tambah).grid(row=0, column=2, padx=10, pady=5)

    # ====================================================================
    # M2 LOGIC (Sesuai Screenshot)
    # ====================================================================
    def _tampil_form_m2_postfix(self):
        self._bersihkan_form()
        self.lbl_judul_menu.config(text="Stack: hitung struk lewat postfix")
        self.lbl_desc_menu.config(text="Struk diubah ke postfix, lalu dihitung dua tahap dengan stack.")
        
        ttk.Label(self.form_container, text="Struk belanja (infix):").grid(row=0, column=0, padx=5, pady=5)
        ent_exp = ttk.Entry(self.form_container, width=40)
        ent_exp.insert(0, "( 3 * 12000 ) + ( 2 * 8500 ) - 5000")
        ent_exp.grid(row=0, column=1, padx=5, pady=5)
        
        def do_hitung():
            ekspresi = ent_exp.get()
            try:
                t0 = time.perf_counter()
                pf_str, total, langkah = hitung_struk(ekspresi)
                ms = (time.perf_counter() - t0) * 1000
                
                self.log("stack_postfix", "M2 - stack", ms)
                self.lbl_desc_menu.config(text=f"Postfix: {pf_str}\nTOTAL: Rp {total:,}")
                
                # Ubah kolom Treeview khusus Postfix[cite: 12]
                cols = ["langkah", "token", "tindakan", "stack", "output"]
                self.tree.config(columns=cols)
                widths = [60, 80, 250, 200, 250]
                for c, w in zip(cols, widths):
                    self.tree.heading(c, text=c)
                    self.tree.column(c, width=w, anchor=tk.W)
                    
                self.tree.delete(*self.tree.get_children())
                for l in langkah:
                    self.tree.insert("", tk.END, values=l)
                    
            except Exception as e:
                messagebox.showerror("Error Kasir", str(e))
                
        ttk.Button(self.form_container, text="HITUNG", command=do_hitung).grid(row=0, column=2, padx=10)

    def _tampil_form_m2_enqueue(self):
        self._bersihkan_form()
        self._setup_kolom_pesanan()
        self.lbl_judul_menu.config(text="Queue: pesanan baru masuk ke belakang")
        self.lbl_desc_menu.config(text="Menambah pesanan di ujung belakang kedua antrean sekaligus.")
        
        ttk.Label(self.form_container, text="Nama pelanggan:").grid(row=0, column=0, padx=5, pady=5)
        ent_nama = ttk.Entry(self.form_container, width=30)
        ent_nama.insert(0, "X2")
        ent_nama.grid(row=0, column=1, padx=5, pady=5)
        
        def do_enqueue():
            p = self.m2_sistem.pesanan_baru(ent_nama.get().strip() or "Anonim")
            t0 = time.perf_counter()
            self.m2_sistem.enqueue(p)
            ms = (time.perf_counter() - t0) * 1000
            
            self.log("queue_enqueue", "M2 - queue", ms)
            
            # Format tampilan hasil seperti screenshot "kolom | isi"[cite: 16]
            self.tree.config(columns=["kolom", "isi"])
            self.tree.heading("kolom", text="kolom")
            self.tree.heading("isi", text="isi")
            self.tree.column("kolom", width=150)
            self.tree.column("isi", width=400)
            self.tree.delete(*self.tree.get_children())
            
            info = [("oid", p.oid), ("pelanggan", p.pelanggan), ("resto", p.resto), 
                    ("menu", p.menu), ("harga", f"{p.harga:,}"), ("prioritas", p.prioritas),
                    ("masuk", p.t_masuk), ("selesai", "-"), ("status", p.status)]
            
            for k, v in info:
                self.tree.insert("", tk.END, values=(k, v))
                
            self.lbl_desc_menu.config(text=f"{p.oid} masuk ke barisan paling belakang pada KEDUA antrean.\n"
                                           f"Panjang sekarang: naif {len(self.m2_sistem.naif):,}, circular {len(self.m2_sistem.circ):,}")
                                           
        ttk.Button(self.form_container, text="ENQUEUE", command=do_enqueue).grid(row=0, column=2, padx=10)

    def _tampil_form_m2_dequeue(self, tipe):
        self._bersihkan_form()
        self._setup_kolom_pesanan()
        
        if tipe == "naif":
            self.lbl_judul_menu.config(text="Queue naif: ambil dari depan dengan menggeser isi")
            self.lbl_desc_menu.config(text="Mengambil indeks 0 lalu menggeser seluruh sisa isi ke kiri. Biayanya O(n).")
        else:
            self.lbl_judul_menu.config(text="Queue circular: ambil dari depan dengan memajukan penunjuk")
            self.lbl_desc_menu.config(text="Hanya penunjuk front yang maju, isi larik tidak digeser sama sekali.")
            
        ttk.Label(self.form_container, text="Berapa kali dequeue:").grid(row=0, column=0, padx=5, pady=5)
        ent_n = ttk.Entry(self.form_container, width=10)
        ent_n.insert(0, "2")
        ent_n.grid(row=0, column=1, padx=5, pady=5)
        
        def do_dequeue():
            try:
                n = int(ent_n.get())
            except ValueError:
                n = 1
                
            t0 = time.perf_counter()
            keluar, geser = self.m2_sistem.dequeue(tipe, n)
            ms = (time.perf_counter() - t0) * 1000
            
            self.log(f"queue_dequeue_{tipe}", "M2 - queue", ms)
            
            avg_geser = geser / n if n > 0 else 0
            if tipe == "naif":
                msg = (f"{len(keluar)} pesanan keluar dari depan antrean {tipe}.\n"
                       f"Total {geser:,} elemen digeser, rata-rata {avg_geser:,.0f} geseran per dequeue.\n"
                       f"Sisa antrean {tipe} {len(self.m2_sistem._antrean(tipe)):,}.")
            else:
                msg = (f"{len(keluar)} pesanan keluar dari depan antrean {tipe}.\n"
                       f"Tidak ada elemen yang digeser. front sekarang {self.m2_sistem.circ.front}, "
                       f"rear {self.m2_sistem.circ.rear}, kapasitas {self.m2_sistem.circ.kapasitas()}.\n"
                       f"Sisa antrean {tipe} {len(self.m2_sistem.circ):,}.")
            
            self.lbl_desc_menu.config(text=msg)
            self._isi_tabel_pesanan(keluar, start_idx=1)
            
        ttk.Button(self.form_container, text="DEQUEUE", command=do_dequeue).grid(row=0, column=2, padx=10)

    def _aksi_m2_undo(self):
        self._bersihkan_form()
        self._setup_kolom_pesanan()
        self.lbl_judul_menu.config(text="Stack: batalkan aksi antrean terakhir")
        
        t0 = time.perf_counter()
        msg_undo = self.m2_sistem.undo_last()
        ms = (time.perf_counter() - t0) * 1000
        
        self.log("stack_undo", "M2 - stack", ms)
        self.lbl_desc_menu.config(text=f"{msg_undo}\n"
                                       f"Panjang antrean sekarang: naif {len(self.m2_sistem.naif):,}, circular {len(self.m2_sistem.circ):,}. "
                                       f"Tumpukan undo {len(self.m2_sistem.undo)}, redo {len(self.m2_sistem.redo)}.")
        # Refresh treeview dengan isi antrean saat ini
        self._isi_tabel_pesanan(self.m2_sistem.circ.isi()[:1000])

    def _aksi_m2_redo(self):
        self._bersihkan_form()
        self._setup_kolom_pesanan()
        self.lbl_judul_menu.config(text="Stack: kerjakan lagi aksi yang dibatalkan")
        
        t0 = time.perf_counter()
        msg_redo = self.m2_sistem.redo_last()
        ms = (time.perf_counter() - t0) * 1000
        
        self.log("stack_redo", "M2 - stack", ms)
        self.lbl_desc_menu.config(text=f"{msg_redo}\n"
                                       f"Panjang antrean sekarang: naif {len(self.m2_sistem.naif):,}, circular {len(self.m2_sistem.circ):,}. "
                                       f"Tumpukan undo {len(self.m2_sistem.undo)}, redo {len(self.m2_sistem.redo)}.")
        self._isi_tabel_pesanan(self.m2_sistem.circ.isi()[:1000])

    # ====================================================================
    # M3 LOGIC (Sesuai Screenshot Sort/Search)
    # ====================================================================
    def _tampil_form_m3_sort(self, tipe):
        self._bersihkan_form()
        self._setup_kolom_pesanan()
        
        if tipe == "insertion":
            self.lbl_judul_menu.config(text="Sort: insertion sort, O(n²)")
            self.lbl_desc_menu.config(text="Setiap elemen digeser mundur sampai menemukan tempatnya. Biayanya tumbuh kuadratik.")
        else:
            self.lbl_judul_menu.config(text="Sort: merge sort, O(n log n)")
            self.lbl_desc_menu.config(text="Larik dibelah dua terus-menerus, lalu potongan yang sudah terurut disatukan kembali.")
            
        ttk.Label(self.form_container, text="Jumlah baris diurutkan:").grid(row=0, column=0, padx=5, pady=5)
        ent_n = ttk.Entry(self.form_container, width=15)
        ent_n.insert(0, "4000" if tipe == "merge" else "10")
        ent_n.grid(row=0, column=1, padx=5, pady=5)
        
        ttk.Label(self.form_container, text="Diurutkan menurut:").grid(row=0, column=2, padx=5, pady=5)
        cmb_kunci = ttk.Combobox(self.form_container, values=["oid", "harga", "selesai"], state="readonly", width=10)
        cmb_kunci.current(0)
        cmb_kunci.grid(row=0, column=3, padx=5, pady=5)
        
        def do_sort():
            try:
                n_baris = int(ent_n.get())
            except ValueError:
                n_baris = 100
                
            kunci_str = cmb_kunci.get()
            kunci_map = {"oid": 0, "harga": 4, "selesai": 7}
            idx_kunci = kunci_map.get(kunci_str, 0)
            
            data_uji = [row.copy() for row in self.m3_data_raw[:n_baris]]
            
            try:
                t0 = time.perf_counter()
                if tipe == "insertion":
                    hasil, banding, pindah = insertion_sort(data_uji, idx_kunci)
                else:
                    hasil, banding, pindah = merge_sort(data_uji, idx_kunci)
                ms = (time.perf_counter() - t0) * 1000
                
                self.log(f"sort_{tipe}_sort", f"M3 - {tipe} sort", ms)
                
                self.lbl_desc_menu.config(text=f"{n_baris:,} pesanan diurutkan menurut {kunci_str}.\n"
                                               f"{banding:,} perbandingan, {pindah:,} pemindahan.")
                # Tampilkan maksimal 1000 data teratas agar UI tidak nge-lag
                self._isi_tabel_pesanan(hasil[:1000])
                
            except ValueError as e:
                # Menangani penolakan data > 20.000 pada insertion sort[cite: 23]
                messagebox.showwarning("DITOLAK", str(e))
                self.lbl_desc_menu.config(text=str(e))
                
        ttk.Button(self.form_container, text="URUTKAN", command=do_sort).grid(row=0, column=4, padx=15)

    def _tampil_form_m3_search(self, tipe):
        self._bersihkan_form()
        self._setup_kolom_pesanan()
        
        if tipe == "linear":
            self.lbl_judul_menu.config(text="Search: linear search, O(n)")
            self.lbl_desc_menu.config(text="Memeriksa pesanan satu per satu dari depan. Tidak menuntut data terurut.")
        else:
            self.lbl_judul_menu.config(text="Search: binary search, O(log n)")
            self.lbl_desc_menu.config(text="Membuang separuh sisa daftar pada setiap perbandingan. Menuntut daftar terurut (oid).")
            
        ttk.Label(self.form_container, text="Nomor pesanan (oid):").grid(row=0, column=0, padx=5, pady=5)
        ent_target = ttk.Entry(self.form_container, width=20)
        ent_target.insert(0, "O-137442")
        ent_target.grid(row=0, column=1, padx=5, pady=5)
        
        def do_search():
            target = ent_target.get().strip()
            idx_kunci = 0 # Asumsi pencarian selalu berdasarkan OID untuk demo M3
            
            if tipe == "linear":
                t0 = time.perf_counter()
                idx_temu, banding = linear_search(self.m3_data_raw, target, idx_kunci)
                ms = (time.perf_counter() - t0) * 1000
                self.log("search_linear", "M3 - search", ms)
                
                if idx_temu != -1:
                    item = self.m3_data_raw[idx_temu]
                    self.lbl_desc_menu.config(text=f"Ditemukan pada indeks {idx_temu:,}.\n{banding:,} perbandingan.")
                    self._isi_tabel_pesanan([item])
                else:
                    self.lbl_desc_menu.config(text=f"Tidak ditemukan.\n{banding:,} perbandingan.")
                    self.tree.delete(*self.tree.get_children())
                    
            elif tipe == "binary":
                # Harus bangun daftar terurut OID sekali menggunakan merge sort[cite: 23]
                t_sort_0 = time.perf_counter()
                data_terurut, _, _ = merge_sort(self.m3_data_raw, 0)
                ms_sort = (time.perf_counter() - t_sort_0) * 1000
                
                t_search_0 = time.perf_counter()
                idx_temu, banding = binary_search(data_terurut, target, 0)
                ms_search = (time.perf_counter() - t_search_0) * 1000
                
                self.log("search_binary", "M3 - search", ms_search, extra=f"(+ {ms_sort:.2f} ms sort)")
                
                if idx_temu != -1:
                    item = data_terurut[idx_temu]
                    self.lbl_desc_menu.config(
                        text=f"Daftar terurut oid dibangun sekali dengan merge sort, {ms_sort:.2f} ms.\n"
                             f"Ditemukan pada baris ke-{idx_temu:,} dari {len(data_terurut):,} baris.\n"
                             f"{banding:,} perbandingan, bandingkan dengan linear search."
                    )
                    self._isi_tabel_pesanan([item])
                else:
                    self.lbl_desc_menu.config(text=f"Tidak ditemukan dalam {banding:,} perbandingan.")
                    self.tree.delete(*self.tree.get_children())
                    
        ttk.Button(self.form_container, text="CARI", command=do_search).grid(row=0, column=2, padx=15)


if __name__ == "__main__":
    app = Aplikasi2EZ4U()
    app.mainloop()