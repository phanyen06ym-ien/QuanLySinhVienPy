from database.connect import get_connection

# ================= SINH VIÊN =================
def get_info(ma_sv):
    conn = get_connection()
    if not conn:
        return None
    try:
        cur = conn.cursor()
        cur.execute("""
            SELECT HoTen, NgaySinh, DiaChi, GioiTinh,
                   SDT, MaLop, NamThu, KhoaHoc
            FROM SINHVIEN
            WHERE MaSV=?
        """, (ma_sv,))
        return cur.fetchone()
    finally:
        conn.close()

# ================= ĐIỂM =================
def get_grades(ma_sv):
    conn = get_connection()
    if not conn:
        return []
    try:
        cur = conn.cursor()
        cur.execute("""
            SELECT D.MaHP, H.TenHP, D.HocKy, D.NamHoc, 
                   CAST(D.DiemChuyenCan AS FLOAT), 
                   CAST(D.DiemBaiTap AS FLOAT),
                   CAST(D.DiemGiuaKy AS FLOAT), 
                   CAST(D.DiemCuoiKy AS FLOAT), 
                   CAST(D.DiemTongKet AS FLOAT)
            FROM DIEM D
            JOIN HOCPHAN H ON D.MaHP = H.MaHP
            WHERE D.MaSV=?
        """, (ma_sv,))
        return cur.fetchall()
    finally:
        conn.close()

# ================= ĐĂNG KÝ =================
def check_registered(ma_sv, ma_hp, hk, nh):
    conn = get_connection()
    if not conn:
        return False
    try:
        cur = conn.cursor()
        cur.execute("""
            SELECT 1 FROM DANGKY
            WHERE MaSV=? AND MaHP=? AND HocKy=? AND NamHoc=?
        """, (ma_sv, ma_hp, hk, nh))
        return cur.fetchone() is not None
    finally:
        conn.close()

def register_course(ma_sv, ma_hp, hk, nh):
    conn = get_connection()
    if not conn:
        return False, "Không kết nối database"
    try:
        cur = conn.cursor()
        cur.execute("""
            INSERT INTO DANGKY (MaSV, MaHP, HocKy, NamHoc)
            VALUES (?, ?, ?, ?)
        """, (ma_sv, ma_hp, hk, nh))
        conn.commit()
        return True, "Đăng ký thành công"
    except Exception as e:
        return False, str(e)
    finally:
        conn.close()

def register_course_logic(ma_sv, ma_hp, hk, nh):
    if check_registered(ma_sv, ma_hp, hk, nh):
        return False, "Bạn đã đăng ký môn này rồi!"
    return register_course(ma_sv, ma_hp, hk, nh)

# ================= DANH SÁCH ĐÃ ĐĂNG KÝ =================
def get_registered_courses(ma_sv):
    conn = get_connection()
    if not conn:
        return []
    try:
        cur = conn.cursor()
        cur.execute("""
            SELECT D.MaHP, H.TenHP, D.HocKy, D.NamHoc
            FROM DANGKY D
            JOIN HOCPHAN H ON D.MaHP = H.MaHP
            WHERE D.MaSV=?
        """, (ma_sv,))
        return cur.fetchall()
    finally:
        conn.close()

# ================= BƯỚC 1: LẤY TẤT CẢ HỌC PHẦN (HÀM MỚI) =================

# Copy đoạn này dán vào cuối file student_service.py
def get_all_subjects():
    conn = get_connection()
    if not conn:
        return []
    try:
        cur = conn.cursor()
        # Lấy MaHP và TenHP từ bảng HOCPHAN
        cur.execute("SELECT MaHP, TenHP FROM HOCPHAN")
        return cur.fetchall()
    finally:
        conn.close()