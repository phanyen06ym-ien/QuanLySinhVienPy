from database.connect import get_connection


def login(username, password):
    conn = get_connection()
    if not conn:
        return None

    try:
        cursor = conn.cursor()
        cursor.execute("""
            SELECT VaiTro, MaSV, MaGV
            FROM TAIKHOAN
            WHERE TenDangNhap=? AND MatKhau=?
        """, (username, password))
        return cursor.fetchone()
    finally:
        conn.close()


def update_password(username, new_password):
    conn = get_connection()
    if not conn:
        return False

    try:
        cursor = conn.cursor()
        cursor.execute("""
            UPDATE TAIKHOAN
            SET MatKhau=?
            WHERE TenDangNhap=?
        """, (new_password, username))

        conn.commit()
        return cursor.rowcount > 0

    finally:
        conn.close()