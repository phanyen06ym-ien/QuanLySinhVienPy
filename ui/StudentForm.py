import tkinter as tk
from tkinter import ttk, messagebox
from datetime import datetime

from services.StudentService import StudentService


class StudentForm:
    def __init__(self, root, ma_sv, login_win):
        self.root = root
        self.login_win = login_win
        self.ma_sv = ma_sv

        self.root.title(f"Hệ thống Sinh viên - Mã SV: {ma_sv}")
        self.root.geometry("950x600")

        # ===== LOGOUT =====
        tk.Button(self.root, text="Đăng xuất",
                  bg="#e74c3c", fg="white",
                  command=self.dang_xuat).pack(anchor="ne", padx=10, pady=10)

        # ===== TABS =====
        self.tabs = ttk.Notebook(self.root)
        self.tabs.pack(fill=tk.BOTH, expand=True)

        self.tab_i = tk.Frame(self.tabs)
        self.tab_g = tk.Frame(self.tabs)
        self.tab_r = tk.Frame(self.tabs)

        self.tabs.add(self.tab_i, text="Thông tin")
        self.tabs.add(self.tab_g, text="Điểm")
        self.tabs.add(self.tab_r, text="Đăng ký")

        self.load_info()
        self.ui_grades()
        self.ui_registration()

    # ================= INFO =================
    def load_info(self):
        res = StudentService.get_info(self.ma_sv)

        if not res:
            tk.Label(self.tab_i, text="Không có dữ liệu").pack()
            return

        frame = tk.LabelFrame(self.tab_i, text="Hồ sơ sinh viên")
        frame.pack(padx=20, pady=20, fill="both")

        def format_date(d):
            if isinstance(d, datetime):
                return d.strftime("%Y-%m-%d")
            return str(d) if d else ""

        fields = [
            ("Mã SV", self.ma_sv),
            ("Họ tên", res[0]),
            ("Ngày sinh", format_date(res[1])),
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
            tk.Label(row, text=str(v) if v else "").pack(side="left")

    # ================= GRADES =================
    def ui_grades(self):
        cols = ("mahp", "tenhp", "hk", "nh", "cc", "bt", "gk", "ck", "tk")

        self.tree_grades = ttk.Treeview(self.tab_g, columns=cols, show="headings")

        headers = ["Mã HP", "Tên HP", "HK", "Năm", "CC", "BT", "GK", "CK", "TK"]

        for c, h in zip(cols, headers):
            self.tree_grades.heading(c, text=h)
            self.tree_grades.column(c, width=90, anchor="center")

        self.tree_grades.column("tenhp", width=200)
        self.tree_grades.pack(fill="both", expand=True, padx=10, pady=10)

        tk.Button(self.tab_g, text="Load điểm",
                  command=self.load_grades).pack(pady=5)

        self.load_grades()

    def load_grades(self):
        self.tree_grades.delete(*self.tree_grades.get_children())

        rows = StudentService.get_grades(self.ma_sv)

        for r in rows:
            clean_row = []
            for item in r:
                if isinstance(item, float):
                    clean_row.append(f"{item:.1f}")
                else:
                    clean_row.append(str(item) if item else "")
            self.tree_grades.insert("", tk.END, values=clean_row)

    # ================= REGISTER =================
    def ui_registration(self):
        frame = tk.Frame(self.tab_r)
        frame.pack(pady=10)

        tk.Label(frame, text="Chọn môn").pack(side="left")

        subjects = StudentService.get_all_subjects() or []
        self.subject_map = {f"{s[0]} - {s[1]}": s[0] for s in subjects}

        self.ent_mahp = ttk.Combobox(frame,
                                    values=list(self.subject_map.keys()),
                                    width=35,
                                    state="readonly")
        self.ent_mahp.pack(side="left", padx=5)

        if self.subject_map:
            self.ent_mahp.current(0)

        tk.Label(frame, text="HK").pack(side="left")
        self.ent_hk = ttk.Combobox(frame,
                                  values=["1", "2", "3"],
                                  width=5,
                                  state="readonly")
        self.ent_hk.pack(side="left")
        self.ent_hk.current(0)

        tk.Label(frame, text="Năm").pack(side="left")
        self.ent_nh = tk.Entry(frame, width=12)
        self.ent_nh.pack(side="left", padx=5)
        self.ent_nh.insert(0, "2024-2025")

        tk.Button(frame, text="Đăng ký",
                  bg="green", fg="white",
                  command=self.register_course).pack(side="left", padx=10)

        # ===== TABLE =====
        tk.Label(self.tab_r, text="MÔN ĐÃ ĐĂNG KÝ").pack()

        cols = ("mahp", "tenhp", "hk", "nh")
        self.tree_reg = ttk.Treeview(self.tab_r, columns=cols, show="headings")

        headers = ["Mã HP", "Tên HP", "HK", "Năm"]

        for c, h in zip(cols, headers):
            self.tree_reg.heading(c, text=h)
            self.tree_reg.column(c, width=150, anchor="center")

        self.tree_reg.pack(fill="both", expand=True, padx=10, pady=10)

        self.load_registered_courses()

    def register_course(self):
        selected = self.ent_mahp.get()

        if not selected or selected not in self.subject_map:
            messagebox.showwarning("Lỗi", "Chọn môn học hợp lệ!")
            return

        ma_hp = self.subject_map[selected]
        hk = self.ent_hk.get()
        nh = self.ent_nh.get().strip()

        ok = StudentService.register_course(self.ma_sv, ma_hp, hk, nh)

        if ok:
            messagebox.showinfo("OK", "Đăng ký thành công")
            self.load_registered_courses()
        else:
            messagebox.showerror("Lỗi", "Đăng ký thất bại")

    def load_registered_courses(self):
        self.tree_reg.delete(*self.tree_reg.get_children())

        rows = StudentService.get_registered_courses(self.ma_sv)

        for r in rows:
            self.tree_reg.insert("", tk.END,
                                 values=[str(i) if i else "" for i in r])

    # ================= LOGOUT =================
    def dang_xuat(self):
        if messagebox.askyesno("Xác nhận", "Bạn muốn đăng xuất?"):
            self.root.destroy()
            self.login_win.deiconify()