from extensions import db, bcrypt
from flask_login import UserMixin

class Guru(UserMixin, db.Model):
    __tablename__ = "guru"

    id = db.Column(db.Integer, primary_key=True)
    nama = db.Column(db.String(100), nullable=False)
    username = db.Column(db.String(50), unique=True, nullable=False)
    password = db.Column(db.String(255), nullable=False)

    # Relasi ke Absensi (One-to-Many)
    absensi_guru_list = db.relationship(
        "Absensi",
        back_populates="guru",  # harus sama dengan guru di model Absensi
        lazy=True
    )

    def set_password(self, plain_password):
        """Hash password sebelum disimpan"""
        self.password = bcrypt.generate_password_hash(plain_password).decode('utf-8')

    def check_password(self, plain_password):
        """Cek password saat login"""
        return bcrypt.check_password_hash(self.password, plain_password)

    def __repr__(self):
        return f"<Guru {self.nama} - {self.username}>"
