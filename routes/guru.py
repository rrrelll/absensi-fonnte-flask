# routes/guru.py
from flask import Blueprint, render_template, request, redirect, url_for, flash
from extensions import db
from models.guru import Guru

guru_bp = Blueprint("guru", __name__, url_prefix="/guru")


# ==========================
# 📋 Tampilkan semua guru
# ==========================
@guru_bp.route("/")
def list_guru():
    data = Guru.query.order_by(Guru.nama.asc()).all()
    return render_template("guru.html", guru=data)


# ==========================
# ➕ Tambah guru baru
# ==========================
@guru_bp.route("/add", methods=["POST"])
def add_guru():
    nama = request.form.get("nama", "").strip()
    username = request.form.get("username", "").strip()
    password = request.form.get("password", "").strip()

    if not nama or not username or not password:
        flash("Semua field wajib diisi!", "danger")
        return redirect(url_for("guru.list_guru"))

    # Cegah duplikasi username
    if Guru.query.filter_by(username=username).first():
        flash("Username sudah digunakan!", "warning")
        return redirect(url_for("guru.list_guru"))

    new_guru = Guru(nama=nama, username=username, password=password)
    db.session.add(new_guru)
    db.session.commit()

    flash("✅ Data guru berhasil ditambahkan!", "success")
    return redirect(url_for("guru.list_guru"))


# ==========================
# ✏️ Edit guru
# ==========================
@guru_bp.route("/edit", methods=["POST"])
def edit_guru():
    id = request.form.get("id")
    guru = Guru.query.get_or_404(id)

    nama = request.form.get("nama", "").strip()
    username = request.form.get("username", "").strip()
    password = request.form.get("password", "").strip()

    if not nama or not username:
        flash("Nama dan username wajib diisi!", "danger")
        return redirect(url_for("guru.list_guru"))

    # Cegah duplikasi username saat edit
    existing_user = Guru.query.filter(Guru.username == username, Guru.id != id).first()
    if existing_user:
        flash("Username sudah digunakan oleh guru lain!", "warning")
        return redirect(url_for("guru.list_guru"))

    guru.nama = nama
    guru.username = username
    if password:
        guru.password = password

    db.session.commit()
    flash("✏️ Data guru berhasil diperbarui!", "success")
    return redirect(url_for("guru.list_guru"))


# ==========================
# 🗑️ Hapus guru
# ==========================
@guru_bp.route("/delete", methods=["POST"])
def delete_guru():
    id = request.form.get("id")
    guru = Guru.query.get_or_404(id)

    db.session.delete(guru)
    db.session.commit()

    flash("🗑️ Data guru berhasil dihapus!", "success")
    return redirect(url_for("guru.list_guru"))
