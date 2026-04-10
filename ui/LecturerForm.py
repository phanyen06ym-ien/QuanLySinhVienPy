import tkinter as tk
from tkinter import ttk, messagebox
from services.LecturerService import LecturerService

class LecturerForm:
    def __init__(self, root, ma_id, login_win, role):
        self.root = root
        self.login_win = login_win
        self.ma_id = ma_id
        self.role = role

        self.root.title(f"Hệ Thống Giảng Viên - GV: {ma_id}")
        self.root.geometry("1150x700")

        tk.Button(self.root, text="Đăng xuất",
                  bg="#e74c3c", fg="white",
                  command=self.dang_xuat).pack(anchor="ne", padx=10, pady=5)

        self.tabs = ttk.Notebook(self.root)
        self.tabs.pack(fill=tk.BOTH, expand=True)

        # Tabs
        self.tab0 = tk.Frame(self.tabs)
        self.tab1 = tk.Frame(self.tabs)
        self.tab2 = tk.Frame(self.tabs)

        self.tabs.add(self.tab0, text="Thông tin")
        self.tabs.add(self.tab1, text="Lớp & Học phần")
        self.tabs.add(self.tab2, text="Nhập điểm")

        self.ui_info()
        self.ui_classes_subjects()
        self.ui_grades()
        self.auto_load_first_subject()

    # ================= INFO =================
    def ui_info(self):
        res = LecturerService.get_info(self.ma_id)

        if not res:
            tk.Label(self.tab0, text="Không có dữ liệu").pack()
            return

        frame = tk.LabelFrame(self.tab0, text="Thông tin giảng viên")
        frame.pack(padx=20, pady=20, fill="both")

        # FIX: đủ 7 cột theo VIEW
        labels = [
            "Mã GV", "Họ tên", "Giới tính",
            "Email", "Địa chỉ",
            "Mã khoa", "Tên khoa"
        ]

        for i, val in enumerate(res):
            if i >= len(labels):  # chống crash
                break

            row = tk.Frame(frame)
            row.pack(fill="x", pady=5)

            tk.Label(row, text=labels[i], width=15, anchor="w").pack(side="left")
            tk.Label(row, text=str(val) if val else "").pack(side="left")

    # ================= LỚP & HỌC PHẦN =================
    def ui_classes_subjects(self):
        container = tk.Frame(self.tab1)
        container.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

        # ===== LỚP =====
        frame_lop = tk.LabelFrame(container, text="Lớp phụ trách")
        frame_lop.pack(fill=tk.X, pady=10)

        self.tree_lop = ttk.Treeview(frame_lop,
                                    columns=("ma", "ten", "nganh"),
                                    show="headings", height=4)

        self.tree_lop.heading("ma", text="Mã lớp")
        self.tree_lop.heading("ten", text="Tên lớp")
        self.tree_lop.heading("nganh", text="Chuyên ngành")

        self.tree_lop.pack(fill=tk.X, padx=10, pady=10)

        # ===== HỌC PHẦN =====
        frame_hp = tk.LabelFrame(container, text="Học phần giảng dạy")
        frame_hp.pack(fill=tk.BOTH, expand=True)

        self.tree_hp = ttk.Treeview(
            frame_hp,
            columns=("malop", "tenlop", "mahp", "tenhp", "tc", "hk", "nam", "phong"),
            show="headings"
        )

        headers = ["Mã lớp", "Tên lớp", "Mã HP", "Tên HP", "Tín chỉ", "HK", "Năm", "Phòng"]

        for c, h in zip(self.tree_hp["columns"], headers):
            self.tree_hp.heading(c, text=h)
            self.tree_hp.column(c, anchor="center", width=120)

        self.tree_hp.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

        self.tree_hp.bind("<<TreeviewSelect>>", self.on_subject_click)

        tk.Button(container, text="Load",
                  command=self.refresh_tab1).pack(pady=5)

        self.refresh_tab1()

    def refresh_tab1(self):
        self.load_classes()
        self.load_subjects()

    def load_classes(self):
        self.tree_lop.delete(*self.tree_lop.get_children())
        rows = LecturerService.get_classes(self.ma_id)

        for r in rows:
            self.tree_lop.insert("", tk.END,
                                 values=[str(i) if i else "" for i in r])

    def on_subject_click(self, event):
        sel = self.tree_hp.selection()
        if not sel:
            return

        val = self.tree_hp.item(sel[0])["values"]

        # val = (malop, tenlop, mahp, tenhp, tc, hk, nam, phong)

        self.tabs.select(2)

        self.entries["mhp"].delete(0, tk.END)
        self.entries["mhp"].insert(0, val[2])

        self.entries["hk"].delete(0, tk.END)
        self.entries["hk"].insert(0, val[5])

        self.entries["nh"].delete(0, tk.END)
        self.entries["nh"].insert(0, val[6])

        self.load_grades()


    def load_subjects(self):
        self.tree_hp.delete(*self.tree_hp.get_children())
        rows = LecturerService.get_subjects(self.ma_id)

        for r in rows:
            self.tree_hp.insert("", tk.END, values=(
                r[0],  # MaLop
                r[1],  # TenLop
                r[2],  # MaHP
                r[3],  # TenHP
                r[4],  # TinChi
                r[5],  # HocKy
                r[6],  # NamHoc
                r[7]  # PhongHoc
            ))

    # ================= ĐIỂM =================
    def ui_grades(self):
        frame = tk.LabelFrame(self.tab2, text="Nhập điểm")
        frame.pack(fill=tk.X, padx=10, pady=10)

        labels = ["Mã SV", "Mã HP", "HK", "Năm", "CC", "BT", "GK", "CK"]
        keys = ["msv", "mhp", "hk", "nh", "cc", "bt", "gk", "ck"]

        self.entries = {}

        for i, (text, key) in enumerate(zip(labels, keys)):
            tk.Label(frame, text=text).grid(row=i // 4, column=(i % 4) * 2)
            e = tk.Entry(frame)
            e.grid(row=i // 4, column=(i % 4) * 2 + 1)
            self.entries[key] = e

        # Buttons
        btn = tk.Frame(self.tab2)
        btn.pack()

        tk.Button(btn, text="Lưu", bg="green", fg="white",
                  command=self.save_grade).pack(side=tk.LEFT, padx=5)

        tk.Button(btn, text="Xóa", bg="orange",
                  command=self.delete_grade).pack(side=tk.LEFT, padx=5)

        tk.Button(btn, text="Load",
                  command=self.load_grades).pack(side=tk.LEFT, padx=5)

        # Table
        cols = ("msv", "ten", "lop", "mhp", "tenhp", "tc", "hk", "nh", "cc", "bt", "gk", "ck", "tk")

        self.tree_diem = ttk.Treeview(
            self.tab2,
            columns=cols,
            show="headings"
        )

        headers = [
            "MSV", "Tên", "Lớp", "MHP", "Tên HP", "TC",
            "HK", "Năm", "CC", "BT", "GK", "CK", "TK"
        ]

        for c, h in zip(cols, headers):
            self.tree_diem.heading(c, text=h)
            self.tree_diem.column(c, anchor="center", width=90)

        self.tree_diem.pack(fill=tk.BOTH, expand=True)

        self.tree_diem.bind("<<TreeviewSelect>>", self.on_select)

    def load_grades(self):
        print("ĐANG LOAD...")  # debug

        self.tree_diem.delete(*self.tree_diem.get_children())

        self.tree_diem.update()

        mhp = self.entries["mhp"].get().strip()
        hk = self.entries["hk"].get().strip()
        nh = self.entries["nh"].get().strip()

        if not mhp:
            messagebox.showwarning("Thiếu", "Nhập mã học phần")
            return

        rows = LecturerService.get_grades(
            mhp,
            hk if hk else None,
            nh if nh else None
        )

        print("DATA:", rows)  # debug

        if not rows:
            messagebox.showinfo("Thông báo", "Không có dữ liệu")
            return

        for r in rows:
            self.tree_diem.insert("", tk.END, values=(
                r[0], r[1], r[2], r[3], r[4],
                r[5], r[6], r[7],
                r[8] or 0,
                r[9] or 0,
                r[10] or 0,
                r[11] or 0,
                r[12] or 0
            ))

    def save_grade(self):
        try:
            data = (
                self.entries["msv"].get(),
                self.entries["mhp"].get(),
                self.entries["hk"].get(),
                self.entries["nh"].get(),
                float(self.entries["cc"].get() or 0),
                float(self.entries["bt"].get() or 0),
                float(self.entries["gk"].get() or 0),
                float(self.entries["ck"].get() or 0),
            )
            LecturerService.insert_grade(data)

            messagebox.showinfo("OK", "Đã lưu")

            self.load_grades()

        except Exception as e:
            messagebox.showerror("Lỗi", str(e))

    def delete_grade(self):
        sel = self.tree_diem.selection()
        if not sel:
            messagebox.showwarning("Thiếu", "Chọn dòng để xóa")
            return

        val = self.tree_diem.item(sel[0])["values"]

        # val = (msv, ten, lop, mhp, tenhp, tc, hk, nh, ...)

        LecturerService.delete_grade(
            val[0],  # MaSV
            val[3],  # MaHP
            val[6],  # HocKy
            val[7]  # NamHoc
        )

        messagebox.showinfo("OK", "Đã xóa")
        self.load_grades()

    def on_select(self, event):
        sel = self.tree_diem.selection()
        if not sel:
            return

        val = self.tree_diem.item(sel[0])["values"]

        self.entries["msv"].delete(0, tk.END)
        self.entries["msv"].insert(0, val[0])

        self.entries["mhp"].delete(0, tk.END)
        self.entries["mhp"].insert(0, val[3])

        self.entries["hk"].delete(0, tk.END)
        self.entries["hk"].insert(0, val[6])

        self.entries["nh"].delete(0, tk.END)
        self.entries["nh"].insert(0, val[7])

        self.entries["cc"].delete(0, tk.END)
        self.entries["cc"].insert(0, val[8])

        self.entries["bt"].delete(0, tk.END)
        self.entries["bt"].insert(0, val[9])

        self.entries["gk"].delete(0, tk.END)
        self.entries["gk"].insert(0, val[10])

        self.entries["ck"].delete(0, tk.END)
        self.entries["ck"].insert(0, val[11])

    def auto_load_first_subject(self):
        try:
            rows = LecturerService.get_subjects(self.ma_id)

            if not rows:
                return

            r = rows[0]

            # r = (MaLop, TenLop, MaHP, TenHP, TinChi, HocKy, NamHoc, PhongHoc)

            self.entries["mhp"].delete(0, tk.END)
            self.entries["mhp"].insert(0, r[2])

            self.entries["hk"].delete(0, tk.END)
            self.entries["hk"].insert(0, r[5])

            self.entries["nh"].delete(0, tk.END)
            self.entries["nh"].insert(0, r[6])

            self.load_grades()

        except Exception as e:
            print("Auto load lỗi:", e)

    def dang_xuat(self):
        self.root.destroy()
        self.login_win.deiconify()