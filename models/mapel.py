from extensions import db

class MataPelajaran(db.Model):
    __tablename__ = "mata_pelajaran"

    id = db.Column(db.Integer, primary_key=True)
    nama_mapel = db.Column(db.String(100), nullable=False, unique=True)

    # Relasi ke Siswa (One-to-Many)
    siswa_list = db.relationship(
        "Siswa",
        back_populates="mapel",  # Akses Siswa.mapel
        lazy=True
    )

    # Relasi ke Absensi (One-to-Many)
    absensi_list = db.relationship(
        "Absensi",
        back_populates="mapel",  # Akses Absensi.mapel
        lazy=True
    )

    def __repr__(self):
        return f"<MataPelajaran {self.nama_mapel}>"
