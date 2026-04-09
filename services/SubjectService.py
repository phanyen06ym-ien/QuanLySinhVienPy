from database.db import Database


class SubjectService:

    # ================= DANH SÁCH HỌC PHẦN =================
    @staticmethod
    def get_all():
        db = Database()
        try:
            return db.fetchall("EXEC spXemHocPhan")
        finally:
            db.close()


    # ================= THÊM HỌC PHẦN =================
    @staticmethod
    def add(ma_hp, ten_hp, tin_chi, ma_khoa):
        db = Database()
        try:
            sql = "EXEC spThemHocPhan ?, ?, ?, ?"
            return db.execute(sql, (ma_hp, ten_hp, tin_chi, ma_khoa))
        finally:
            db.close()


    # ================= SỬA HỌC PHẦN =================
    @staticmethod
    def update(ma_hp, ten_hp, tin_chi, ma_khoa):
        db = Database()
        try:
            sql = "EXEC spSuaHocPhan ?, ?, ?, ?"
            return db.execute(sql, (ma_hp, ten_hp, tin_chi, ma_khoa))
        finally:
            db.close()


    # ================= XÓA HỌC PHẦN =================
    @staticmethod
    def delete(ma_hp):
        db = Database()
        try:
            sql = "EXEC spXoaHocPhan ?"
            return db.execute(sql, (ma_hp,))
        finally:
            db.close()