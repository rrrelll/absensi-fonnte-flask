from flask import Blueprint, render_template, request, redirect, url_for, flash
from sqlalchemy.exc import IntegrityError
from extensions import db
from models.siswa import Siswa
from models.jurusan import Jurusan
from models.mapel import MataPelajaran  # <- model mata pelajaran

siswa_bp = Blueprint('siswa', __name__, url_prefix='/siswa')

# ==========================
# 📋 Tampilkan semua siswa
# ==========================
@siswa_bp.route('/')
def list_siswa():
    siswa_list = Siswa.query.all()
    jurusan_list = Jurusan.query.order_by(Jurusan.nama_jurusan).all()
    mapel_list = MataPelajaran.query.order_by(MataPelajaran.nama_mapel).all()
    
    return render_template(
        'siswa.html',
        siswa=siswa_list,
        jurusan_list=jurusan_list,
        mapel_list=mapel_list
    )

# ==========================
# ➕ Tambah siswa baru
# ==========================
@siswa_bp.route('/add', methods=['POST'])
def add_siswa():
    nama = request.form.get('nama')
    nisn = request.form.get('nisn')
    kelas = request.form.get('kelas')
    jurusan = request.form.get('jurusan')
    mapel_id = request.form.get('mapel')  # <- ID dari tabel MataPelajaran
    nama_ortu = request.form.get('nama_ortu')
    no_ortu = request.form.get('no_ortu')

    # Cek unik berdasarkan kombinasi nisn + mapel
    existing_siswa = Siswa.query.filter_by(nisn=nisn, mapel_id=mapel_id).first()
    if existing_siswa:
        flash(f'Siswa dengan NISN {nisn} untuk mata pelajaran ini sudah ada.', 'danger')
        return redirect(url_for('siswa.list_siswa'))

    new_siswa = Siswa(
        nama=nama,
        nisn=nisn,
        kelas=kelas,
        jurusan=jurusan,
        mapel_id=mapel_id,  # simpan ID MataPelajaran
        nama_ortu=nama_ortu,
        no_ortu=no_ortu
    )

    try:
        db.session.add(new_siswa)
        db.session.commit()
        flash('Data siswa berhasil ditambahkan ✅', 'success')
    except IntegrityError:
        db.session.rollback()
        flash('Terjadi kesalahan! Pastikan data valid.', 'danger')

    return redirect(url_for('siswa.list_siswa'))

# ==========================
# ✏️ Edit siswa
# ==========================
@siswa_bp.route('/edit/<int:id>', methods=['GET', 'POST'])
def edit_siswa(id):
    siswa = Siswa.query.get_or_404(id)
    jurusan_list = Jurusan.query.order_by(Jurusan.nama_jurusan).all()
    mapel_list = MataPelajaran.query.order_by(MataPelajaran.nama_mapel).all()

    if request.method == 'POST':
        nisn_baru = request.form.get('nisn')
        mapel_baru = request.form.get('mapel')

        # Cek unik berdasarkan nisn + mapel, kecuali data yang sedang diedit
        existing_siswa = Siswa.query.filter_by(nisn=nisn_baru, mapel_id=mapel_baru).first()
        if existing_siswa and existing_siswa.id != siswa.id:
            flash(f'Siswa dengan NISN {nisn_baru} untuk mata pelajaran ini sudah digunakan.', 'danger')
            return redirect(url_for('siswa.list_siswa'))

        siswa.nama = request.form.get('nama')
        siswa.nisn = nisn_baru
        siswa.kelas = request.form.get('kelas')
        siswa.jurusan = request.form.get('jurusan')
        siswa.mapel_id = mapel_baru
        siswa.nama_ortu = request.form.get('nama_ortu')
        siswa.no_ortu = request.form.get('no_ortu')

        try:
            db.session.commit()
            flash('Data siswa berhasil diperbarui ✅', 'success')
        except IntegrityError:
            db.session.rollback()
            flash('Gagal memperbarui data! Pastikan data valid.', 'danger')

        return redirect(url_for('siswa.list_siswa'))

    return render_template(
        'edit_siswa.html',
        siswa=siswa,
        jurusan_list=jurusan_list,
        mapel_list=mapel_list
    )

# ==========================
# 🗑️ Hapus siswa
# ==========================
@siswa_bp.route('/delete', methods=['POST'])
def delete_siswa():
    id = request.form.get('id')
    siswa = Siswa.query.get_or_404(id)

    try:
        db.session.delete(siswa)
        db.session.commit()
        flash('Data siswa berhasil dihapus 🗑️', 'success')
    except Exception:
        db.session.rollback()
        flash('Gagal menghapus data siswa.', 'danger')

    return redirect(url_for('siswa.list_siswa'))
