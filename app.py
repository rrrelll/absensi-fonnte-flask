# app.py
from flask import Flask, redirect, url_for
from extensions import db, login_manager
import pymysql

# =========================================================
# Inisialisasi Flask App
# =========================================================
app = Flask(__name__)
app.config.update(
    SQLALCHEMY_DATABASE_URI='mysql+pymysql://root:@localhost/smkmuliabuana',
    SQLALCHEMY_TRACK_MODIFICATIONS=False,
    SECRET_KEY='supersecret'
)

# =========================================================
# Inisialisasi Ekstensi
# =========================================================
db.init_app(app)
login_manager.init_app(app)

# =========================================================
# Import Model untuk Flask-Login
# =========================================================
from models.guru import Guru

@login_manager.user_loader
def load_user(guru_id):
    """Mengambil data guru berdasarkan ID untuk Flask-Login"""
    return Guru.query.get(int(guru_id))

# =========================================================
# Registrasi Blueprint (Semua route di sini)
# =========================================================
# ⚠️ Urutan ini penting — harus setelah app & db siap
from routes.auth import auth_bp
from routes.siswa import siswa_bp
from routes.absensi import absensi_bp
from routes.guru import guru_bp
from routes.dasbor import dasbor_bp
from routes.jurusan import jurusan_bp
from routes.mapel import mapel_bp

# Daftarkan blueprint ke app utama
app.register_blueprint(auth_bp)
app.register_blueprint(siswa_bp)
app.register_blueprint(absensi_bp)
app.register_blueprint(guru_bp)
app.register_blueprint(dasbor_bp)
app.register_blueprint(jurusan_bp)
app.register_blueprint(mapel_bp)

# =========================================================
# Route Utama (Redirect ke Login)
# =========================================================
@app.route('/')
def home():
    return redirect(url_for('auth.login'))

# =========================================================
# Jalankan App
# =========================================================
if __name__ == '__main__':
    try:
        with app.app_context():
            db.create_all()  # Buat tabel jika belum ada
        print("✅ Database terhubung dan tabel siap digunakan.")
    except pymysql.MySQLError as e:
        print(f"❌ Gagal terhubung ke database: {e}")
    except Exception as e:
        print(f"⚠️ Terjadi kesalahan saat inisialisasi: {e}")

    # Jalankan server Flask
    app.run(debug=True)
