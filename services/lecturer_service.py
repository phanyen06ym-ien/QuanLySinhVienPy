from database.connect import get_connection

# ================= GIẢNG VIÊN =================
def get_info(ma_gv):
    conn = get_connection()
    if not conn:
        return None
    try:
        cur = conn.cursor()
        cur.execute("""
            SELECT MaGV, HoTen, GioiTinh, DiaChi, Email, MaKhoa
            FROM GIANGVIEN
            WHERE MaGV = ?
        """, (ma_gv,))
        return cur.fetchone()
    finally:
        conn.close()


# ================= LỚP PHỤ TRÁCH =================
def get_classes(ma_gv):
    conn = get_connection()
    if not conn:
        return []
    try:
        cur = conn.cursor()
        cur.execute("""
            SELECT MaLop, TenLop, ChuyenNganh
            FROM LOPHOC
            WHERE CoVanHocTap = ?
        """, (ma_gv,))
        return cur.fetchall()
    finally:
        conn.close()


# ================= HỌC PHẦN PHỤ TRÁCH =================
def get_subjects(ma_gv):
    conn = get_connection()
    if not conn:
        return []
    try:
        cur = conn.cursor()
        cur.execute("""
            SELECT 
                hp.MaHP,
                hp.TenHP,
                pc.MaLop,
                pc.HocKy,
                pc.NamHoc,
                pc.PhongHoc
            FROM PHANCONG pc
            JOIN HOCPHAN hp ON pc.MaHP = hp.MaHP
            WHERE pc.MaGV = ?
            ORDER BY pc.NamHoc DESC, pc.HocKy DESC
        """, (ma_gv,))
        return cur.fetchall()
    finally:
        conn.close()


# ================= SINH VIÊN THEO LỚP =================
def get_students_by_class(malop):
    conn = get_connection()
    if not conn:
        return []
    try:
        cur = conn.cursor()
        cur.execute("""
            SELECT MaSV, HoTen
            FROM SINHVIEN
            WHERE MaLop = ?
        """, (malop,))
        return cur.fetchall()
    finally:
        conn.close()


# ================= LẤY TÊN SINH VIÊN =================
def get_student_name(msv):
    conn = get_connection()
    if not conn:
        return None
    try:
        cur = conn.cursor()
        cur.execute("""
            SELECT HoTen FROM SINHVIEN WHERE MaSV = ?
        """, (msv,))
        return cur.fetchone()
    finally:
        conn.close()


# ================= ĐIỂM THEO HỌC PHẦN =================
def get_grades_by_hp(mahp, hk, nh):
    conn = get_connection()
    if not conn: return []
    try:
        cur = conn.cursor()
        # Sử dụng LIKE để linh hoạt hơn với dữ liệu năm học (ví dụ: '2025' vẫn khớp '2024-2025')
        query = """
            SELECT 
                dk.MaSV, s.HoTen, dk.MaHP, dk.HocKy, dk.NamHoc,
                ISNULL(d.DiemChuyenCan, 0), ISNULL(d.DiemBaiTap, 0),
                ISNULL(d.DiemGiuaKy, 0), ISNULL(d.DiemCuoiKy, 0), ISNULL(d.DiemTongKet, 0)
            FROM DANGKY dk
            JOIN SINHVIEN s ON dk.MaSV = s.MaSV
            LEFT JOIN DIEM d ON dk.MaSV = d.MaSV 
                AND dk.MaHP = d.MaHP 
                AND dk.HocKy = d.HocKy 
                AND dk.NamHoc = d.NamHoc
            WHERE dk.MaHP = ? AND dk.HocKy = ? AND dk.NamHoc LIKE ?
            ORDER BY dk.MaSV
        """
        cur.execute(query, (mahp, hk, f"%{nh}%"))
        return cur.fetchall()
    finally:
        conn.close()


# ================= LƯU / UPDATE ĐIỂM =================
def save_grade(msv, mhp, hk, nh, cc, bt, gk, ck):
    conn = get_connection()
    if not conn:
        return
    try:
        cur = conn.cursor()

        # Tính điểm tổng kết (có thể chỉnh lại)
        tongket = round(cc * 0.1 + bt * 0.2 + gk * 0.3 + ck * 0.4, 2)

        cur.execute("""
            SELECT 1 FROM DIEM
            WHERE MaSV=? AND MaHP=? AND HocKy=? AND NamHoc=?
        """, (msv, mhp, hk, nh))

        if cur.fetchone():
            cur.execute("""
                UPDATE DIEM
                SET 
                    DiemChuyenCan=?,
                    DiemBaiTap=?,
                    DiemGiuaKy=?,
                    DiemCuoiKy=?,
                    DiemTongKet=?
                WHERE MaSV=? AND MaHP=? AND HocKy=? AND NamHoc=?
            """, (cc, bt, gk, ck, tongket, msv, mhp, hk, nh))
        else:
            cur.execute("""
                INSERT INTO DIEM
                (MaSV, MaHP, HocKy, NamHoc,
                 DiemChuyenCan, DiemBaiTap,
                 DiemGiuaKy, DiemCuoiKy, DiemTongKet)
                VALUES (?,?,?,?,?,?,?,?,?)
            """, (msv, mhp, hk, nh, cc, bt, gk, ck, tongket))

        conn.commit()
    finally:
        conn.close()


# ================= XÓA ĐIỂM =================
def delete_grade(msv, mhp, hk, nh):
    conn = get_connection()
    if not conn:
        return
    try:
        cur = conn.cursor()
        cur.execute("""
            DELETE FROM DIEM
            WHERE MaSV=? AND MaHP=? AND HocKy=? AND NamHoc=?
        """, (msv, mhp, hk, nh))
        conn.commit()
    finally:
        conn.close()