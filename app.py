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

# Jika Railway menyediakan variabel env, pakai itu
MYSQLUSER = os.getenv("root")
MYSQLPASSWORD = os.getenv("RrhbInnXYcFmBpknRZXFlegdtWivOtuj")
MYSQLHOST = os.getenv("mysql.railway.internal")
MYSQLPORT = os.getenv("3306")
MYSQLDATABASE = os.getenv("railway")

if MYSQLUSER and MYSQLHOST:
    # Mode DEPLOY (Railway)
    app.config["SQLALCHEMY_DATABASE_URI"] = (
        f"mysql+pymysql://{MYSQLUSER}:{MYSQLPASSWORD}"
        f"@{MYSQLHOST}:{MYSQLPORT}/{MYSQLDATABASE}"
    )
else:
    # Mode LOCAL (XAMPP)
    app.config["SQLALCHEMY_DATABASE_URI"] = (
        "mysql+pymysql://root:@localhost/smkmuliabuana"
    )

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

# =========================================================
# Jalankan untuk Lokal
# =========================================================
#if __name__ == '__main__':
 #   port = int(os.getenv("PORT", 5000))
  #  app.run(host="0.0.0.0", port=port)

