from flask import Blueprint, render_template, request, redirect, url_for, flash, session
from flask_login import login_user
from extensions import db, bcrypt
from models.guru import Guru

auth_bp = Blueprint("auth", __name__, url_prefix="/auth")

@auth_bp.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        username = request.form.get("username")
        password = request.form.get("password")

        guru = Guru.query.filter_by(username=username).first()

        if guru and bcrypt.check_password_hash(guru.password, password):
            login_user(guru)   # Pakai Flask-Login
            flash("Berhasil login!", "success")
            return redirect(url_for("dasbor.dasbor_index"))
        else:
            flash("Username atau password salah!", "danger")

    return render_template("login.html")

@auth_bp.route("/logout")
def logout():
    session.clear()
    flash("Anda telah logout.", "info")
    return redirect(url_for("auth.login"))


@auth_bp.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        nama = request.form.get("nama")
        username = request.form.get("username")
        password = request.form.get("password")

        # Validasi isian
        if not nama or not username or not password:
            flash("Semua field harus diisi.", "danger")
            return redirect(url_for("auth.register"))

        # Cek username sudah dipakai atau belum
        if Guru.query.filter_by(username=username).first():
            flash("Username sudah digunakan, coba yang lain!", "danger")
            return redirect(url_for("auth.register"))

        # Hash password dan simpan
        hashed_pw = bcrypt.generate_password_hash(password).decode('utf-8')
        guru = Guru(nama=nama, username=username, password=hashed_pw)
        db.session.add(guru)
        db.session.commit()

        flash("Registrasi berhasil, silakan login.", "success")
        return redirect(url_for("auth.login"))

    return render_template("register.html")


