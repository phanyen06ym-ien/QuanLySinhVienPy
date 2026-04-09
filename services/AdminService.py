from database.db import Database

class AdminService:

    # ================= TÀI KHOẢN =================

    @staticmethod
    def get_all_taikhoan():
        db = Database()
        try:
            return db.fetchall("SELECT * FROM VIEW_TaiKhoan_FullInfo")
        finally:
            db.close()

    @staticmethod
    def add_taikhoan(username, password, role, masv=None, magv=None):
        db = Database()
        try:
            sql = "EXEC spThemTaiKhoan ?, ?, ?, ?, ?"
            return db.execute(sql, (username, password, role, masv, magv))
        finally:
            db.close()

    @staticmethod
    def delete_taikhoan(username):
        db = Database()
        try:
            sql = "EXEC spXoaTaiKhoan ?"
            return db.execute(sql, (username,))
        finally:
            db.close()

    # ================= SINH VIÊN =================

    @staticmethod
    def get_all_sinhvien():
        db = Database()
        try:
            sql = "SELECT * FROM VIEW_SinhVien_FullInfo"
            return db.fetchall(sql)
        finally:
            db.close()

    @staticmethod
    def add_sinhvien(data):
        db = Database()
        try:
            sql = "EXEC spThemSinhVien ?, ?, ?, ?, ?, ?, ?, ?, ?"
            return db.execute(sql, data)
        finally:
            db.close()

    @staticmethod
    def update_sinhvien(data):
        db = Database()
        try:
            sql = "EXEC spSuaSinhVien ?, ?, ?, ?, ?, ?, ?, ?, ?"
            return db.execute(sql, data)
        finally:
            db.close()

    @staticmethod
    def delete_sinhvien(masv):
        db = Database()
        try:
            sql = "EXEC spXoaSinhVien ?"
            return db.execute(sql, (masv,))
        finally:
            db.close()

    # ================= GIẢNG VIÊN =================

    @staticmethod
    def get_all_giangvien():
        db = Database()
        try:
            return db.fetchall("EXEC spXemGiangVien")
        finally:
            db.close()

    @staticmethod
    def add_giangvien(data):
        db = Database()
        try:
            sql = "EXEC spThemGiangVien ?, ?, ?, ?, ?, ?"
            return db.execute(sql, data)
        finally:
            db.close()

    @staticmethod
    def update_giangvien(data):
        db = Database()
        try:
            sql = "EXEC spSuaGiangVien ?, ?, ?, ?, ?, ?"
            return db.execute(sql, data)
        finally:
            db.close()

    @staticmethod
    def delete_giangvien(magv):
        db = Database()
        try:
            sql = "EXEC spXoaGiangVien ?"
            return db.execute(sql, (magv,))
        finally:
            db.close()

    # ================= PHÂN CÔNG =================

    @staticmethod
    def get_pc_by_giangvien(magv):
        db = Database()
        try:
            sql = "EXEC spXemPhanCongTheoGV ?"
            return db.fetchall(sql, (magv,))
        finally:
            db.close()

    @staticmethod
    def get_all_phancong():
        db = Database()
        try:
            return db.fetchall("SELECT * FROM PHANCONG")
        finally:
            db.close()

    @staticmethod
    def add_phancong(data):
        db = Database()
        try:
            sql = "EXEC spPhanCong ?, ?, ?, ?, ?"
            return db.execute(sql, data)
        finally:
            db.close()

    @staticmethod
    def delete_phancong(magv, mahp, malop, hocky, namhoc):
        db = Database()
        try:
            sql = """
                DELETE FROM PHANCONG
                WHERE MaGV=? AND MaHP=? AND MaLop=? AND HocKy=? AND NamHoc=?
            """
            return db.execute(sql, (magv, mahp, malop, hocky, namhoc))
        finally:
            db.close()

    # ================= HỌC PHẦN =================

    @staticmethod
    def get_all_hocphan():
        db = Database()
        try:
            return db.fetchall("EXEC spXemHocPhan")
        finally:
            db.close()

    @staticmethod
    def add_hocphan(data):
        db = Database()
        try:
            sql = "EXEC spThemHocPhan ?, ?, ?, ?"
            return db.execute(sql, data)
        finally:
            db.close()

    @staticmethod
    def update_hocphan(data):
        db = Database()
        try:
            sql = "EXEC spSuaHocPhan ?, ?, ?, ?"
            return db.execute(sql, data)
        finally:
            db.close()

    @staticmethod
    def delete_hocphan(ma_hp):
        db = Database()
        try:
            sql = "EXEC spXoaHocPhan ?"
            return db.execute(sql, (ma_hp,))
        finally:
            db.close()


    # ================= BÁO CÁO =================

    @staticmethod
    def get_baocao_loc(ma_lop=None, ma_khoa=None):
        db = Database()
        try:
            sql = "SELECT * FROM VIEW_BaoCaoSinhVien WHERE 1=1"
            params = []

            if ma_lop:
                sql += " AND MaLop LIKE ?"
                params.append(f"%{ma_lop}%")

            if ma_khoa:
                sql += " AND KhoaHoc LIKE ?"
                params.append(f"%{ma_khoa}%")

            return db.fetchall(sql, tuple(params))
        finally:
            db.close()


# ===== INSTANCE =====
admin_service = AdminService()