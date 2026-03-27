import tkinter as tk
from tkinter import ttk, messagebox

from services.student_service import (
    get_info,
    get_grades,
    register_course_logic,
    get_registered_courses,
    get_all_subjects
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

        self.tabs.add(self.tab_i, text="Thông tin")
        self.tabs.add(self.tab_g, text="Điểm")
        self.tabs.add(self.tab_r, text="Đăng ký")

        # Load dữ liệu ban đầu
        self.load_info()
        self.ui_grades()
        self.ui_registration()

    # ================= TAB INFO =================
    def load_info(self):
        try:
            res = get_info(self.ma_sv)
            if not res: return

            frame = tk.LabelFrame(self.tab_i, text="Hồ sơ sinh viên", font=("Arial", 12, "bold"))
            frame.pack(padx=20, pady=20, fill="both")

            fields = [
                ("Mã SV", self.ma_sv), ("Họ tên", res[0]), ("Ngày sinh", res[1]),
                ("Địa chỉ", res[2]), ("Giới tính", res[3]), ("SĐT", res[4]),
                ("Mã lớp", res[5]), ("Năm thứ", res[6]), ("Khóa học", res[7]),
            ]

            for k, v in fields:
                row = tk.Frame(frame)
                row.pack(fill="x", pady=3)
                tk.Label(row, text=k, width=15, anchor="w").pack(side="left")
                tk.Label(row, text=v).pack(side="left")
        except Exception as e:
            messagebox.showerror("Lỗi Info", str(e))

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

        tk.Button(self.tab_g, text="🔄 Load Điểm", command=self.load_grades).pack(pady=5)
        self.load_grades()

    def load_grades(self):
        for item in self.tree_grades.get_children(): self.tree_grades.delete(item)
        rows = get_grades(self.ma_sv)
        if rows:
            for r in rows:
                clean_row = [str(item) if item is not None else "" for item in r]
                self.tree_grades.insert("", tk.END, values=clean_row)

    # ================= TAB REGISTER (FIXED INDENTATION) =================
    def ui_registration(self):
        # Frame nhập liệu
        frame_input = tk.Frame(self.tab_r)
        frame_input.pack(fill="x", pady=10)

        tk.Label(frame_input, text="Chọn môn:").pack(side="left", padx=5)

        # Lấy danh sách từ DB
        subjects = get_all_subjects()
        subject_values = [f"{s[0]} - {s[1]}" for s in subjects]

        self.ent_mahp = ttk.Combobox(frame_input, values=subject_values, width=35, state="readonly")
        self.ent_mahp.pack(side="left", padx=5)
        if subject_values: self.ent_mahp.current(0)

        tk.Label(frame_input, text="HK:").pack(side="left", padx=5)
        self.ent_hk = ttk.Combobox(frame_input, values=["1", "2", "3"], width=5, state="readonly")
        self.ent_hk.pack(side="left")
        self.ent_hk.current(0)

        tk.Label(frame_input, text="Năm:").pack(side="left", padx=5)
        self.ent_nh = tk.Entry(frame_input, width=12)
        self.ent_nh.pack(side="left", padx=5)
        self.ent_nh.insert(0, "2024-2025")

        tk.Button(frame_input, text="Đăng ký", bg="#2ecc71", fg="white", font=("Arial", 9, "bold"),
                  command=self.register_course).pack(side="left", padx=10)

        # Bảng hiển thị các môn đã đăng ký
        tk.Label(self.tab_r, text="DANH SÁCH MÔN ĐÃ ĐĂNG KÝ", font=("Arial", 10, "bold")).pack(pady=5)
        cols = ("mahp", "tenhp", "hk", "nh")
        self.tree_reg = ttk.Treeview(self.tab_r, columns=cols, show="headings")
        headers = ["Mã HP", "Tên HP", "Học kỳ", "Năm học"]

        for c, h in zip(cols, headers):
            self.tree_reg.heading(c, text=h)
            self.tree_reg.column(c, width=150, anchor="center")

        self.tree_reg.pack(fill="both", expand=True, padx=10, pady=10)
        self.load_registered_courses()

    def register_course(self):
        selection = self.ent_mahp.get()
        if not selection:
            messagebox.showwarning("Thiếu dữ liệu", "Vui lòng chọn môn học!")
            return

        ma_hp = selection.split(" - ")[0].strip()
        hk = self.ent_hk.get()
        nh = self.ent_nh.get().strip()

        success, msg = register_course_logic(self.ma_sv, ma_hp, hk, nh)
        if success:
            messagebox.showinfo("OK", msg)
            self.load_registered_courses()
        else:
            messagebox.showerror("Lỗi", msg)

    def load_registered_courses(self):
        for item in self.tree_reg.get_children(): self.tree_reg.delete(item)
        rows = get_registered_courses(self.ma_sv)
        if rows:
            for r in rows:
                clean_row = [str(item) if item is not None else "" for item in r]
                self.tree_reg.insert("", tk.END, values=clean_row)

    # ================= LOGOUT =================
    def dang_xuat(self):
        if messagebox.askyesno("Xác nhận", "Bạn có chắc chắn muốn đăng xuất?"):
            self.root.destroy()
            self.login_win.deiconify()