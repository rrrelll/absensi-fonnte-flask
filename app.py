# app.py
from flask import Flask, redirect, url_for
from extensions import db, login_manager
import os

# =========================================================
# Inisialisasi Flask App
# =========================================================
app = Flask(__name__)

# =========================================================
# KONFIG DATABASE UNTUK RAILWAY & LOCAL
# =========================================================

DATABASE_URL = os.getenv("MYSQL_PUBLIC_URL")  # gunakan PRIVATE endpoint dari Railway

if DATABASE_URL:
    # Railway: ganti mysql:// -> mysql+pymysql://
    app.config["SQLALCHEMY_DATABASE_URI"] = DATABASE_URL.replace(
        "mysql://", "mysql+pymysql://"
    )
else:
    # Local development
    app.config["SQLALCHEMY_DATABASE_URI"] = "mysql+pymysql://root:@localhost/smkmuliabuana"

app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
app.config["SECRET_KEY"] = os.getenv("SECRET_KEY", "supersecret")

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

