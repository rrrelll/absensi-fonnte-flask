from flask import Blueprint, render_template, request, redirect, url_for, flash
from extensions import db
from models.jurusan import Jurusan  # pastikan file models/jurusan.py ada dan benar

jurusan_bp = Blueprint('jurusan', __name__, url_prefix='/jurusan')


# ==========================
# 📋 Tampilkan & Tambah Jurusan
# ==========================
@jurusan_bp.route('/', methods=['GET', 'POST'])
def list_jurusan():
    if request.method == 'POST':
        nama_jurusan = request.form.get('nama_jurusan', '').strip()

        if not nama_jurusan:
            flash('Nama jurusan tidak boleh kosong!', 'danger')
        else:
            # Cek agar tidak duplikat
            existing = Jurusan.query.filter_by(nama_jurusan=nama_jurusan).first()
            if existing:
                flash('Nama jurusan sudah ada!', 'warning')
            else:
                new_jurusan = Jurusan(nama_jurusan=nama_jurusan)
                db.session.add(new_jurusan)
                db.session.commit()
                flash('Jurusan berhasil ditambahkan!', 'success')
            return redirect(url_for('jurusan.list_jurusan'))

    # ✅ Urutkan berdasarkan nama (A–Z)
    data_jurusan = Jurusan.query.order_by(Jurusan.nama_jurusan.asc()).all()
    return render_template('jurusan.html', jurusan=data_jurusan)


# ==========================
# ✏️ Edit Jurusan
# ==========================
@jurusan_bp.route('/edit', methods=['POST'])
def edit_jurusan():
    id = request.form.get('id')
    nama_jurusan = request.form.get('nama_jurusan', '').strip()

    if not nama_jurusan:
        flash('Nama jurusan tidak boleh kosong!', 'danger')
        return redirect(url_for('jurusan.list_jurusan'))

    jurusan = Jurusan.query.get_or_404(id)

    # Cegah nama ganda
    existing = Jurusan.query.filter(Jurusan.nama_jurusan == nama_jurusan, Jurusan.id != id).first()
    if existing:
        flash('Nama jurusan sudah digunakan!', 'warning')
        return redirect(url_for('jurusan.list_jurusan'))

    jurusan.nama_jurusan = nama_jurusan
    db.session.commit()
    flash('Jurusan berhasil diperbarui!', 'success')
    return redirect(url_for('jurusan.list_jurusan'))


# ==========================
# 🗑️ Hapus Jurusan
# ==========================
@jurusan_bp.route('/delete', methods=['POST'])
def delete_jurusan():
    id = request.form.get('id')
    jurusan = Jurusan.query.get_or_404(id)

    try:
        db.session.delete(jurusan)
        db.session.commit()
        flash('Jurusan berhasil dihapus!', 'success')
    except Exception as e:
        db.session.rollback()
        flash(f'Terjadi kesalahan saat menghapus jurusan: {e}', 'danger')

    return redirect(url_for('jurusan.list_jurusan'))
