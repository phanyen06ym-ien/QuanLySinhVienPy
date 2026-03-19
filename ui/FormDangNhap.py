import tkinter as tk
from tkinter import messagebox
from database.connect import get_connection
from ui.FormGiangVien import LecturerForm
from ui.FormSinhVien import StudentForm


class LoginForm:
    def __init__(self, root):
        self.root = root
        self.root.title("Đăng nhập")
        self.root.geometry("400x300")

        tk.Label(root, text="Quản Lý Sinh Viên", font=("Arial", 16, "bold")).pack(pady=20)

        frame = tk.Frame(root)
        frame.pack(pady=10)

        tk.Label(frame, text="Tài khoản:").grid(row=0, column=0)
        self.entry_user = tk.Entry(frame)
        self.entry_user.grid(row=0, column=1)

        tk.Label(frame, text="Mật khẩu:").grid(row=1, column=0)
        self.entry_pass = tk.Entry(frame, show="*")
        self.entry_pass.grid(row=1, column=1)

        tk.Button(root, text="Đăng nhập", command=self.dang_nhap).pack(pady=10)

    def dang_nhap(self):
        u = self.entry_user.get()
        p = self.entry_pass.get()

        conn = get_connection()
        if conn:
            cursor = conn.cursor()
            cursor.execute(
                "SELECT VaiTro, MaSV, MaGV FROM TAIKHOAN WHERE MaTK=? AND PasswordHash=?",
                (u, p)
            )
            row = cursor.fetchone()

            if row:
                vaitro, masv, magv = row
                self.root.withdraw()
                new_win = tk.Toplevel()

                if vaitro in ["GiangVien", "Admin"]:
                    LecturerForm(new_win, magv if magv else "ADMIN", self.root, vaitro)
                else:
                    StudentForm(new_win, masv, self.root)
            else:
                messagebox.showerror("Lỗi", "Sai tài khoản hoặc mật khẩu")

            conn.close()