# routes/mapel.py
from flask import Blueprint, render_template, request, redirect, url_for, flash
from extensions import db
from models.mapel import MataPelajaran

mapel_bp = Blueprint('mapel', __name__, url_prefix='/mapel')


# ===============================
# 📋 List & Tambah Mata Pelajaran
# ===============================
@mapel_bp.route('/', methods=['GET', 'POST'])
def list_mapel():
    if request.method == 'POST':
        nama_mapel = request.form.get('nama_mapel', '').strip()
        if not nama_mapel:
            flash("Nama mata pelajaran tidak boleh kosong!", "danger")
        else:
            # ✅ Cek duplikat
            existing = MataPelajaran.query.filter_by(nama_mapel=nama_mapel).first()
            if existing:
                flash(f"Mata Pelajaran '{nama_mapel}' sudah ada!", "warning")
            else:
                new_mapel = MataPelajaran(nama_mapel=nama_mapel)
                db.session.add(new_mapel)
                db.session.commit()
                flash(f"Mata Pelajaran '{nama_mapel}' berhasil ditambahkan!", "success")
            return redirect(url_for('mapel.list_mapel'))

    # ✅ Ambil semua mapel urut A-Z
    mapel = MataPelajaran.query.order_by(MataPelajaran.nama_mapel.asc()).all()
    return render_template('mapel_list.html', mapel=mapel)

# ===============================
# ✏️ Edit Mata Pelajaran
# ===============================
@mapel_bp.route('/edit/<int:id>', methods=['POST'])
def edit_mapel(id):
    nama_mapel = request.form.get('nama_mapel', '').strip()
    if not nama_mapel:
        flash("Nama mata pelajaran tidak boleh kosong!", "danger")
        return redirect(url_for('mapel.list_mapel'))

    mp = MataPelajaran.query.get_or_404(id)

    # ✅ Cek duplikat saat edit
    existing = MataPelajaran.query.filter(
        MataPelajaran.nama_mapel == nama_mapel,
        MataPelajaran.id != id
    ).first()
    if existing:
        flash(f"Mata Pelajaran '{nama_mapel}' sudah ada!", "warning")
        return redirect(url_for('mapel.list_mapel'))

    mp.nama_mapel = nama_mapel
    db.session.commit()
    flash(f"Mata Pelajaran '{nama_mapel}' berhasil diperbarui!", "success")
    return redirect(url_for('mapel.list_mapel'))


# ===============================
# 🗑️ Hapus Mata Pelajaran
# ===============================
@mapel_bp.route('/hapus/<int:id>', methods=['POST'])
def hapus_mapel(id):
    mp = MataPelajaran.query.get_or_404(id)
    db.session.delete(mp)
    db.session.commit()
    flash(f"Mata Pelajaran '{mp.nama_mapel}' berhasil dihapus!", "success")
    return redirect(url_for('mapel.list_mapel'))
