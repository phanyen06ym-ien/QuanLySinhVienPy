from database.connect import get_connection

def get_classes():
    conn = get_connection()
    if not conn:
        return []

    try:
        cursor = conn.cursor()
        cursor.execute("SELECT MaLop, TenLop FROM LOPHOC")
        return cursor.fetchall()
    finally:
        conn.close()


def get_students_in_class(ma_lop):
    conn = get_connection()
    if not conn:
        return []

    try:
        cursor = conn.cursor()
        cursor.execute("""
            SELECT MaSV, HoTen 
            FROM SINHVIEN 
            WHERE MaLop=?
        """, (ma_lop,))
        return cursor.fetchall()
    finally:
        conn.close()