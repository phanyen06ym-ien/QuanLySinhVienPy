import tkinter as tk
from tkinter import ttk, messagebox

from services.student_service import (
    get_info,
    get_grades,
    register_course_logic,
    get_registered_courses
)


class StudentForm:
    def __init__(self, root, ma_sv, login_win):
        self.root = root
        self.login_win = login_win
        self.ma_sv = ma_sv

        self.root.title(f"Hệ thống Sinh viên - Mã SV: {ma_sv}")
        self.root.geometry("950x600")

        # ================= LOGOUT =================
        btn_logout = tk.Button(
            self.root,
            text="Đăng xuất",
            bg="#e74c3c",
            fg="white",
            font=("Arial", 10, "bold"),
            command=self.dang_xuat
        )
        btn_logout.pack(anchor="ne", padx=15, pady=10)

        # ================= TABS =================
        self.tabs = ttk.Notebook(self.root)
        self.tabs.pack(fill=tk.BOTH, expand=True)

        self.tab_i = tk.Frame(self.tabs, bg="#f5f6fa")
        self.tab_g = tk.Frame(self.tabs, bg="#f5f6fa")
        self.tab_r = tk.Frame(self.tabs, bg="#f5f6fa")

        self.tabs.add(self.tab_i, text="👤 Thông tin")
        self.tabs.add(self.tab_g, text="📝 Điểm")
        self.tabs.add(self.tab_r, text="📚 Đăng ký")

        # load
        self.load_info()
        self.ui_grades()
        self.ui_registration()

    # ================= TAB INFO =================
    def load_info(self):
        try:
            res = get_info(self.ma_sv)
            if not res:
                return

            frame = tk.LabelFrame(
                self.tab_i,
                text="Hồ sơ sinh viên",
                font=("Arial", 12, "bold")
            )
            frame.pack(padx=20, pady=20, fill="both")

            fields = [
                ("Mã SV", self.ma_sv),
                ("Họ tên", res[0]),
                ("Ngày sinh", res[1]),
                ("Địa chỉ", res[2]),
                ("Giới tính", res[3]),
                ("SĐT", res[4]),
                ("Mã lớp", res[5]),
                ("Năm thứ", res[6]),
                ("Khóa học", res[7]),
            ]

            for k, v in fields:
                row = tk.Frame(frame)
                row.pack(fill="x", pady=3)

                tk.Label(row, text=k, width=15, anchor="w").pack(side="left")
                tk.Label(row, text=v).pack(side="left")

        except Exception as e:
            messagebox.showerror("Lỗi", str(e))

    # ================= TAB GRADES =================
    def ui_grades(self):
        cols = ("mahp", "tenhp", "hk", "nh", "cc", "bt", "gk", "ck", "tk")

        self.tree_grades = ttk.Treeview(self.tab_g, columns=cols, show="headings")

        headers = ["Mã HP", "Tên HP", "HK", "Năm", "CC", "BT", "GK", "CK", "TK"]

        for c, h in zip(cols, headers):
            self.tree_grades.heading(c, text=h)
            self.tree_grades.column(c, width=90, anchor="center")

        self.tree_grades.column("tenhp", width=200)

        self.tree_grades.pack(fill="both", expand=True, padx=10, pady=10)

        tk.Button(
            self.tab_g,
            text="🔄 Load",
            command=self.load_grades
        ).pack(pady=5)

        self.load_grades()

    def load_grades(self):
        for item in self.tree_grades.get_children():
            self.tree_grades.delete(item)

        rows = get_grades(self.ma_sv)
        if rows:
            for r in rows:
                clean_row = [str(item) if item is not None else "" for item in r]
                self.tree_grades.insert("", tk.END, values=clean_row)

    # ================= TAB REGISTER =================
    def ui_registration(self):
        frame = tk.Frame(self.tab_r)
        frame.pack(fill="x", pady=10)

        tk.Label(frame, text="Mã HP").pack(side="left", padx=5)
        self.ent_mahp = tk.Entry(frame, width=15)
        self.ent_mahp.pack(side="left")

        tk.Label(frame, text="Học kỳ").pack(side="left", padx=5)
        self.ent_hk = ttk.Combobox(frame, values=["1", "2", "3"], width=5)
        self.ent_hk.pack(side="left")
        self.ent_hk.current(0)

        tk.Label(frame, text="Năm học").pack(side="left", padx=5)
        self.ent_nh = tk.Entry(frame, width=12)
        self.ent_nh.pack(side="left")
        self.ent_nh.insert(0, "2024-2025")

        tk.Button(
            frame,
            text="Đăng ký",
            bg="#2ecc71",
            fg="white",
            command=self.register_course
        ).pack(side="left", padx=10)

        # bảng môn đã đăng ký
        cols = ("mahp", "tenhp", "hk", "nh")

        self.tree_reg = ttk.Treeview(self.tab_r, columns=cols, show="headings")

        headers = ["Mã HP", "Tên HP", "Học kỳ", "Năm học"]

        for c, h in zip(cols, headers):
            self.tree_reg.heading(c, text=h)
            self.tree_reg.column(c, width=120)

        self.tree_reg.pack(fill="both", expand=True, padx=10, pady=10)

        self.load_registered_courses()

    def register_course(self):
        ma_hp = self.ent_mahp.get().strip()
        hk = self.ent_hk.get()
        nh = self.ent_nh.get().strip()

        if not ma_hp:
            messagebox.showwarning("Thiếu dữ liệu", "Nhập mã học phần!")
            return

        success, msg = register_course_logic(self.ma_sv, ma_hp, hk, nh)

        if success:
            messagebox.showinfo("OK", msg)
            self.load_registered_courses()
        else:
            messagebox.showerror("Lỗi", msg)

    def load_registered_courses(self):
        for item in self.tree_reg.get_children():
            self.tree_reg.delete(item)

        rows = get_registered_courses(self.ma_sv)

        if rows:
            for r in rows:
                clean_row = [str(item) if item is not None else "" for item in r]
                self.tree_reg.insert("", tk.END, values=clean_row)

    # ================= LOGOUT =================
    def dang_xuat(self):
        if messagebox.askyesno("Xác nhận", "Đăng xuất?"):
            self.root.destroy()
            self.login_win.deiconify()