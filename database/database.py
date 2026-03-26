from .connect import get_connection

class Database:
    @staticmethod
    def get():
        conn = get_connection()
        if conn is None:
            raise Exception("Không thể kết nối DB")
        return DBWrapper(conn)


class DBWrapper:
    def __init__(self, conn):
        self.conn = conn

    def fetchall(self, sql, params=None):
        cursor = self.conn.cursor()
        cursor.execute(sql, params or [])
        return cursor.fetchall()

    def fetchone(self, sql, params=None):
        cursor = self.conn.cursor()
        cursor.execute(sql, params or [])
        return cursor.fetchone()

    def execute(self, sql, params=None):
        try:
            cursor = self.conn.cursor()
            cursor.execute(sql, params or [])
            self.conn.commit()
            return True
        except Exception as e:
            print("Lỗi SQL:", e)
            self.conn.rollback()
            return False

    def close(self):
        self.conn.close()