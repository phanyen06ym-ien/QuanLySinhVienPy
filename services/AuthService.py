from database.db import Database

class AuthService:

    @staticmethod
    def login(username, password):
        db = Database()
        try:
            sql = "EXEC spLogin ?, ?"
            return db.fetchone(sql, (username, password))
        finally:
            db.close()


    @staticmethod
    def update_password(username, new_password):
        db = Database()
        try:
            sql = "EXEC spDoiMatKhau ?, ?"
            return db.execute(sql, (username, new_password))
        finally:
            db.close()