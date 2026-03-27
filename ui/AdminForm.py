import tkinter as tk
from tkinter import ttk, messagebox, filedialog
from database.connect import get_connection
import openpyxl
from openpyxl.styles import Font, PatternFill, Alignment
from datetime import datetime
from services.admin_service import *
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import re

class AdminForm:
    def __init__(self, root, ma_admin, login_win):
        self.root, self.login_win, self.ma_id = root, login_win, ma_admin
        self.root.title(f"Hệ Thống Quản Trị - Admin: {ma_admin}")
        self.root.geometry("1200x700")

        tk.Button(self.root, text="Đăng xuất", bg="red", fg="white",
                  command=self.dang_xuat).pack(anchor="ne", padx=10, pady=5)

        self.tabs = ttk.Notebook(self.root)
        self.tabs.pack(fill=tk.BOTH, expand=True)

        # Tabs
        self.tab_users = tk.Frame(self.tabs)
        self.tab_students = tk.Frame(self.tabs)
        self.tab_teachers = tk.Frame(self.tabs)
        self.tab_courses = tk.Frame(self.tabs)
        self.tab_report = tk.Frame(self.tabs)

        self.tabs.add(self.tab_users, text="Quản lý Tài khoản")
        self.tabs.add(self.tab_students, text="Quản lý Sinh viên")
        self.tabs.add(self.tab_teachers, text="Quản lý Giảng viên")
        self.tabs.add(self.tab_courses, text="Học phần")
        self.tabs.add(self.tab_report, text="Báo cáo")

        self.ui_taikhoan()
        self.ui_sinhvien()
        self.ui_giangvien()
        self.ui_hocphan()
        self.ui_baocao()

    def dang_xuat(self):
        self.root.destroy()
        self.login_win.deiconify()

# ====================== TÀI KHOẢN ======================
    def ui_taikhoan(self):
        f = tk.Frame(self.tab_users)
        f.pack(pady=10)

        tk.Label(f, text="Username").grid(row=0, column=0, padx=5)
        self.tk_user = tk.Entry(f)
        self.tk_user.grid(row=0, column=1, padx=5)

        tk.Label(f, text="Vai trò").grid(row=0, column=2, padx=5)
        self.tk_role = ttk.Combobox(f, values=["SV", "GV", "ADMIN"])
        self.tk_role.grid(row=0, column=3, padx=5)
        self.tk_role.current(0)

        # Nút bấm
        btn_f = tk.Frame(self.tab_users)
        btn_f.pack(pady=5)
        tk.Button(btn_f, text="Thêm", command=self.add_tk, bg="green", fg="white", width=10).pack(side=tk.LEFT, padx=5)
        tk.Button(btn_f, text="Xóa", command=self.del_tk, bg="orange", width=10).pack(side=tk.LEFT, padx=5)
        tk.Button(btn_f, text="Load", command=self.load_tk, bg="blue", fg="white", width=10).pack(side=tk.LEFT, padx=5)

        # Bảng hiển thị
        self.tree_tk = ttk.Treeview(self.tab_users, columns=("u", "p", "r"), show="headings")
        self.tree_tk.heading("u", text="User")
        self.tree_tk.heading("p", text="Pass")
        self.tree_tk.heading("r", text="Role")

        for col in ("u", "p", "r"):
            self.tree_tk.column(col, anchor="center")

        self.tree_tk.pack(fill=tk.BOTH, expand=True, padx=10)
        self.load_tk()

    def add_tk(self):
        username = self.tk_user.get().strip()
        role = self.tk_role.get()
        if not username:
            messagebox.showwarning("Thiếu tin", "Vui lòng nhập Username!")
            return
        if add_taikhoan(username, "123456", role):
            messagebox.showinfo("OK", f"Đã thêm tài khoản {username}")
            self.load_tk()
        else:
            messagebox.showerror("Lỗi", "Không thêm được tài khoản")

    def del_tk(self):
        sel = self.tree_tk.selection()
        if not sel: return
        username = self.tree_tk.item(sel[0])['values'][0]
        if delete_taikhoan(username):
            self.load_tk()

    def load_tk(self):
        self.tree_tk.delete(*self.tree_tk.get_children())
        rows = get_all_taikhoan()
        for r in rows:
            clean_row = [str(item) for item in r]
            self.tree_tk.insert("", tk.END, values=clean_row)

# ====================== SINH VIÊN ======================
    def ui_sinhvien(self):
        frame = tk.Frame(self.tab_students)
        frame.pack(pady=10)
        labels = ["MaSV", "HoTen", "GioiTinh", "NgaySinh", "SDT", "DiaChi", "MaLop", "NamThu", "KhoaHoc"]
        self.sv_entries = {}
        for i, text in enumerate(labels):
            tk.Label(frame, text=text).grid(row=i // 3, column=(i % 3) * 2)
            ent = tk.Entry(frame, width=18)
            ent.grid(row=i // 3, column=(i % 3) * 2 + 1, padx=5, pady=3)
            self.sv_entries[text] = ent

        btn_frame = tk.Frame(self.tab_students)
        btn_frame.pack()
        tk.Button(btn_frame, text="Thêm", bg="green", fg="white", command=self.add_sv).pack(side=tk.LEFT, padx=5)
        tk.Button(btn_frame, text="Sửa", bg="blue", fg="white", command=self.update_sv).pack(side=tk.LEFT, padx=5)
        tk.Button(btn_frame, text="Xóa", bg="orange", command=self.delete_sv).pack(side=tk.LEFT, padx=5)
        tk.Button(btn_frame, text="Làm mới", command=self.load_sv).pack(side=tk.LEFT, padx=5)

        cols = ("masv", "hoten", "gt", "ns", "sdt", "dc", "lop", "nam", "khoa")
        self.tree_sv = ttk.Treeview(self.tab_students, columns=cols, show="headings")
        headers = ["Mã SV", "Họ Tên", "Giới tính", "Ngày sinh", "SĐT", "Địa chỉ", "Mã lớp", "Năm", "Khóa"]
        for col, h in zip(cols, headers):
            self.tree_sv.heading(col, text=h)
            self.tree_sv.column(col, width=120, anchor="center")
        self.tree_sv.pack(fill=tk.BOTH, expand=True)
        self.tree_sv.bind("<<TreeviewSelect>>", self.on_sv_select)
        self.load_sv()

    def load_sv(self):
        self.tree_sv.delete(*self.tree_sv.get_children())
        rows = get_all_sinhvien()
        for row in rows:
            clean_row = []
            for item in row:
                if isinstance(item, datetime):
                    clean_row.append(item.strftime('%Y-%m-%d'))
                elif item is None:
                    clean_row.append("")
                else:
                    clean_row.append(str(item))
            self.tree_sv.insert("", tk.END, values=clean_row)

    def on_sv_select(self, event):
        sel = self.tree_sv.selection()
        if not sel: return
        values = self.tree_sv.item(sel[0])['values']
        keys = ["MaSV", "HoTen", "GioiTinh", "NgaySinh", "SDT", "DiaChi", "MaLop", "NamThu", "KhoaHoc"]
        for k, v in zip(keys, values):
            self.sv_entries[k].delete(0, tk.END)
            self.sv_entries[k].insert(0, str(v) if v else "")

    def add_sv(self):
        data = [
            self.sv_entries["MaSV"].get(),
            self.sv_entries["HoTen"].get(),
            self.sv_entries["GioiTinh"].get(),
            self.sv_entries["NgaySinh"].get(),
            self.sv_entries["MaLop"].get(),
            self.sv_entries["SDT"].get(),
            self.sv_entries["DiaChi"].get(),
            self.sv_entries["NamThu"].get(),
            self.sv_entries["KhoaHoc"].get()
        ]

        result = add_sinhvien(data)

        if result == True:
            messagebox.showinfo("OK", "Thêm thành công")
            self.load_sv()
        else:
            messagebox.showerror("Lỗi SQL", result)

    def update_sv(self):
        data = (
            self.sv_entries["HoTen"].get(),
            self.sv_entries["GioiTinh"].get(),
            self.sv_entries["NgaySinh"].get(),
            self.sv_entries["SDT"].get(),
            self.sv_entries["DiaChi"].get(),
            self.sv_entries["MaLop"].get(),
            self.sv_entries["NamThu"].get(),
            self.sv_entries["KhoaHoc"].get(),
            self.sv_entries["MaSV"].get()
        )

        result = update_sinhvien(data)

        if result == True:
            messagebox.showinfo("OK", "Cập nhật thành công")
            self.load_sv()
        else:
            messagebox.showerror("Lỗi SQL", result)


    def delete_sv(self):
        masv = self.sv_entries["MaSV"].get()
        if delete_sinhvien(masv):
            messagebox.showinfo("OK", "Đã xóa")
            self.load_sv()
   #giảng viên
    def ui_giangvien(self):
        # ===== FRAME CHA =====
        main_frame = tk.Frame(self.tab_teachers)
        main_frame.pack(fill="both", expand=True, padx=10, pady=5)

        left_frame = tk.Frame(main_frame)
        left_frame.pack(side="left", fill="both", expand=True, padx=5)

        right_frame = tk.Frame(main_frame)
        right_frame.pack(side="left", fill="both", expand=True, padx=5)

        # ===== FORM GIẢNG VIÊN =====
        form_frame = tk.LabelFrame(left_frame, text="Thông tin giảng viên")
        form_frame.pack(fill="x", pady=5)

        tk.Label(form_frame, text="Mã GV").grid(row=0, column=0, padx=5, pady=2)
        self.gv_magv = tk.Entry(form_frame)
        self.gv_magv.grid(row=0, column=1, padx=5)

        tk.Label(form_frame, text="Họ tên").grid(row=0, column=2)
        self.gv_hoten = tk.Entry(form_frame)
        self.gv_hoten.grid(row=0, column=3, padx=5)

        tk.Label(form_frame, text="Giới tính").grid(row=1, column=0)
        self.gv_gt = ttk.Combobox(form_frame, values=["Nam", "Nữ"])
        self.gv_gt.grid(row=1, column=1)
        self.gv_gt.current(0)

        tk.Label(form_frame, text="Địa chỉ").grid(row=1, column=2)
        self.gv_dc = tk.Entry(form_frame)
        self.gv_dc.grid(row=1, column=3)

        tk.Label(form_frame, text="Email").grid(row=2, column=0)
        self.gv_email = tk.Entry(form_frame)
        self.gv_email.grid(row=2, column=1)

        tk.Label(form_frame, text="Mã khoa").grid(row=2, column=2)
        self.gv_khoa = tk.Entry(form_frame)
        self.gv_khoa.grid(row=2, column=3)

        # ===== BUTTON =====
        btn_frame = tk.Frame(left_frame)
        btn_frame.pack(pady=5)

        tk.Button(btn_frame, text="Thêm", bg="green", fg="white",
                  command=self.add_gv).pack(side=tk.LEFT, padx=5)

        tk.Button(btn_frame, text="Sửa", bg="blue", fg="white",
                  command=self.update_gv).pack(side=tk.LEFT, padx=5)

        tk.Button(btn_frame, text="Xóa", bg="orange",
                  command=self.delete_gv).pack(side=tk.LEFT, padx=5)

        tk.Button(btn_frame, text="Làm mới",
                  command=self.load_gv).pack(side=tk.LEFT, padx=5)

        # ===== BẢNG GIẢNG VIÊN =====
        cols = ("magv", "hoten", "gt", "dc", "email", "khoa")
        self.tree_gv = ttk.Treeview(left_frame, columns=cols, show="headings")

        headers = ["Mã GV", "Họ Tên", "Giới tính", "Địa chỉ", "Email", "Mã Khoa"]
        for c, h in zip(cols, headers):
            self.tree_gv.heading(c, text=h)
            self.tree_gv.column(c, width=120, anchor="center")

        self.tree_gv.pack(fill=tk.BOTH, expand=True, pady=5)

        # ===== PHÂN CÔNG =====
        pc_frame = tk.LabelFrame(right_frame, text="Phân công giảng dạy")
        pc_frame.pack(fill="x", pady=5)

        tk.Label(pc_frame, text="Mã HP").grid(row=0, column=0)
        self.pc_mahp = ttk.Combobox(pc_frame, width=15)
        self.pc_mahp.grid(row=0, column=1)

        tk.Label(pc_frame, text="Mã lớp").grid(row=0, column=2)
        self.pc_malop = ttk.Combobox(pc_frame, width=15)
        self.pc_malop.grid(row=0, column=3)

        tk.Label(pc_frame, text="Học kỳ").grid(row=1, column=0)
        self.pc_hocky = tk.Entry(pc_frame)
        self.pc_hocky.grid(row=1, column=1)

        tk.Label(pc_frame, text="Năm học").grid(row=1, column=2)
        self.pc_namhoc = tk.Entry(pc_frame)
        self.pc_namhoc.grid(row=1, column=3)

        tk.Label(pc_frame, text="Phòng").grid(row=2, column=0)
        self.pc_phong = tk.Entry(pc_frame)
        self.pc_phong.grid(row=2, column=1)

        tk.Button(pc_frame, text="Phân công", bg="green", fg="white",
                  command=self.add_pc).grid(row=3, column=1)

        tk.Button(pc_frame, text="Xóa PC", bg="red", fg="white",
                  command=self.delete_pc).grid(row=3, column=2)

        # ===== BẢNG PHÂN CÔNG =====
        cols = ("mahp", "tenhp", "lop", "hk", "nam", "phong")
        self.tree_pc = ttk.Treeview(right_frame, columns=cols, show="headings")

        headers = ["Mã HP", "Tên HP", "Lớp", "Học kỳ", "Năm", "Phòng"]
        for c, h in zip(cols, headers):
            self.tree_pc.heading(c, text=h)
            self.tree_pc.column(c, width=120, anchor="center")

        self.tree_pc.pack(fill=tk.BOTH, expand=True, pady=5)

        # ===== EVENT =====
        self.tree_gv.bind("<<TreeviewSelect>>", self.on_gv_select)

        # ===== LOAD DATA =====
        self.load_gv()
        self.load_combobox_data()


    def load_gv(self):
        self.tree_gv.delete(*self.tree_gv.get_children())
        rows = get_all_giangvien()
        for r in rows:
            # FIX LỖI HIỂN THỊ: Chuyển Tuple thành mảng các chuỗi sạch sẽ
            clean_row = [str(item) if item is not None else "" for item in r]
            self.tree_gv.insert("", tk.END, values=clean_row)

    def load_hp_lop(self):
        conn = get_connection()
        cursor = conn.cursor()

        # Học phần
        cursor.execute("SELECT MaHP FROM HOCPHAN")
        self.list_hp.delete(0, tk.END)
        for row in cursor.fetchall():
            self.list_hp.insert(tk.END, row[0])

        # Lớp
        cursor.execute("SELECT MaLop FROM LOPHOC")
        self.list_lop.delete(0, tk.END)
        for row in cursor.fetchall():
            self.list_lop.insert(tk.END, row[0])

        conn.close()

    def load_combobox_data(self):
        conn = get_connection()
        cursor = conn.cursor()

        cursor.execute("SELECT MaHP FROM HOCPHAN")
        self.pc_mahp['values'] = [r[0] for r in cursor.fetchall()]

        cursor.execute("SELECT MaLop FROM LOPHOC")
        self.pc_malop['values'] = [r[0] for r in cursor.fetchall()]

        conn.close()

    def on_gv_select(self, event):
        selected = self.tree_gv.selection()
        if not selected:
            return

        item = self.tree_gv.item(selected[0])
        r = item["values"]

        if not r:
            return

        # ===== ĐỔ DỮ LIỆU VÀO FORM =====
        self.gv_magv.delete(0, tk.END)
        self.gv_magv.insert(0, r[0])

        self.gv_hoten.delete(0, tk.END)
        self.gv_hoten.insert(0, r[1])

        self.gv_gt.set(r[2])

        self.gv_dc.delete(0, tk.END)
        self.gv_dc.insert(0, r[3])

        self.gv_email.delete(0, tk.END)
        self.gv_email.insert(0, r[4])

        self.gv_khoa.delete(0, tk.END)
        self.gv_khoa.insert(0, r[5])

        # ===== LOAD PHÂN CÔNG =====
        magv = r[0]
        print("Đang load phân công cho:", magv)  # debug

        self.load_pc_by_gv(magv)

    def load_pc_by_gv(self, magv):
        # Xóa bảng cũ
        self.tree_pc.delete(*self.tree_pc.get_children())

        # gọi service
        rows = get_pc_by_giangvien(magv)

        print("DATA SERVICE:", rows)  # debug

        # Đổ vào bảng
        for row in rows:
            clean_row = [str(item) if item is not None else "" for item in row]
            self.tree_pc.insert("", "end", values=clean_row)

    def get_selected_hp_lop(self):
        hp = [self.list_hp.get(i) for i in self.list_hp.curselection()]
        lop = [self.list_lop.get(i) for i in self.list_lop.curselection()]
        return hp, lop

    def is_valid_email(self, email):
        pattern = r'^[\w\.-]+@[\w\.-]+\.\w+$'
        return re.match(pattern, email)

    def add_gv(self):
        data = (
            self.gv_magv.get().strip(),
            self.gv_hoten.get().strip(),
            self.gv_gt.get(),
            self.gv_dc.get().strip(),
            self.gv_email.get().strip(),
            self.gv_khoa.get().strip()
        )

        if not data[0]:
            messagebox.showwarning("Lỗi", "Mã GV không được để trống")
            return

        if add_giangvien(data):
            messagebox.showinfo("OK", "Thêm giảng viên thành công")
            self.load_gv()
        else:
            messagebox.showerror("Lỗi", "Không thể thêm giảng viên")

    def update_gv(self):
        email = self.gv_email.get().strip()

        if not self.is_valid_email(email):
            messagebox.showerror("Lỗi", "Email không hợp lệ!")
            return

        data = (
            self.gv_hoten.get().strip(),
            self.gv_gt.get(),
            self.gv_dc.get().strip(),
            email,
            self.gv_khoa.get().strip(),
            self.gv_magv.get().strip()
        )

        if update_giangvien(data):
            messagebox.showinfo("OK", "Cập nhật thành công")
            self.load_gv()

    def delete_gv(self):
        magv = self.gv_magv.get().strip()
        if not magv: return
        if messagebox.askyesno("Xác nhận", f"Bạn có chắc muốn xóa giảng viên {magv}?"):
            if delete_giangvien(magv):
                messagebox.showinfo("OK", "Đã xóa giảng viên")
                self.load_gv()

    def add_pc(self):
        # Lấy dữ liệu từ các ô nhập liệu
        magv = self.gv_magv.get().strip()
        mahp = self.pc_mahp.get().strip()
        malop = self.pc_malop.get().strip()
        hocky = self.pc_hocky.get().strip()
        namhoc = self.pc_namhoc.get().strip()
        phong = self.pc_phong.get().strip()

        # 1. Kiểm tra không được để trống các trường quan trọng
        if not (magv and mahp and malop and hocky and namhoc):
            messagebox.showwarning("Thông báo", "Vui lòng nhập đầy đủ: Mã GV, Mã HP, Lớp, Học kỳ và Năm học!")
            return

        data = (magv, mahp, malop, hocky, namhoc, phong)

        # 2. Gọi service để thực thi lệnh INSERT vào SQL
        if add_phancong(data):
            messagebox.showinfo("Thành công", f"Đã phân công môn {mahp} cho giảng viên {magv}")
            # Load lại bảng hiển thị để cập nhật dữ liệu mới
            if hasattr(self, 'load_pc_by_gv'):
                self.load_pc_by_gv(magv)
        else:
            messagebox.showerror("Lỗi",
                                 "Không thể phân công. Vui lòng kiểm tra lại Mã HP hoặc Mã Lớp có tồn tại không!")

    def delete_pc(self):
        selected = self.tree_pc.selection()
        if not selected:
            return

        row = self.tree_pc.item(selected[0])['values']

        magv = self.gv_magv.get()
        mahp = row[0]
        malop = row[2]
        hocky = row[3]
        namhoc = row[4]

        if delete_phancong(magv, mahp, malop, hocky, namhoc):
            messagebox.showinfo("OK", "Đã xóa phân công")
            self.load_pc_by_gv(magv)

# ====================== HỌC PHẦN ======================
    def ui_hocphan(self):
        # Khung nhập liệu
        frame = tk.Frame(self.tab_courses)
        frame.pack(pady=10)

        tk.Label(frame, text="Mã HP").grid(row=0, column=0, padx=5)
        self.hp_ma = tk.Entry(frame, width=15)
        self.hp_ma.grid(row=0, column=1, padx=5)

        tk.Label(frame, text="Tên HP").grid(row=0, column=2, padx=5)
        self.hp_ten = tk.Entry(frame, width=25)
        self.hp_ten.grid(row=0, column=3, padx=5)

        tk.Label(frame, text="Số tín chỉ").grid(row=0, column=4, padx=5)
        self.hp_tin = tk.Entry(frame, width=10)
        self.hp_tin.grid(row=0, column=5, padx=5)

        # Khung nút bấm
        btn_frame = tk.Frame(self.tab_courses)
        btn_frame.pack(pady=5)

        tk.Button(btn_frame, text="Thêm", bg="green", fg="white", width=10,
                  command=self.add_hp).pack(side=tk.LEFT, padx=5)
        tk.Button(btn_frame, text="Xóa", bg="orange", width=10,
                  command=self.del_hp).pack(side=tk.LEFT, padx=5)
        tk.Button(btn_frame, text="Làm mới", bg="blue", fg="white", width=10,
                  command=self.load_hp).pack(side=tk.LEFT, padx=5)

        # Bảng hiển thị
        cols = ("ma", "ten", "tin")
        self.tree_hp = ttk.Treeview(self.tab_courses, columns=cols, show="headings")
        self.tree_hp.heading("ma", text="Mã Học Phần")
        self.tree_hp.heading("ten", text="Tên Học Phần")
        self.tree_hp.heading("tin", text="Số Tín Chỉ")

        for c in cols:
            self.tree_hp.column(c, anchor="center", width=200)

        self.tree_hp.pack(fill=tk.BOTH, expand=True, padx=10, pady=5)
        self.tree_hp.bind("<<TreeviewSelect>>", self.on_hp_select)
        self.load_hp()

    def load_hp(self):
        self.tree_hp.delete(*self.tree_hp.get_children())
        rows = get_all_hocphan()
        for r in rows:
            # FIX LỖI NGOẶC ĐƠN: Chuyển dữ liệu sang dạng chuỗi sạch
            clean_row = [str(item) for item in r]
            self.tree_hp.insert("", tk.END, values=clean_row)

    def on_hp_select(self, event):
        sel = self.tree_hp.selection()
        if not sel: return
        v = self.tree_hp.item(sel[0])['values']
        self.hp_ma.delete(0, tk.END);
        self.hp_ma.insert(0, v[0])
        self.hp_ten.delete(0, tk.END);
        self.hp_ten.insert(0, v[1])
        self.hp_tin.delete(0, tk.END);
        self.hp_tin.insert(0, v[2])

    def add_hp(self):
        ma, ten, tin = self.hp_ma.get().strip(), self.hp_ten.get().strip(), self.hp_tin.get().strip()
        if not ma or not ten:
            messagebox.showwarning("Chú ý", "Vui lòng nhập đủ Mã và Tên HP")
            return
        if add_hocphan(ma, ten, tin):
            messagebox.showinfo("Thành công", f"Đã thêm học phần {ten}")
            self.load_hp()
        else:
            messagebox.showerror("Lỗi", "Không thể thêm học phần ")

    def del_hp(self):
        ma = self.hp_ma.get().strip()
        if not ma: return
        if messagebox.askyesno("Xác nhận", f"Bạn có muốn xóa học phần {ma}?"):
            if delete_hocphan(ma):
                messagebox.showinfo("Xong", "Đã xóa thành công")
                self.load_hp()

# ====================== BÁO CÁO ======================
    def ui_baocao(self):
        btn_frame = tk.Frame(self.tab_report)
        btn_frame.pack(pady=10)

        tk.Button(btn_frame, text="Tải dữ liệu", bg="#3498db", fg="white", command=self.load_rp).pack(side=tk.LEFT,
                                                                                                      padx=5)
        tk.Button(btn_frame, text="Xuất Excel", bg="#2ecc71", fg="white", command=self.export_excel).pack(side=tk.LEFT,
                                                                                                          padx=5)
        tk.Button(btn_frame, text="Xem biểu đồ điểm", bg="#9b59b6", fg="white", command=self.show_chart).pack(
            side=tk.LEFT, padx=5)

        cols = ("msv", "ten", "hp", "diem")
        self.tree_rp = ttk.Treeview(self.tab_report, columns=cols, show="headings")
        headers = ["Mã SV", "Họ Tên", "Học Phần", "Điểm TK"]

        for c, h in zip(cols, headers):
            self.tree_rp.heading(c, text=h)
            self.tree_rp.column(c, width=150, anchor="center")

        # FIX: Sửa từ tree_sv thành tree_rp
        self.tree_rp.pack(fill=tk.BOTH, expand=True, padx=10, pady=5)
        self.load_rp()

    def load_rp(self):
        self.tree_rp.delete(*self.tree_rp.get_children())
        for r in get_baocao():
            self.tree_rp.insert("", tk.END, values=r)

    def export_excel(self):
        wb=openpyxl.Workbook()
        ws=wb.active
        ws.append(["MaSV","Ten","HP","Diem"])
        for row in self.tree_rp.get_children():
            ws.append(self.tree_rp.item(row)['values'])
        path=f"baocao_{datetime.now().strftime('%H%M%S')}.xlsx"
        wb.save(path)
        messagebox.showinfo("OK",f"Đã lưu {path}")

    def load_rp(self):
        # Xóa dữ liệu cũ
        self.tree_rp.delete(*self.tree_rp.get_children())

        # Lấy dữ liệu từ service
        rows = get_baocao()

        if rows:
            for r in rows:
                # Fix lỗi hiển thị Tuple (dấu ngoặc đơn) và định dạng điểm số
                clean_row = []
                for i, item in enumerate(r):
                    if i == 3:  # Cột điểm
                        clean_row.append(f"{float(item):.1f}") if item is not None else clean_row.append("")
                    else:
                        clean_row.append(str(item) if item is not None else "")
                self.tree_rp.insert("", tk.END, values=clean_row)

    def export_excel(self):
        # Kiểm tra xem có dữ liệu để xuất không
        if not self.tree_rp.get_children():
            messagebox.showwarning("Chú ý", "Không có dữ liệu để xuất!")
            return

        filename = filedialog.asksaveasfilename(
            defaultextension=".xlsx",
            filetypes=[("Excel files", "*.xlsx")],
            title="Lưu báo cáo"
        )
        if not filename: return

        try:
            wb = openpyxl.Workbook()
            ws = wb.active
            ws.title = "Báo cáo điểm"

            # 1. Tạo tiêu đề cột và định dạng (In đậm, màu nền)
            headers = ["Mã SV", "Họ Tên", "Học Phần", "Điểm TK"]
            ws.append(headers)

            header_fill = PatternFill(start_color="3498db", end_color="3498db", fill_type="solid")
            header_font = Font(bold=True, color="FFFFFF")

            for cell in ws[1]:
                cell.fill = header_fill
                cell.font = header_font
                cell.alignment = Alignment(horizontal="center")

            # 2. Ghi dữ liệu từ bảng vào file
            for row_id in self.tree_rp.get_children():
                row_data = self.tree_rp.item(row_id)['values']
                # Chuyển cột điểm sang kiểu số để Excel hiểu
                ws.append([row_data[0], row_data[1], row_data[2], float(row_data[3])])

            # 3. Tự động chỉnh độ rộng cột
            for column_cells in ws.columns:
                length = max(len(str(cell.value)) for cell in column_cells)
                ws.column_dimensions[column_cells[0].column_letter].width = length + 2

            wb.save(filename)
            messagebox.showinfo("OK", f"Đã xuất file thành công:\n{filename}")
        except Exception as e:
            messagebox.showerror("Lỗi", f"Không thể lưu file: {e}")

    def show_chart(self):
        # 1. Lấy dữ liệu điểm từ Treeview
        items = self.tree_rp.get_children()
        if not items:
            messagebox.showwarning("Chú ý", "Tải dữ liệu trước khi xem biểu đồ!")
            return

        # Phân loại điểm
        categories = {'Xuất sắc (9-10)': 0, 'Giỏi (8-8.9)': 0, 'Khá (7-7.9)': 0, 'TB (5-6.9)': 0, 'Yếu (<5)': 0}

        for item_id in items:
            try:
                diem = float(self.tree_rp.item(item_id)['values'][3])
                if diem >= 9:
                    categories['Xuất sắc (9-10)'] += 1
                elif diem >= 8:
                    categories['Giỏi (8-8.9)'] += 1
                elif diem >= 7:
                    categories['Khá (7-7.9)'] += 1
                elif diem >= 5:
                    categories['TB (5-6.9)'] += 1
                else:
                    categories['Yếu (<5)'] += 1
            except:
                continue  # Bỏ qua nếu dữ liệu điểm lỗi

        # 2. Tạo cửa sổ mới để hiện biểu đồ
        chart_win = tk.Toplevel(self.root)
        chart_win.title("Biểu đồ phân bố điểm số")
        chart_win.geometry("800x600")

        # 3. Vẽ biểu đồ bằng Matplotlib
        fig, ax = plt.figure(figsize=(8, 6), dpi=100), plt.gca()

        names = list(categories.keys())
        values = list(categories.values())
        colors = ['#2ecc71', '#3498db', '#f1c40f', '#e67e22', '#e74c3c']  # Màu sắc cho từng loại

        bars = ax.bar(names, values, color=colors)

        # Định dạng biểu đồ
        ax.set_title('Tỷ lệ phân bố điểm tổng kết sinh viên', fontsize=14, fontweight='bold')
        ax.set_xlabel('Xếp loại', fontsize=12)
        ax.set_ylabel('Số lượng sinh viên', fontsize=12)
        ax.grid(axis='y', linestyle='--', alpha=0.7)

        # Hiển thị số liệu trên đầu mỗi cột
        for bar in bars:
            height = bar.get_height()
            ax.text(bar.get_x() + bar.get_width() / 2, height,
                    f'{int(height)}',
                    ha='center', va='bottom', fontweight='bold')

        # 4. Nhúng biểu đồ Matplotlib vào cửa sổ Tkinter
        canvas = FigureCanvasTkAgg(fig, master=chart_win)
        canvas.draw()
        canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True)