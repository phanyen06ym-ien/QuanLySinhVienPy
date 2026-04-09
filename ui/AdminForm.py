import tkinter as tk
from tkinter import ttk, messagebox, filedialog
import openpyxl
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

from services.AdminService import AdminService

admin_service = AdminService()


class AdminForm:
    def __init__(self, root, ma_admin, login_win):
        self.root = root
        self.login_win = login_win
        self.ma_id = ma_admin

        self.root.title(f"Admin - {ma_admin}")
        self.root.geometry("1200x700")

        # Khởi tạo các biến Treeview để tránh lỗi warning IDE
        self.tree_tk = None
        self.tree_sv = None
        self.tree_hp = None
        self.tree_rp = None

        # Nút đăng xuất
        tk.Button(self.root, text="Đăng xuất",
                  bg="#e74c3c", fg="white", font=("Arial", 10, "bold"),
                  command=self.dang_xuat).pack(anchor="ne", padx=10, pady=5)

        # Tabs hệ thống
        self.tabs = ttk.Notebook(self.root)
        self.tabs.pack(fill=tk.BOTH, expand=True)

        self.tab_users = tk.Frame(self.tabs)
        self.tab_students = tk.Frame(self.tabs)
        self.tab_teachers = tk.Frame(self.tabs)
        self.tab_courses = tk.Frame(self.tabs)
        self.tab_report = tk.Frame(self.tabs)
        self.tab_assign = tk.Frame(self.tabs)

        self.tabs.add(self.tab_users, text="Quản lý Tài khoản")
        self.tabs.add(self.tab_students, text="Sinh viên")
        self.tabs.add(self.tab_teachers, text="Giảng viên")
        self.tabs.add(self.tab_assign, text="Phân công")
        self.tabs.add(self.tab_courses, text="Học phần")
        self.tabs.add(self.tab_report, text="Báo cáo & Thống kê")



        # Khởi tạo giao diện từng Tab
        self.ui_taikhoan()
        self.ui_sinhvien()
        self.ui_giangvien()
        self.ui_phancong()
        self.ui_hocphan()
        self.ui_baocao()

    def dang_xuat(self):
        if messagebox.askyesno("Xác nhận", "Bạn có chắc chắn muốn đăng xuất?"):
            self.root.destroy()
            self.login_win.deiconify()

    # ================= TAB: TÀI KHOẢN (ĐÃ FIX) =================
    def ui_taikhoan(self):
        f = tk.Frame(self.tab_users)
        f.pack(pady=15)

        tk.Label(f, text="Username:", font=("Arial", 10)).grid(row=0, column=0, padx=5)
        self.tk_user = tk.Entry(f, width=20)
        self.tk_user.grid(row=0, column=1, padx=5)

        tk.Label(f, text="Role:", font=("Arial", 10)).grid(row=0, column=2, padx=5)
        self.tk_role = ttk.Combobox(f, values=["SV", "GV", "ADMIN"], width=10, state="readonly")
        self.tk_role.grid(row=0, column=3, padx=5)
        self.tk_role.current(0)

        # Các nút chức năng
        btn_frame = tk.Frame(self.tab_users)
        btn_frame.pack(pady=5)

        tk.Button(btn_frame, text="Thêm mới", bg="#2ecc71", fg="white", width=12, command=self.add_tk).pack(
            side=tk.LEFT, padx=5)
        tk.Button(btn_frame, text="Xóa", bg="#e67e22", fg="white", width=12, command=self.del_tk).pack(side=tk.LEFT,
                                                                                                       padx=5)
        tk.Button(btn_frame, text="Làm mới (Load)", bg="#3498db", fg="white", width=12, command=self.load_tk).pack(
            side=tk.LEFT, padx=5)

        # Cấu trúc bảng Treeview: Thêm cột "Tên người dùng"
        columns = ("u", "p", "r", "n")
        self.tree_tk = ttk.Treeview(self.tab_users, columns=columns, show="headings")

        self.tree_tk.heading("u", text="Tên tài khoản")
        self.tree_tk.heading("p", text="Mật khẩu")
        self.tree_tk.heading("r", text="Vai trò")
        self.tree_tk.heading("n", text="Tên người dùng (Họ tên)")

        self.tree_tk.column("u", width=150, anchor="w")
        self.tree_tk.column("p", width=100, anchor="center")
        self.tree_tk.column("r", width=100, anchor="center")
        self.tree_tk.column("n", width=250, anchor="w")

        self.tree_tk.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        self.load_tk()

    def load_tk(self):
        """Load dữ liệu tài khoản (đúng theo VIEW 3 cột)"""
        self.tree_tk.delete(*self.tree_tk.get_children())

        try:
            data = admin_service.get_all_taikhoan()

            for r in data:
                # VIEW: TenDangNhap | VaiTro | TenNguoiDung
                username = r[0]
                role = r[1]
                name = r[2]

                safe_row = (username, "******", role, name)

                self.tree_tk.insert("", tk.END, values=safe_row)

        except Exception as e:
            messagebox.showerror("Lỗi load dữ liệu", str(e))

    def add_tk(self):
        u = self.tk_user.get().strip()
        r = self.tk_role.get()
        if not u:
            messagebox.showwarning("Chú ý", "Vui lòng nhập Username")
            return

        # Mật khẩu mặc định khi thêm mới là 123456
        if admin_service.add_taikhoan(u, "123456", r):
            messagebox.showinfo("Thành công", f"Đã thêm tài khoản {u}")
            self.load_tk()
            self.tk_user.delete(0, tk.END)

    def del_tk(self):
        sel = self.tree_tk.selection()
        if not sel:
            messagebox.showwarning("Chú ý", "Chọn tài khoản cần xóa trong bảng")
            return

        u = self.tree_tk.item(sel[0])['values'][0]
        if messagebox.askyesno("Xác nhận", f"Xóa tài khoản {u}?"):
            admin_service.delete_taikhoan(u)
            self.load_tk()

    # ================= CÁC TAB KHÁC (GIỮ NGUYÊN LOGIC NHƯNG FIX THAM SỐ) =================

    def ui_sinhvien(self):
        # ===== TITLE =====
        tk.Label(self.tab_students, text="QUẢN LÝ SINH VIÊN",
                 font=("Arial", 14, "bold")).pack(pady=5)

        # ===== FORM =====
        frame = tk.LabelFrame(self.tab_students, text="Thông tin sinh viên")
        frame.pack(padx=10, pady=10, fill="x")

        for i in range(6):
            frame.columnconfigure(i, weight=1)

        pad_y = 4

        # ===== CỘT 1 =====
        tk.Label(frame, text="Mã SV").grid(row=0, column=0, sticky="w", padx=5, pady=pad_y)
        self.sv_masv = tk.Entry(frame)
        self.sv_masv.grid(row=0, column=1, sticky="ew", padx=5)

        tk.Label(frame, text="Họ tên").grid(row=1, column=0, sticky="w", padx=5, pady=pad_y)
        self.sv_name = tk.Entry(frame)
        self.sv_name.grid(row=1, column=1, sticky="ew", padx=5)

        tk.Label(frame, text="Giới tính").grid(row=2, column=0, sticky="w", padx=5, pady=pad_y)
        self.sv_gender = ttk.Combobox(frame, values=["Nam", "Nữ"], state="readonly")
        self.sv_gender.grid(row=2, column=1, sticky="ew", padx=5)

        # ===== CỘT 2 =====
        tk.Label(frame, text="Ngày sinh").grid(row=0, column=2, sticky="w", padx=5)
        self.sv_ngaysinh = tk.Entry(frame)
        self.sv_ngaysinh.grid(row=0, column=3, sticky="ew", padx=5)

        tk.Label(frame, text="SĐT").grid(row=1, column=2, sticky="w", padx=5)
        self.sv_sdt = tk.Entry(frame)
        self.sv_sdt.grid(row=1, column=3, sticky="ew", padx=5)

        tk.Label(frame, text="Địa chỉ").grid(row=2, column=2, sticky="w", padx=5)
        self.sv_diachi = tk.Entry(frame)
        self.sv_diachi.grid(row=2, column=3, sticky="ew", padx=5)

        # ===== CỘT 3 =====
        tk.Label(frame, text="Mã lớp").grid(row=0, column=4, sticky="w", padx=5)
        self.sv_lop = tk.Entry(frame)
        self.sv_lop.grid(row=0, column=5, sticky="ew", padx=5)

        tk.Label(frame, text="Năm thứ").grid(row=1, column=4, sticky="w", padx=5)
        self.sv_namthu = tk.Entry(frame)
        self.sv_namthu.grid(row=1, column=5, sticky="ew", padx=5)

        tk.Label(frame, text="Khóa học").grid(row=2, column=4, sticky="w", padx=5)
        self.sv_khoahoc = tk.Entry(frame)
        self.sv_khoahoc.grid(row=2, column=5, sticky="ew", padx=5)

        # ===== BUTTON =====
        btn_frame = tk.Frame(self.tab_students)
        btn_frame.pack(pady=8)

        tk.Button(btn_frame, text="Thêm", width=10, bg="#4CAF50", fg="white",
                  command=self.add_sv).pack(side=tk.LEFT, padx=6)

        tk.Button(btn_frame, text="Sửa", width=10, bg="#2196F3", fg="white",
                  command=self.update_sv).pack(side=tk.LEFT, padx=6)

        tk.Button(btn_frame, text="Xóa", width=10, bg="#f44336", fg="white",
                  command=self.delete_sv).pack(side=tk.LEFT, padx=6)

        tk.Button(btn_frame, text="Tải lại", width=10, bg="#FF9800", fg="white",
                  command=self.load_sv).pack(side=tk.LEFT, padx=6)

        # ===== SEARCH =====
        search_frame = tk.Frame(self.tab_students)
        search_frame.pack(pady=5)

        tk.Label(search_frame, text="Tìm kiếm:").pack(side=tk.LEFT)

        self.sv_search = tk.Entry(search_frame, width=30)
        self.sv_search.pack(side=tk.LEFT, padx=5)

        tk.Button(search_frame, text="Tìm",
                  bg="#9C27B0", fg="white",
                  command=self.search_sv).pack(side=tk.LEFT)

        # ===== TABLE =====
        table_frame = tk.Frame(self.tab_students)
        table_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

        cols = ("masv", "ten", "gt", "ns", "sdt", "dc", "nam", "khoa", "lop")

        self.tree_sv = ttk.Treeview(table_frame, columns=cols, show="headings")

        headers = ["MaSV", "Họ Tên", "Giới Tính", "Ngày Sinh",
                   "SDT", "Địa Chỉ", "Năm Thứ", "Khóa Học", "Mã Lớp"]

        for c, h in zip(cols, headers):
            self.tree_sv.heading(c, text=h)
            self.tree_sv.column(c, width=110, anchor="center")

        # ===== SCROLLBAR =====
        scroll = ttk.Scrollbar(table_frame, orient="vertical", command=self.tree_sv.yview)
        self.tree_sv.configure(yscroll=scroll.set)

        self.tree_sv.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scroll.pack(side=tk.RIGHT, fill=tk.Y)

        # ===== STYLE TABLE =====
        style = ttk.Style()
        style.configure("Treeview", rowheight=28)
        style.configure("Treeview.Heading", font=("Arial", 10, "bold"))

        self.tree_sv.bind("<<TreeviewSelect>>", self.on_select_sv)

        self.load_sv()

    def load_sv(self):
        self.tree_sv.delete(*self.tree_sv.get_children())

        try:
            data = admin_service.get_all_sinhvien()

            for row in data:
                self.tree_sv.insert("", "end", values=(
                    row[0],  # MaSV
                    row[1],  # HoTen
                    row[2],  # GioiTinh
                    row[3],  # NgaySinh
                    row[4],  # SDT
                    row[5],  # DiaChi
                    row[6],  # NamThu
                    row[7],  # KhoaHoc
                    row[8]  # MaLop
                ))
        except Exception as e:
            messagebox.showerror("Lỗi", str(e))

    def add_sv(self):
        try:
            data = (
                self.sv_masv.get(),
                self.sv_name.get(),
                self.sv_gender.get(),
                self.sv_ngaysinh.get(),
                self.sv_lop.get(),
                self.sv_sdt.get(),
                self.sv_diachi.get(),
                int(self.sv_namthu.get()),
                self.sv_khoahoc.get()
            )

            if admin_service.add_sinhvien(data):
                messagebox.showinfo("OK", "Thêm sinh viên thành công")
                self.load_sv()

        except Exception as e:
            messagebox.showerror("Lỗi", str(e))

    def update_sv(self):
        masv = self.sv_masv.get().strip()

        if not masv:
            messagebox.showwarning("Lỗi", "Chọn sinh viên cần sửa")
            return

        data = (
            masv,
            self.sv_name.get(),
            self.sv_gender.get(),
            self.sv_ngaysinh.get(),
            self.sv_lop.get(),
            self.sv_sdt.get(),
            self.sv_diachi.get(),
            int(self.sv_namthu.get()),
            self.sv_khoahoc.get()
        )

        try:
            if admin_service.update_sinhvien(data):
                messagebox.showinfo("OK", "Sửa thành công")
                self.load_sv()
        except Exception as e:
            messagebox.showerror("Lỗi", str(e))

    def delete_sv(self):
        sel = self.tree_sv.selection()

        if not sel:
            messagebox.showwarning("Lỗi", "Chọn sinh viên")
            return

        masv = self.tree_sv.item(sel[0])['values'][0]

        if messagebox.askyesno("Xóa", f"Xóa sinh viên {masv}?"):
            try:
                if admin_service.delete_sinhvien(masv):
                    self.load_sv()
            except Exception as e:
                messagebox.showerror("Lỗi", str(e))

    def search_sv(self):
        keyword = self.sv_search.get().lower().strip()

        self.tree_sv.delete(*self.tree_sv.get_children())

        try:
            data = admin_service.get_all_sinhvien()

            for r in data:
                if keyword in r[0].lower() or keyword in r[1].lower():
                    self.tree_sv.insert("", tk.END, values=(
                        r[0], r[1], r[2], r[3],
                        r[4], r[5], r[6], r[7], r[8]
                    ))
        except Exception as e:
            messagebox.showerror("Lỗi", str(e))

    def on_select_sv(self, event):
        sel = self.tree_sv.selection()

        if sel:
            v = self.tree_sv.item(sel[0])['values']

            self.sv_masv.delete(0, tk.END)
            self.sv_masv.insert(0, v[0])

            self.sv_name.delete(0, tk.END)
            self.sv_name.insert(0, v[1])

            self.sv_gender.set(v[2])

            self.sv_ngaysinh.delete(0, tk.END)
            self.sv_ngaysinh.insert(0, v[3])

            self.sv_lop.delete(0, tk.END)
            self.sv_lop.insert(0, v[4])

            self.sv_sdt.delete(0, tk.END)
            self.sv_sdt.insert(0, v[5])

            self.sv_namthu.delete(0, tk.END)
            self.sv_namthu.insert(0, v[6])

    def ui_giangvien(self):
        tk.Label(self.tab_teachers, text="QUẢN LÝ GIẢNG VIÊN",
                 font=("Arial", 14, "bold")).pack(pady=5)

        frame = tk.LabelFrame(self.tab_teachers, text="Thông tin giảng viên")
        frame.pack(padx=10, pady=10, fill="x")

        # ===== INPUT =====
        tk.Label(frame, text="Mã GV").grid(row=0, column=0, padx=5, pady=5)
        self.gv_magv = tk.Entry(frame)
        self.gv_magv.grid(row=0, column=1, padx=5)

        tk.Label(frame, text="Họ tên").grid(row=1, column=0, padx=5)
        self.gv_name = tk.Entry(frame)
        self.gv_name.grid(row=1, column=1, padx=5)

        tk.Label(frame, text="Giới tính").grid(row=2, column=0, padx=5)
        self.gv_gender = ttk.Combobox(frame, values=["Nam", "Nữ"], state="readonly")
        self.gv_gender.grid(row=2, column=1, padx=5)

        tk.Label(frame, text="Địa chỉ").grid(row=0, column=2, padx=5)
        self.gv_diachi = tk.Entry(frame)
        self.gv_diachi.grid(row=0, column=3, padx=5)

        tk.Label(frame, text="Email").grid(row=1, column=2, padx=5)
        self.gv_email = tk.Entry(frame)
        self.gv_email.grid(row=1, column=3, padx=5)

        tk.Label(frame, text="Mã khoa").grid(row=2, column=2, padx=5)
        self.gv_khoa = tk.Entry(frame)
        self.gv_khoa.grid(row=2, column=3, padx=5)

        # ===== SEARCH =====
        search_frame = tk.Frame(self.tab_teachers)
        search_frame.pack(pady=5)

        tk.Label(search_frame, text="Tìm kiếm:").pack(side=tk.LEFT)

        self.gv_search = tk.Entry(search_frame, width=30)
        self.gv_search.pack(side=tk.LEFT, padx=5)

        tk.Button(search_frame, text="Tìm",
                  bg="#9C27B0", fg="white",
                  command=self.search_gv).pack(side=tk.LEFT)

        # ===== BUTTON =====
        btn = tk.Frame(self.tab_teachers)
        btn.pack(pady=8)

        tk.Button(btn, text="Thêm", bg="#4CAF50", fg="white",
                  command=self.add_gv).pack(side=tk.LEFT, padx=5)

        tk.Button(btn, text="Sửa", bg="#2196F3", fg="white",
                  command=self.update_gv).pack(side=tk.LEFT, padx=5)

        tk.Button(btn, text="Xóa", bg="#f44336", fg="white",
                  command=self.delete_gv).pack(side=tk.LEFT, padx=5)

        tk.Button(btn, text="Tải lại", bg="#FF9800", fg="white",
                  command=self.load_gv).pack(side=tk.LEFT, padx=5)

        # ===== TABLE =====
        cols = ("magv", "ten", "gt", "email", "dc", "khoa")
        self.tree_gv = ttk.Treeview(self.tab_teachers, columns=cols, show="headings")

        headers = ["MaGV", "Họ Tên", "Giới Tính", "Email", "Địa Chỉ", "Mã Khoa"]

        for c, h in zip(cols, headers):
            self.tree_gv.heading(c, text=h)
            self.tree_gv.column(c, width=150, anchor="center")

        self.tree_gv.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

        self.tree_gv.bind("<<TreeviewSelect>>", self.on_select_gv)

        self.load_gv()

    def load_gv(self):
        self.tree_gv.delete(*self.tree_gv.get_children())

        try:
            data = admin_service.get_all_giangvien()

            for r in data:
                self.tree_gv.insert("", tk.END, values=(
                    r[0],  # MaGV
                    r[1],  # HoTen
                    r[2],  # GioiTinh
                    r[3],  # Email
                    r[4],  # DiaChi
                    r[5]  # MaKhoa
                ))
        except Exception as e:
            messagebox.showerror("Lỗi", str(e))

    def add_gv(self):
        data = (
            self.gv_magv.get(),
            self.gv_name.get(),
            self.gv_gender.get(),
            self.gv_diachi.get(),
            self.gv_email.get(),
            self.gv_khoa.get()
        )

        try:
            if admin_service.add_giangvien(data):
                messagebox.showinfo("OK", "Thêm giảng viên thành công")
                self.load_gv()
        except Exception as e:
            messagebox.showerror("Lỗi", str(e))

    def update_gv(self):
        data = (
            self.gv_magv.get(),
            self.gv_name.get(),
            self.gv_gender.get(),
            self.gv_diachi.get(),
            self.gv_email.get(),
            self.gv_khoa.get()
        )

        try:
            if admin_service.update_giangvien(data):
                messagebox.showinfo("OK", "Sửa thành công")
                self.load_gv()
        except Exception as e:
            messagebox.showerror("Lỗi", str(e))

    def delete_gv(self):
        sel = self.tree_gv.selection()

        if not sel:
            messagebox.showwarning("Lỗi", "Chọn giảng viên")
            return

        magv = self.tree_gv.item(sel[0])['values'][0]

        if messagebox.askyesno("Xóa", f"Xóa giảng viên {magv}?"):
            try:
                if admin_service.delete_giangvien(magv):
                    self.load_gv()
            except Exception as e:
                messagebox.showerror("Lỗi", str(e))

    def search_gv(self):
        keyword = self.gv_search.get().lower().strip()

        self.tree_gv.delete(*self.tree_gv.get_children())

        try:
            data = admin_service.get_all_giangvien()

            for r in data:
                if keyword in r[0].lower() or keyword in r[1].lower():
                    self.tree_gv.insert("", tk.END, values=(
                        r[0], r[1], r[2], r[3], r[4], r[5]
                    ))
        except Exception as e:
            messagebox.showerror("Lỗi", str(e))

    def on_select_gv(self, event):
        sel = self.tree_gv.selection()

        if sel:
            v = self.tree_gv.item(sel[0])['values']

            self.gv_magv.delete(0, tk.END)
            self.gv_magv.insert(0, v[0])

            self.gv_name.delete(0, tk.END)
            self.gv_name.insert(0, v[1])

            self.gv_gender.set(v[2])

            self.gv_email.delete(0, tk.END)
            self.gv_email.insert(0, v[3])

            self.gv_diachi.delete(0, tk.END)
            self.gv_diachi.insert(0, v[4])

            self.gv_khoa.delete(0, tk.END)
            self.gv_khoa.insert(0, v[5])

    def ui_phancong(self):
        tk.Label(self.tab_assign, text="PHÂN CÔNG GIẢNG DẠY",
                 font=("Arial", 14, "bold")).pack(pady=5)

        frame = tk.LabelFrame(self.tab_assign, text="Thông tin phân công")
        frame.pack(fill="x", padx=10, pady=10)

        # ===== INPUT =====
        tk.Label(frame, text="Mã GV").grid(row=0, column=0)
        self.pc_gv = tk.Entry(frame)
        self.pc_gv.grid(row=0, column=1)

        tk.Label(frame, text="Mã HP").grid(row=0, column=2)
        self.pc_hp = tk.Entry(frame)
        self.pc_hp.grid(row=0, column=3)

        tk.Label(frame, text="Mã lớp").grid(row=1, column=0)
        self.pc_lop = tk.Entry(frame)
        self.pc_lop.grid(row=1, column=1)

        tk.Label(frame, text="Học kỳ").grid(row=1, column=2)
        self.pc_hk = tk.Entry(frame)
        self.pc_hk.grid(row=1, column=3)

        tk.Label(frame, text="Năm học").grid(row=2, column=0)
        self.pc_nam = tk.Entry(frame)
        self.pc_nam.grid(row=2, column=1)

        # ===== BUTTON =====
        btn = tk.Frame(self.tab_assign)
        btn.pack(pady=5)

        tk.Button(btn, text="Thêm", bg="green", fg="white",
                  command=self.add_pc).pack(side=tk.LEFT, padx=5)

        tk.Button(btn, text="Xóa", bg="orange",
                  command=self.delete_pc).pack(side=tk.LEFT, padx=5)

        tk.Button(btn, text="Load",
                  command=self.load_pc).pack(side=tk.LEFT, padx=5)

        # ===== TABLE =====
        cols = ("gv", "hp", "lop", "hk", "nam")

        self.tree_pc = ttk.Treeview(self.tab_assign, columns=cols, show="headings")

        headers = ["Mã GV", "Mã HP", "Mã lớp", "HK", "Năm"]

        for c, h in zip(cols, headers):
            self.tree_pc.heading(c, text=h)
            self.tree_pc.column(c, width=120)

        self.tree_pc.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        self.tree_pc.bind("<<TreeviewSelect>>", self.on_select_pc)
        self.load_pc()

    def load_pc(self):
        self.tree_pc.delete(*self.tree_pc.get_children())

        try:
            data = admin_service.get_all_phancong()

            for r in data:
                self.tree_pc.insert("", tk.END, values=(
                    r[0],  # MaGV
                    r[1],  # MaHP
                    r[2],  # MaLop
                    r[3],  # HocKy
                    r[4]  # NamHoc
                ))

        except Exception as e:
            messagebox.showerror("Lỗi", str(e))

    def add_pc(self):
        try:
            if not all([
                self.pc_gv.get(),
                self.pc_hp.get(),
                self.pc_lop.get(),
                self.pc_hk.get(),
                self.pc_nam.get()
            ]):
                messagebox.showwarning("Thiếu", "Nhập đầy đủ thông tin")
                return

            data = (
                self.pc_gv.get(),
                self.pc_hp.get(),
                self.pc_lop.get(),
                int(self.pc_hk.get()),
                self.pc_nam.get()
            )

            admin_service.add_phancong(data)

            messagebox.showinfo("OK", "Đã phân công")
            self.load_pc()

        except Exception as e:
            messagebox.showerror("Lỗi", str(e))

    def delete_pc(self):
        sel = self.tree_pc.selection()
        if not sel:
            messagebox.showwarning("Thiếu", "Chọn dòng để xóa")
            return

        val = self.tree_pc.item(sel[0])["values"]

        admin_service.delete_phancong(
            val[0],  # MaGV
            val[1],  # MaHP
            val[2],  # MaLop
            val[3],  # HocKy
            val[4]  # NamHoc
        )

        messagebox.showinfo("OK", "Đã xóa")
        self.load_pc()

    def on_select_pc(self, event):
        sel = self.tree_pc.selection()
        if not sel:
            return

        val = self.tree_pc.item(sel[0])["values"]

        self.pc_gv.delete(0, tk.END)
        self.pc_gv.insert(0, val[0])

        self.pc_hp.delete(0, tk.END)
        self.pc_hp.insert(0, val[1])

        self.pc_lop.delete(0, tk.END)
        self.pc_lop.insert(0, val[2])

        self.pc_hk.delete(0, tk.END)
        self.pc_hk.insert(0, val[3])

        self.pc_nam.delete(0, tk.END)
        self.pc_nam.insert(0, val[4])

    def ui_hocphan(self):
        tk.Label(self.tab_courses, text="QUẢN LÝ HỌC PHẦN",
                 font=("Arial", 14, "bold")).pack(pady=5)

        frame = tk.LabelFrame(self.tab_courses, text="Thông tin học phần")
        frame.pack(padx=10, pady=10, fill="x")

        # ===== INPUT =====
        tk.Label(frame, text="Mã HP").grid(row=0, column=0, padx=5, pady=5)
        self.hp_ma = tk.Entry(frame)
        self.hp_ma.grid(row=0, column=1)

        tk.Label(frame, text="Tên HP").grid(row=1, column=0)
        self.hp_ten = tk.Entry(frame)
        self.hp_ten.grid(row=1, column=1)

        tk.Label(frame, text="Tín chỉ").grid(row=0, column=2)
        self.hp_tc = tk.Entry(frame)
        self.hp_tc.grid(row=0, column=3)

        tk.Label(frame, text="Mã khoa").grid(row=1, column=2)
        self.hp_khoa = tk.Entry(frame)
        self.hp_khoa.grid(row=1, column=3)

        # ===== BUTTON =====
        btn = tk.Frame(self.tab_courses)
        btn.pack(pady=8)

        tk.Button(btn, text="Thêm", bg="#4CAF50", fg="white",
                  command=self.add_hp).pack(side=tk.LEFT, padx=5)

        tk.Button(btn, text="Sửa", bg="#2196F3", fg="white",
                  command=self.update_hp).pack(side=tk.LEFT, padx=5)

        tk.Button(btn, text="Xóa", bg="#f44336", fg="white",
                  command=self.del_hp).pack(side=tk.LEFT, padx=5)

        tk.Button(btn, text="Tải lại", bg="#FF9800", fg="white",
                  command=self.load_hp).pack(side=tk.LEFT, padx=5)


        # ===== TABLE =====
        cols = ("ma", "ten", "tc", "khoa")
        self.tree_hp = ttk.Treeview(self.tab_courses, columns=cols, show="headings")

        headers = ["Mã HP", "Tên HP", "Tín chỉ", "Khoa"]

        for c, h in zip(cols, headers):
            self.tree_hp.heading(c, text=h)
            self.tree_hp.column(c, width=120, anchor="center")

        self.tree_hp.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

        self.tree_hp.bind("<<TreeviewSelect>>", self.on_select_hp)

        self.load_hp()

    def load_hp(self):
        self.tree_hp.delete(*self.tree_hp.get_children())
        data = admin_service.get_all_hocphan() or []
        for r in data:
            self.tree_hp.insert("", tk.END, values=(r[0], r[1], r[2], r[3]))

    def add_hp(self):
        ma = self.hp_ma.get().strip()
        ten = self.hp_ten.get().strip()
        tc = self.hp_tc.get().strip()
        khoa = self.hp_khoa.get().strip()

        if ma and ten and tc and khoa:
            if admin_service.add_hocphan((ma, ten, int(tc), khoa)):
                self.load_hp()
        else:
            messagebox.showwarning("Lỗi", "Nhập đầy đủ thông tin")

    def update_hp(self):
        ma = self.hp_ma.get().strip()
        ten = self.hp_ten.get().strip()
        tc = self.hp_tc.get().strip()
        khoa = self.hp_khoa.get().strip()

        if ma and ten and tc and khoa:
            admin_service.update_hocphan((ma, ten, int(tc), khoa))
            self.load_hp()

    def del_hp(self):
        ma = self.hp_ma.get().strip()
        if ma:
            admin_service.delete_hocphan(ma)
            self.load_hp()

    def on_select_hp(self, event):
        selected = self.tree_hp.focus()
        if selected:
            values = self.tree_hp.item(selected, "values")

            self.hp_ma.delete(0, tk.END)
            self.hp_ma.insert(0, values[0])

            self.hp_ten.delete(0, tk.END)
            self.hp_ten.insert(0, values[1])

            self.hp_tc.delete(0, tk.END)
            self.hp_tc.insert(0, values[2])

            self.hp_khoa.delete(0, tk.END)
            self.hp_khoa.insert(0, values[3])

    def ui_baocao(self):
        # ===== TITLE =====
        tk.Label(
            self.tab_report,
            text="BÁO CÁO SINH VIÊN",
            font=("Arial", 16, "bold"),
            fg="#2c3e50"
        ).pack(pady=10)

        # ===== FILTER =====
        filter_frame = tk.LabelFrame(
            self.tab_report,
            text="Bộ lọc tìm kiếm",
            font=("Arial", 10, "bold")
        )
        filter_frame.pack(fill="x", padx=15, pady=5)

        # Căn cột đẹp hơn
        filter_frame.columnconfigure(1, weight=1)
        filter_frame.columnconfigure(3, weight=1)

        tk.Label(filter_frame, text="Mã Lớp:").grid(row=0, column=0, padx=10, pady=8, sticky="w")
        self.rp_lop = tk.Entry(filter_frame)
        self.rp_lop.grid(row=0, column=1, padx=10, pady=8, sticky="ew")

        tk.Label(filter_frame, text="Khóa Học:").grid(row=0, column=2, padx=10, pady=8, sticky="w")
        self.rp_khoa = tk.Entry(filter_frame)
        self.rp_khoa.grid(row=0, column=3, padx=10, pady=8, sticky="ew")

        # ===== BUTTONS =====
        btn_frame = tk.Frame(self.tab_report)
        btn_frame.pack(pady=10)

        tk.Button(
            btn_frame,
            text="Tìm kiếm",
            bg="#3498db",
            fg="white",
            width=15,
            command=self.load_rp
        ).pack(side=tk.LEFT, padx=10)

        tk.Button(
            btn_frame,
            text="Xuất Excel",
            bg="#2ecc71",
            fg="white",
            width=15,
            command=self.export_excel
        ).pack(side=tk.LEFT, padx=10)

        tk.Button(
            btn_frame,
            text="Làm mới",
            bg="#f39c12",
            fg="white",
            width=15,
            command=lambda: [self.rp_lop.delete(0, tk.END),
                             self.rp_khoa.delete(0, tk.END),
                             self.load_rp()]
        ).pack(side=tk.LEFT, padx=10)

        tk.Button(
            btn_frame,
            text="Biểu đồ",
            bg="#9b59b6",
            fg="white",
            width=15,
            command=self.show_chart
        ).pack(side=tk.LEFT, padx=10)

        # ===== TABLE =====
        table_frame = tk.Frame(self.tab_report)
        table_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=5)

        cols = (
            "msv", "ten", "gt", "ns", "sdt",
            "dc", "nam", "khoa", "malop", "tenlop", "nganh"
        )

        headers = [
            "MaSV", "Họ Tên", "Giới Tính", "Ngày Sinh", "SĐT",
            "Địa Chỉ", "Năm Thứ", "Khóa Học", "Mã Lớp",
            "Tên Lớp", "Chuyên Ngành"
        ]

        self.tree_rp = ttk.Treeview(
            table_frame,
            columns=cols,
            show="headings"
        )

        # ===== STYLE =====
        style = ttk.Style()
        style.configure("Treeview", rowheight=28)
        style.configure("Treeview.Heading", font=("Arial", 10, "bold"))

        # ===== HEADERS =====
        for c, h in zip(cols, headers):
            self.tree_rp.heading(c, text=h)
            self.tree_rp.column(c, width=110, anchor="center")

        # ===== SCROLLBAR =====
        scroll_y = ttk.Scrollbar(
            table_frame,
            orient="vertical",
            command=self.tree_rp.yview
        )

        scroll_x = ttk.Scrollbar(
            table_frame,
            orient="horizontal",
            command=self.tree_rp.xview
        )

        self.tree_rp.configure(
            yscrollcommand=scroll_y.set,
            xscrollcommand=scroll_x.set
        )

        self.tree_rp.pack(side=tk.TOP, fill=tk.BOTH, expand=True)
        scroll_y.pack(side=tk.RIGHT, fill=tk.Y)
        scroll_x.pack(side=tk.BOTTOM, fill=tk.X)

        # ===== LOAD DATA AUTO =====
        self.load_rp()

    def load_rp(self):
        self.tree_rp.delete(*self.tree_rp.get_children())

        val_lop = self.rp_lop.get().strip()
        val_khoa = self.rp_khoa.get().strip()

        try:
            data = admin_service.get_baocao_loc(ma_lop=val_lop, ma_khoa=val_khoa)

            print("DATA:", data)

            if not data:
                messagebox.showwarning("Thông báo", "Không có dữ liệu!")
                return

            for r in data:
                self.tree_rp.insert("", tk.END, values=(
                    r[0], r[1], r[2], r[3],
                    r[4], r[5], r[6], r[7],
                    r[8], r[9], r[10]
                ))

        except Exception as e:
            messagebox.showerror("Lỗi", f"Lỗi khi tải dữ liệu: {e}")

    def export_excel(self):
        file = filedialog.asksaveasfilename(defaultextension=".xlsx")
        if not file:
            return

        wb = openpyxl.Workbook()
        ws = wb.active

        # header đúng 11 cột
        ws.append([
            "MaSV", "Họ Tên", "Giới Tính", "Ngày Sinh", "SDT",
            "Địa Chỉ", "Năm Thứ", "Khóa Học", "Mã Lớp",
            "Tên Lớp", "Chuyên Ngành"
        ])

        for row in self.tree_rp.get_children():
            ws.append(self.tree_rp.item(row)['values'])

        wb.save(file)
        messagebox.showinfo("OK", "Xuất Excel thành công!")

    def show_chart(self):
        from collections import Counter

        data = []

        # Lấy dữ liệu từ bảng
        for item in self.tree_rp.get_children():
            row = self.tree_rp.item(item)['values']
            if row:
                malop = row[8]  # cột MaLop
                if malop:
                    data.append(malop)

        if not data:
            messagebox.showwarning("Thông báo", "Không có dữ liệu để vẽ!")
            return

        # Đếm số lượng SV theo lớp
        counter = Counter(data)
        labels = list(counter.keys())
        values = list(counter.values())

        # ===== VẼ BIỂU ĐỒ =====
        fig, ax = plt.subplots(figsize=(6, 4))

        ax.bar(labels, values)
        ax.set_title("Số lượng sinh viên theo lớp")
        ax.set_xlabel("Mã lớp")
        ax.set_ylabel("Số lượng SV")

        # ===== HIỂN THỊ =====
        win = tk.Toplevel(self.root)
        win.title("Biểu đồ thống kê")

        canvas = FigureCanvasTkAgg(fig, master=win)
        canvas.draw()
        canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True)