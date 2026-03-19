import tkinter as tk
from tkinter import ttk
from database.connect import get_connection


class LecturerForm:
    def __init__(self, root, ma_gv, login_win, role):
        self.root = root
        self.login_win = login_win

        self.root.title(f"Giảng viên: {ma_gv}")
        self.root.geometry("800x500")

        tk.Button(root, text="Đăng xuất", command=self.dang_xuat).pack(anchor="ne")

        self.tabs = ttk.Notebook(root)
        self.tabs.pack(fill=tk.BOTH, expand=True)

        self.tab1 = tk.Frame(self.tabs)
        self.tabs.add(self.tab1, text="Danh sách lớp")

        self.load_classes()

    def load_classes(self):
        tree = ttk.Treeview(self.tab1, columns=("ma", "ten"), show="headings")
        tree.heading("ma", text="Mã lớp")
        tree.heading("ten", text="Tên lớp")
        tree.pack(fill=tk.BOTH, expand=True)

        conn = get_connection()
        if conn:
            cursor = conn.cursor()
            cursor.execute("SELECT MaLop, TenLop FROM LOPHOC")

            for row in cursor.fetchall():
                tree.insert("", tk.END, values=row)

            conn.close()

    def dang_xuat(self):
        self.root.destroy()
        self.login_win.deiconify()