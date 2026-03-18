import pyodbc
from config.db_config import SERVER, DATABASE, USERNAME, PASSWORD

def get_connection():
    try:
        conn = pyodbc.connect(
            f"DRIVER={{SQL Server}};"
            f"SERVER={SERVER};"
            f"DATABASE={DATABASE};"
            f"UID={USERNAME};"
            f"PWD={PASSWORD};"
        )
        return conn
    except Exception as e:
        print("loi:", e)
        return None


# test
if __name__ == "__main__":
    conn = get_connection()
    if conn:
        print("ket noi thanh cong!")
    else:
        print("ket noi that bai!")