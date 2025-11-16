# routes/dasbor.py
from flask import Blueprint, render_template
from flask_login import login_required, current_user
from datetime import date
from models.absensi import Absensi  # ✅ model dipanggil langsung
from extensions import db  # ✅ ambil instance db dari extensions.py

# ============================
# Blueprint Dasbor
# ============================
dasbor_bp = Blueprint('dasbor', __name__, url_prefix='/dasbor')


@dasbor_bp.route('/')
@login_required
def dasbor_index():
    """Halaman utama dasbor guru"""

    today = date.today()

    # ✅ Hitung jumlah absensi berdasarkan status hari ini
    sakit = Absensi.query.filter_by(tanggal=today, status='Sakit').count()
    izin = Absensi.query.filter_by(tanggal=today, status='Izin').count()
    alfa = Absensi.query.filter_by(tanggal=today, status='Alfa').count()  # gunakan 'Alfa' agar konsisten dengan data
    hadir = Absensi.query.filter_by(tanggal=today, status='Hadir').count()

    # ✅ Pastikan semua variabel dikirim ke template
    return render_template(
        'dasbor.html',
        guru_nama=getattr(current_user, 'nama', 'Guru'),
        sakit=sakit,
        izin=izin,
        alfa=alfa,
        hadir=hadir
    )
