import pyodbc

# ===== CONFIG =====
SERVER = r'(localdb)\MSSQLLocalDB'
DATABASE = 'QuanLySinhVien'


# ===== CONNECTION =====
def get_connection():
    try:
        conn_str = (
            "DRIVER={ODBC Driver 17 for SQL Server};"
            f"SERVER={SERVER};"
            f"DATABASE={DATABASE};"
            "Trusted_Connection=yes;"
            "TrustServerCertificate=yes;"
        )
        conn = pyodbc.connect(conn_str)
        return conn
    except Exception as e:
        raise Exception(f"Lỗi kết nối database: {e}")


# ===== DATABASE WRAPPER =====
class Database:
    def __init__(self):
        self.conn = get_connection()

    def fetchall(self, sql, params=None):
        try:
            cursor = self.conn.cursor()
            cursor.execute(sql, params or [])
            return cursor.fetchall()
        except Exception as e:
            print(" Lỗi fetchall:", e)
            return []

    def fetchone(self, sql, params=None):
        try:
            cursor = self.conn.cursor()
            cursor.execute(sql, params or [])
            return cursor.fetchone()
        except Exception as e:
            print(" Lỗi fetchone:", e)
            return None

    def execute(self, sql, params=None):
        try:
            cursor = self.conn.cursor()
            cursor.execute(sql, params or [])
            self.conn.commit()
            return True
        except Exception as e:
            print(" Lỗi execute:", e)
            self.conn.rollback()
            return False

    def close(self):
        if self.conn:
            self.conn.close()