import tkinter as tk
from tkinter import ttk, messagebox
import services.lecturer_service as LecturerService

class LecturerForm:
    def __init__(self, root, ma_id, login_win, role):
        self.root = root
        self.login_win = login_win
        self.ma_id = ma_id
        self.role = role

        self.root.title(f"Hệ Thống Giảng Viên - GV: {ma_id}")
        self.root.geometry("1150x700")

        tk.Button(
            self.root, text="Đăng xuất",
            bg="#e74c3c", fg="white",
            command=self.dang_xuat
        ).pack(anchor="ne", padx=10, pady=5)

        self.tabs = ttk.Notebook(self.root)
        self.tabs.pack(fill=tk.BOTH, expand=True)

        # TAB 1
        self.tab0 = tk.Frame(self.tabs)
        self.tabs.add(self.tab0, text="Thông tin cá nhân")
        self.ui_info()

        # TAB 2
        self.tab1 = tk.Frame(self.tabs)
        self.tabs.add(self.tab1, text="Lớp phụ trách")
        self.ui_classes()

        # TAB 3
        self.tab2 = tk.Frame(self.tabs)
        self.tabs.add(self.tab2, text="Quản lý điểm")
        self.ui_grades()

    # ================= INFO =================
    def ui_info(self):
        res = LecturerService.get_info(self.ma_id)
        if not res:
            return

        frame = tk.LabelFrame(self.tab0, text="Hồ sơ giảng viên",
                              font=("Arial", 12, "bold"))
        frame.pack(padx=30, pady=30, fill="both")

        fields = [
            ("Mã GV", res[0]),
            ("Họ tên", res[1]),
            ("Giới tính", res[2]),
            ("Địa chỉ", res[3]),
            ("Email", res[4]),
            ("Mã khoa", res[5]),
        ]

        for k, v in fields:
            row = tk.Frame(frame)
            row.pack(fill="x", pady=5)

            tk.Label(row, text=k, width=15, anchor="w",
                     font=("Arial", 11, "bold")).pack(side="left")

            tk.Label(row, text=v or "", font=("Arial", 11)).pack(side="left")

    # ================= CLASS =================
    def ui_classes(self):
        cols = ("ma", "ten", "nganh")
        self.tree_lop = ttk.Treeview(self.tab1, columns=cols, show="headings")

        self.tree_lop.heading("ma", text="Mã Lớp")
        self.tree_lop.heading("ten", text="Tên Lớp")
        self.tree_lop.heading("nganh", text="Chuyên ngành")

        self.tree_lop.column("ma", width=100, anchor="center")
        self.tree_lop.column("ten", width=200, anchor="w")
        self.tree_lop.column("nganh", width=250, anchor="w")

        self.tree_lop.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

        tk.Button(
            self.tab1,
            text="Tải danh sách lớp",
            bg="#3498db",
            fg="white",
            command=self.load_classes
        ).pack(pady=5)

        self.load_classes()

    def load_classes(self):
        for i in self.tree_lop.get_children():
            self.tree_lop.delete(i)

        rows = LecturerService.get_classes(self.ma_id)
        if rows:
            for r in rows:
                clean_row = [str(item) if item is not None else "" for item in r]
                self.tree_lop.insert("", tk.END, values=clean_row)

    # ================= GRADES =================
    def ui_grades(self):
        frame = tk.LabelFrame(self.tab2, text="Nhập điểm")
        frame.pack(fill=tk.X, padx=10, pady=10)

        labels = [
            ("Mã SV", "msv"), ("Họ tên", "hoten"), ("Mã HP", "mhp"),
            ("HK", "hk"), ("Năm", "nh"), ("CC", "cc"),
            ("BT", "bt"), ("GK", "gk"), ("CK", "ck")
        ]

        self.entries = {}
        for i, (text, key) in enumerate(labels):
            tk.Label(frame, text=text).grid(row=i // 3, column=(i % 3) * 2)
            e = tk.Entry(frame, width=18)
            e.grid(row=i // 3, column=(i % 3) * 2 + 1)
            self.entries[key] = e

        btn_frame = tk.Frame(self.tab2)
        btn_frame.pack(pady=5)

        tk.Button(btn_frame, text="Lưu", bg="green", fg="white", command=self.save_grade).pack(side=tk.LEFT, padx=5)
        tk.Button(btn_frame, text="Xóa", bg="orange", fg="white", command=self.delete_grade).pack(side=tk.LEFT, padx=5)
        tk.Button(btn_frame, text="Load", bg="blue", fg="white", command=self.load_grades).pack(side=tk.LEFT, padx=5)

        cols = ("msv", "ten", "mhp", "hk", "nh", "cc", "bt", "gk", "ck", "tk")
        self.tree_diem = ttk.Treeview(self.tab2, columns=cols, show="headings")
        for c in cols:
            self.tree_diem.heading(c, text=c.upper())
            self.tree_diem.column(c, width=90, anchor="center")

        self.tree_diem.pack(fill=tk.BOTH, expand=True)
        self.tree_diem.bind("<<TreeviewSelect>>", self.on_select)
        self.load_grades()

    def save_grade(self):
        try:
            LecturerService.save_grade(
                self.entries["msv"].get(),
                self.entries["mhp"].get(),
                self.entries["hk"].get(),
                self.entries["nh"].get(),
                float(self.entries["cc"].get() or 0),
                float(self.entries["bt"].get() or 0),
                float(self.entries["gk"].get() or 0),
                float(self.entries["ck"].get() or 0),
            )
            messagebox.showinfo("OK", "Đã lưu!")
            self.load_grades()
        except Exception as e:
            messagebox.showerror("Lỗi", f"Sai dữ liệu hoặc lỗi: {e}")

    def delete_grade(self):
        sel = self.tree_diem.selection()
        if not sel: return
        val = self.tree_diem.item(sel[0])["values"]
        if messagebox.askyesno("Xóa", "Xóa dòng này?"):
            LecturerService.delete_grade(val[0], val[2], val[3], val[4])
            self.load_grades()

    def load_grades(self):
        for i in self.tree_diem.get_children():
            self.tree_diem.delete(i)
        rows = LecturerService.get_grades()
        if rows:
            for r in rows:
                clean_row = [str(item) if item is not None else "" for item in r]
                self.tree_diem.insert("", tk.END, values=clean_row)

    def on_select(self, event):
        sel = self.tree_diem.selection()
        if not sel: return
        val = self.tree_diem.item(sel[0])["values"]
        keys = ["msv", "hoten", "mhp", "hk", "nh", "cc", "bt", "gk", "ck"]
        for i, k in enumerate(keys):
            self.entries[k].delete(0, tk.END)
            self.entries[k].insert(0, val[i])

    def dang_xuat(self):
        self.root.destroy()
        self.login_win.deiconify()