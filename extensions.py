# extensions.py
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from flask_bcrypt import Bcrypt
import pymysql

# ====================================================
# Inisialisasi Ekstensi Flask
# ====================================================

# ORM untuk koneksi database MySQL
db = SQLAlchemy()

# Autentikasi dan session user
login_manager = LoginManager()
login_manager.login_view = 'auth.login'          # endpoint untuk redirect login
login_manager.login_message_category = 'info'    # kategori pesan flash

# Enkripsi password
bcrypt = Bcrypt()

# ====================================================
# Koneksi langsung ke MySQL (opsional, non-SQLAlchemy)
# ====================================================
def get_mysql_connection():
    """
    Fungsi ini digunakan jika ingin menjalankan query SQL langsung
    tanpa melalui SQLAlchemy.
    """
    try:
        connection = pymysql.connect(
            host='localhost',
            user='root',
            password='',
            database='smkmuliabuana',
            cursorclass=pymysql.cursors.DictCursor
        )
        return connection
    except pymysql.MySQLError as e:
        print(f"❌ Gagal konek ke MySQL langsung: {e}")
        return None
