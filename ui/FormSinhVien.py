import tkinter as tk
from tkinter import ttk
from database.connect import get_connection


class StudentForm:
    def __init__(self, root, ma_sv, login_win):
        self.root = root
        self.ma_sv = ma_sv
        self.login_win = login_win

        self.root.title(f"Sinh viên: {ma_sv}")
        self.root.geometry("800x500")

        tk.Button(root, text="Đăng xuất", command=self.dang_xuat).pack(anchor="ne")

        self.tabs = ttk.Notebook(root)
        self.tabs.pack(fill=tk.BOTH, expand=True)

        self.tab1 = tk.Frame(self.tabs)
        self.tabs.add(self.tab1, text="Thông tin")

        self.tab2 = tk.Frame(self.tabs)
        self.tabs.add(self.tab2, text="Điểm")

        self.load_info()
        self.load_grades()

    def load_info(self):
        conn = get_connection()
        if conn:
            cursor = conn.cursor()
            cursor.execute(
                "SELECT HoTen FROM SINHVIEN WHERE MaSV=?",
                (self.ma_sv,)
            )
            row = cursor.fetchone()

            if row:
                tk.Label(self.tab1, text=row[0]).pack()

            conn.close()

    def load_grades(self):
        tree = ttk.Treeview(self.tab2, columns=("hp", "diem"), show="headings")
        tree.heading("hp", text="Học phần")
        tree.heading("diem", text="Điểm")
        tree.pack(fill=tk.BOTH, expand=True)

        conn = get_connection()
        if conn:
            cursor = conn.cursor()
            cursor.execute(
                "SELECT MaHP, Diem FROM KetQua WHERE MaSV=?",
                (self.ma_sv,)
            )

            for row in cursor.fetchall():
                tree.insert("", tk.END, values=row)

            conn.close()

    def dang_xuat(self):
        self.root.destroy()
        self.login_win.deiconify()