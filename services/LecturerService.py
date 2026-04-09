from database.db import Database


class LecturerService:

    # ================= THÔNG TIN GIẢNG VIÊN =================
    @staticmethod
    def get_info(ma_gv):
        db = Database()
        try:
            sql = "SELECT * FROM VIEW_GiangVien_FullInfo WHERE MaGV=?"
            return db.fetchone(sql, (ma_gv,))
        finally:
            db.close()


    # ================= LỚP PHỤ TRÁCH =================
    @staticmethod
    def get_classes(ma_gv):
        db = Database()
        try:
            sql = """
            SELECT MaLop, TenLop, ChuyenNganh
            FROM LOPHOC
            WHERE CoVanHocTap = ?
            """
            return db.fetchall(sql, (ma_gv,))
        finally:
            db.close()


    # ================= HỌC PHẦN PHÂN CÔNG =================
    @staticmethod
    def get_subjects(ma_gv):
        db = Database()
        try:
            sql = "EXEC spXemPhanCongTheoGV ?"
            return db.fetchall(sql, (ma_gv,))
        finally:
            db.close()


    # ================= SINH VIÊN THEO LỚP =================
    @staticmethod
    def get_students_by_class(malop):
        db = Database()
        try:
            sql = "SELECT MaSV, HoTen FROM SINHVIEN WHERE MaLop=?"
            return db.fetchall(sql, (malop,))
        finally:
            db.close()


    # ================= LẤY DANH SÁCH ĐIỂM =================
    @staticmethod
    def get_grades(mahp, hk, nh):
        db = Database()
        try:
            sql = """
            SELECT *
            FROM VIEW_BangDiem_Full
            WHERE MaHP = ? AND HocKy = ? AND NamHoc = ?
            ORDER BY MaSV
            """
            return db.fetchall(sql, (mahp, hk, nh))
        finally:
            db.close()


    # ================= NHẬP ĐIỂM =================
    @staticmethod
    def insert_grade(data):
        db = Database()
        try:
            sql = "EXEC spNhapDiem ?, ?, ?, ?, ?, ?, ?, ?"
            return db.execute(sql, data)
        finally:
            db.close()


    # ================= SỬA ĐIỂM =================
    @staticmethod
    def update_grade(data):
        db = Database()
        try:
            sql = "EXEC spSuaDiem ?, ?, ?, ?, ?, ?, ?, ?"
            return db.execute(sql, data)
        finally:
            db.close()


    # ================= XÓA ĐIỂM =================
    @staticmethod
    def delete_grade(msv, mhp, hk, nh):
        db = Database()
        try:
            sql = """
            DELETE FROM DIEM
            WHERE MaSV=? AND MaHP=? AND HocKy=? AND NamHoc=?
            """
            return db.execute(sql, (msv, mhp, hk, nh))
        finally:
            db.close()