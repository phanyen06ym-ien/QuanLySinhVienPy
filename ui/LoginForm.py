import tkinter as tk
from tkinter import messagebox

from ui.LecturerForm import LecturerForm
from ui.StudentForm import StudentForm
from ui.AdminForm import AdminForm

from services.AuthService import AuthService
from database.db import get_connection

class LoginForm:
    def __init__(self, root):
        self.root = root
        self.root.title("Hệ Thống Quản Lý Đào Tạo - Đăng Nhập")
        self.root.geometry("450x350")
        self.root.resizable(False, False)

        tk.Label(
            root,
            text="QUẢN LÝ SINH VIÊN",
            font=("Arial", 18, "bold"),
            fg="darkblue"
        ).pack(pady=25)

        frame = tk.Frame(root)
        frame.pack(pady=10, padx=20)

        # USERNAME
        tk.Label(frame, text="Tài khoản:", font=("Arial", 11)).grid(row=0, column=0, sticky="w", pady=8)
        self.entry_user = tk.Entry(frame, width=25, font=("Arial", 11))
        self.entry_user.grid(row=0, column=1, padx=10)
        self.entry_user.focus()

        # PASSWORD
        tk.Label(frame, text="Mật khẩu:", font=("Arial", 11)).grid(row=1, column=0, sticky="w", pady=8)
        self.entry_pass = tk.Entry(frame, width=25, font=("Arial", 11), show="*")
        self.entry_pass.grid(row=1, column=1, padx=10)

        # SHOW PASSWORD
        self.show_pass_var = tk.IntVar()
        tk.Checkbutton(
            root,
            text="Hiển thị mật khẩu",
            variable=self.show_pass_var,
            command=self.toggle_pass
        ).pack()

        # LOGIN BUTTON
        tk.Button(
            root,
            text="ĐĂNG NHẬP",
            bg="white",
            fg="black",
            bd=2,
            relief="raised",
            font=("Arial", 11, "bold"),
            width=20,
            command=self.handle_login
        ).pack(pady=15)

        # FORGOT PASSWORD
        tk.Button(
            root,
            text="Quên mật khẩu?",
            fg="blue",
            bd=0,
            cursor="hand2",
            command=self.open_forgot_pwd
        ).pack()

    # ================= HIỆN / ẨN PASSWORD =================
    def toggle_pass(self):
        if self.show_pass_var.get() == 1:
            self.entry_pass.config(show="")
        else:
            self.entry_pass.config(show="*")

    # ================= LOGIN =================
    def handle_login(self):
        username = self.entry_user.get().strip()
        password = self.entry_pass.get().strip()

        if not username or not password:
            messagebox.showwarning("Thông báo", "Vui lòng nhập đầy đủ tài khoản và mật khẩu!")
            return

        try:
            row = AuthService.login(username, password)

            if not row:
                messagebox.showerror("Thất bại", "Sai tài khoản hoặc mật khẩu!")
                return

            # LẤY ĐÚNG DATA TỪ spLogin
            tendangnhap, vaitro, masv, magv, hoten, makhoa = row
            vaitro = (vaitro or "").strip().upper()

            self.root.withdraw()

            new_win = tk.Toplevel()
            new_win.protocol("WM_DELETE_WINDOW", lambda: self.root.destroy())

            # PHÂN QUYỀN
            if vaitro == "GV":
                LecturerForm(new_win, magv, self.root, vaitro)

            elif vaitro == "ADMIN":
                AdminForm(new_win, tendangnhap, self.root)

            elif vaitro == "SV":
                StudentForm(new_win, masv, self.root)

            else:
                messagebox.showerror("Lỗi", "Vai trò không hợp lệ!")
                self.root.deiconify()

        except Exception as e:
            messagebox.showerror("Lỗi hệ thống", str(e))

    # ================= QUÊN MẬT KHẨU =================
    def open_forgot_pwd(self):
        forgot_win = tk.Toplevel(self.root)
        forgot_win.title("Khôi phục mật khẩu")
        forgot_win.geometry("350x250")

        tk.Label(forgot_win, text="Tài khoản:").pack(pady=5)
        en_u = tk.Entry(forgot_win)
        en_u.pack()

        tk.Label(forgot_win, text="Mật khẩu mới:").pack(pady=5)
        en_p1 = tk.Entry(forgot_win, show="*")
        en_p1.pack()

        tk.Label(forgot_win, text="Xác nhận lại:").pack(pady=5)
        en_p2 = tk.Entry(forgot_win, show="*")
        en_p2.pack()

        def confirm_change():
            u = en_u.get().strip()
            p1 = en_p1.get().strip()
            p2 = en_p2.get().strip()

            if not u or not p1:
                messagebox.showerror("Lỗi", "Nhập đầy đủ thông tin!")
                return

            if p1 != p2:
                messagebox.showerror("Lỗi", "Mật khẩu không khớp!")
                return

            try:
                ok = AuthService.update_password(u, p1)

                if not ok:
                    messagebox.showerror("Lỗi", "Tài khoản không tồn tại!")
                    return

                messagebox.showinfo("Thành công", "Đã đổi mật khẩu!")
                forgot_win.destroy()

            except Exception as e:
                messagebox.showerror("Lỗi", str(e))

        tk.Button(
            forgot_win,
            text="Xác nhận",
            bg="white",
            fg="black",
            bd=2,
            command=confirm_change
        ).pack(pady=15)


# ================= RUN =================
if __name__ == "__main__":
    root = tk.Tk()
    app = LoginForm(root)
    root.mainloop()