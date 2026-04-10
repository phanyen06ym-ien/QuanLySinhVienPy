from database.db import Database

class StudentService:

    # ================= THÔNG TIN =================
    @staticmethod
    def get_info(ma_sv):
        db = Database()
        try:
            sql = """
            SELECT * FROM VIEW_SinhVien_FullInfo
            WHERE MaSV = ?
            """
            return db.fetchone(sql, (ma_sv,))
        finally:
            db.close()


    # ================= ĐIỂM =================
    @staticmethod
    def get_grades(ma_sv):
        db = Database()
        try:
            sql = "EXEC spXemBangDiem ?"
            return db.fetchall(sql, (ma_sv,))
        finally:
            db.close()


    # ================= ĐĂNG KÝ =================
    @staticmethod
    def register_course(ma_sv, ma_hp, hk, nh):
        db = Database()
        try:
            sql = "EXEC spDangKyHoc ?, ?, ?, ?"
            return db.execute(sql, (ma_sv, ma_hp, hk, nh))
        finally:
            db.close()


    # ================= HỦY ĐĂNG KÝ =================
    @staticmethod
    def cancel_course(ma_sv, ma_hp, hk, nh):
        db = Database()
        try:
            sql = "EXEC spHuyDangKy ?, ?, ?, ?"
            return db.execute(sql, (ma_sv, ma_hp, hk, nh))
        finally:
            db.close()


    # ================= DANH SÁCH ĐÃ ĐĂNG KÝ =================
    @staticmethod
    def get_registered_courses(ma_sv):
        db = Database()
        try:
            sql = "EXEC spXemDangKyTheoSV ?"
            return db.fetchall(sql, (ma_sv,))
        finally:
            db.close()


    # ================= DANH SÁCH HỌC PHẦN =================
    @staticmethod
    def get_all_subjects():
        db = Database()
        try:
            sql = "EXEC spXemHocPhan"
            return db.fetchall(sql)
        finally:
            db.close()