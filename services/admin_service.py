from database.connect import get_connection
# ===== TÀI KHOẢN =====

def get_all_taikhoan():
    conn = get_connection()
    if not conn:
        return []
    try:
        cursor = conn.cursor()
        cursor.execute("SELECT TenDangNhap, MatKhau, VaiTro FROM TAIKHOAN")
        return cursor.fetchall()
    finally:
        conn.close()


def add_taikhoan(username, password, role):
    conn = get_connection()
    if not conn:
        return False
    try:
        cursor = conn.cursor()
        cursor.execute("INSERT INTO TAIKHOAN VALUES (?, ?, ?)", (username, password, role))
        conn.commit()
        return True
    except Exception as e:
        print("Lỗi thêm tài khoản:", e) # Xem lỗi chi tiết ở terminal
        return False
    finally:
        conn.close()


def delete_taikhoan(username):
    conn = get_connection()
    if not conn:
        return False
    try:
        cursor = conn.cursor()
        cursor.execute("DELETE FROM TAIKHOAN WHERE TenDangNhap=?", (username,))
        conn.commit()
        return True
    finally:
        conn.close()

# ===== SINH VIÊN =====

def get_all_sinhvien():
    conn = get_connection()
    if not conn: return []
    try:
        cursor = conn.cursor()
        cursor.execute("SELECT MaSV, HoTen, GioiTinh, NgaySinh, SDT, DiaChi, MaLop, NamThu, KhoaHoc FROM SINHVIEN")
        rows = cursor.fetchall()
        # Chuyển đổi dữ liệu sang list để tránh lỗi hiển thị Tuple (ngoặc đơn)
        return [list(row) for row in rows]
    finally:
        conn.close()


def add_sinhvien(data):
    conn = get_connection()
    if not conn:
        return False
    try:
        cursor = conn.cursor()
        cursor.execute("""
            INSERT INTO SINHVIEN
            VALUES (?,?,?,?,?,?,?,?,?)
        """, data)
        conn.commit()
        return True
    except Exception as e:
        print("Lỗi thêm SV:", e)
        return False
    finally:
        conn.close()


def update_sinhvien(data):
    conn = get_connection()
    if not conn: return False
    try:
        cursor = conn.cursor()
        cursor.execute("""
            UPDATE SINHVIEN SET
            HoTen=?, GioiTinh=?, NgaySinh=?, SDT=?,
            DiaChi=?, MaLop=?, NamThu=?, KhoaHoc=?
            WHERE MaSV=?
        """, data)
        conn.commit()
        return True
    except Exception as e:
        print("Lỗi Update SV:", e)
        return False
    finally:
        conn.close()


def delete_sinhvien(masv):
    conn = get_connection()
    if not conn:
        return False
    try:
        cursor = conn.cursor()
        cursor.execute("DELETE FROM SINHVIEN WHERE MaSV=?", (masv,))
        conn.commit()
        return True
    finally:
        conn.close()
# ===== GIẢNG VIÊN =====

def get_all_giangvien():
    conn = get_connection()
    cursor = conn.cursor()
    # Chỉ chọn các cột thực sự có trong bảng GIANGVIEN
    cursor.execute("SELECT MaGV, HoTen, GioiTinh, DiaChi, Email, MaKhoa FROM GIANGVIEN")
    rows = cursor.fetchall()
    conn.close()
    return rows


def add_giangvien(data):
    try:
        conn = get_connection()
        cursor = conn.cursor()
        # Data truyền vào từ AdminForm sẽ không còn NgaySinh
        sql = "INSERT INTO GIANGVIEN (MaGV, HoTen, GioiTinh, DiaChi, Email, MaKhoa) VALUES (?, ?, ?, ?, ?, ?)"
        cursor.execute(sql, data)
        conn.commit()
        conn.close()
        return True
    except Exception as e:
        print(f"Lỗi SQL: {e}")
        return False


def update_giangvien(data):
    try:
        conn = get_connection()
        cursor = conn.cursor()
        # Đảm bảo thứ tự tham số trong mảng data khớp với câu lệnh UPDATE
        sql = "UPDATE GIANGVIEN SET HoTen=?, GioiTinh=?, DiaChi=?, Email=?, MaKhoa=? WHERE MaGV=?"
        cursor.execute(sql, data)
        conn.commit()
        conn.close()
        return True
    except Exception as e:
        print(f"Lỗi SQL: {e}")
        return False


def delete_giangvien(magv):
    conn = get_connection()
    if not conn:
        return False
    try:
        cursor = conn.cursor()
        cursor.execute("DELETE FROM GIANGVIEN WHERE MaGV=?", (magv,))
        conn.commit()
        return True
    except Exception as e:
        print("Lỗi xóa GV:", e)
        return False
    finally:
        conn.close()

# ===== HỌC PHẦN =====

def get_all_hocphan():
    conn = get_connection()
    if not conn:
        return []
    try:
        cursor = conn.cursor()
        cursor.execute("SELECT MaHP, TenHP, TinChi FROM HOCPHAN")
        rows = cursor.fetchall()
        return rows
    finally:
        conn.close()

def add_hocphan(ma_hp, ten_hp, tin_chi):
    conn = get_connection()
    if not conn: return False
    try:
        cursor = conn.cursor()
        cursor.execute("INSERT INTO HOCPHAN (MaHP, TenHP, TinChi) VALUES (?, ?, ?)",
                       (ma_hp, ten_hp, tin_chi))
        conn.commit()
        return True
    except Exception as e:
        print("Lỗi thêm học phần:", e)
        return False
    finally:
        conn.close()
def delete_hocphan(ma_hp):
    conn = get_connection()
    if not conn: return False
    try:
        cursor = conn.cursor()
        cursor.execute("DELETE FROM HOCPHAN WHERE MaHP=?", (ma_hp,))
        conn.commit()
        return True
    except Exception as e:
        print("Lỗi xóa học phần:", e)
        return False
    finally:
        conn.close()
# ===== BÁO CÁO =====

def get_baocao():
    conn = get_connection()
    if not conn:
        return []
    try:
        cursor = conn.cursor()
        # Lấy các thông tin cần thiết: Mã SV, Tên SV, Tên HP và Điểm tổng kết
        cursor.execute("""
            SELECT s.MaSV, s.HoTen, h.TenHP, d.DiemTongKet
            FROM DIEM d
            JOIN SINHVIEN s ON d.MaSV = s.MaSV
            JOIN HOCPHAN h ON d.MaHP = h.MaHP
            ORDER BY d.DiemTongKet DESC -- Sắp xếp điểm từ cao xuống thấp
        """)
        return cursor.fetchall()
    finally:
        conn.close()