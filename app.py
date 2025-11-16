# app.py
from flask import Flask, redirect, url_for
from extensions import db, login_manager
import pymysql
import os

# =========================================================
# Inisialisasi Flask App
# =========================================================
app = Flask(__name__)

# =========================================================
# KONFIG DATABASE UNTUK RAILWAY
# =========================================================
DB_HOST = os.getenv("DB_HOST", "localhost")
DB_USER = os.getenv("DB_USER", "root")
DB_PASSWORD = os.getenv("DB_PASSWORD", "")
DB_NAME = os.getenv("DB_NAME", "smkmuliabuana")
DB_PORT = os.getenv("DB_PORT", 3306)

app.config.update(
    SQLALCHEMY_DATABASE_URI=f"mysql+pymysql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}",
    SQLALCHEMY_TRACK_MODIFICATIONS=False,
    SECRET_KEY=os.getenv("SECRET_KEY", "supersecret")
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
    return Guru.query.get(int(guru_id))

# =========================================================
# Registrasi Blueprint
# =========================================================
from routes.auth import auth_bp
from routes.siswa import siswa_bp
from routes.absensi import absensi_bp
from routes.guru import guru_bp
from routes.dasbor import dasbor_bp
from routes.jurusan import jurusan_bp
from routes.mapel import mapel_bp

app.register_blueprint(auth_bp)
app.register_blueprint(siswa_bp)
app.register_blueprint(absensi_bp)
app.register_blueprint(guru_bp)
app.register_blueprint(dasbor_bp)
app.register_blueprint(jurusan_bp)
app.register_blueprint(mapel_bp)

# =========================================================
# Route Default
# =========================================================
@app.route('/')
def home():
    return redirect(url_for('auth.login'))

# =========================================================
# Run App (untuk lokal)
# =========================================================
if __name__ == '__main__':
    app.run(debug=True)
