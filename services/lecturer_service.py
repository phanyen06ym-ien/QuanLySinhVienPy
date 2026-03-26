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
            FROM GIANGVIEN WHERE MaGV=?
        """, (ma_gv,))
        return cur.fetchone()
    finally:
        conn.close()


# ================= LỚP =================
def get_classes(ma_gv):
    conn = get_connection()
    if not conn:
        return []
    try:
        cur = conn.cursor()
        cur.execute("""
            SELECT MaLop, TenLop, ChuyenNganh
            FROM LOPHOC
            WHERE CoVanHocTap=?
        """, (ma_gv,))
        return cur.fetchall()
    finally:
        conn.close()


# ================= SINH VIÊN =================
def get_student_name(msv):
    conn = get_connection()
    if not conn:
        return None
    try:
        cur = conn.cursor()
        cur.execute("SELECT HoTen FROM SINHVIEN WHERE MaSV=?", (msv,))
        return cur.fetchone()
    finally:
        conn.close()


# ================= ĐIỂM =================
def get_grades():
    conn = get_connection()
    if not conn:
        return []
    try:
        cur = conn.cursor()
        cur.execute("""
            SELECT d.MaSV, s.HoTen, d.MaHP, d.HocKy, d.NamHoc,
       CAST(d.DiemChuyenCan AS FLOAT), 
       CAST(d.DiemBaiTap AS FLOAT), 
       CAST(d.DiemGiuaKy AS FLOAT),
       CAST(d.DiemCuoiKy AS FLOAT), 
       CAST(d.DiemTongKet AS FLOAT)
            FROM DIEM d
            LEFT JOIN SINHVIEN s ON d.MaSV = s.MaSV
            ORDER BY d.MaSV, d.NamHoc, d.HocKy
        """)
        return cur.fetchall()
    finally:
        conn.close()


# ================= SAVE ĐIỂM =================
def save_grade(msv, mhp, hk, nh, cc, bt, gk, ck):
    conn = get_connection()
    if not conn:
        return
    try:
        cur = conn.cursor()

        cur.execute("""
            SELECT 1 FROM DIEM
            WHERE MaSV=? AND MaHP=? AND HocKy=? AND NamHoc=?
        """, (msv, mhp, hk, nh))

        if cur.fetchone():
            cur.execute("""
                UPDATE DIEM
                SET DiemChuyenCan=?, DiemBaiTap=?, DiemGiuaKy=?, DiemCuoiKy=?
                WHERE MaSV=? AND MaHP=? AND HocKy=? AND NamHoc=?
            """, (cc, bt, gk, ck, msv, mhp, hk, nh))
        else:
            cur.execute("""
                INSERT INTO DIEM
                (MaSV, MaHP, HocKy, NamHoc,
                 DiemChuyenCan, DiemBaiTap, DiemGiuaKy, DiemCuoiKy)
                VALUES (?,?,?,?,?,?,?,?)
            """, (msv, mhp, hk, nh, cc, bt, gk, ck))

        conn.commit()
    finally:
        conn.close()


# ================= DELETE =================
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