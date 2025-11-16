from extensions import db
from datetime import datetime

class Absensi(db.Model):
    __tablename__ = "absensi"

    # Primary key
    id = db.Column(db.Integer, primary_key=True)

    # Relasi ke Siswa
    siswa_id = db.Column(db.Integer, db.ForeignKey("siswa.id"), nullable=False)
    siswa = db.relationship(
        "Siswa",
        backref=db.backref("absensi_list", lazy=True)  # tetap bisa pakai backref untuk Siswa
    )

    # Relasi ke Guru
    guru_id = db.Column(db.Integer, db.ForeignKey("guru.id"), nullable=False)
    guru = db.relationship(
        "Guru",
        back_populates="absensi_guru_list"  # harus ada field absensi_guru_list di model Guru
    )

    # Relasi ke Mata Pelajaran
    mata_pelajaran_id = db.Column(db.Integer, db.ForeignKey('mata_pelajaran.id'), nullable=False)
    mapel = db.relationship(
        'MataPelajaran',
        back_populates='absensi_list',
        foreign_keys=[mata_pelajaran_id]
    )

    # Tanggal absensi
    tanggal = db.Column(db.Date, default=datetime.utcnow)

    # Status absensi
    status = db.Column(
        db.Enum('Hadir', 'Tidak Hadir', 'Sakit', 'Izin', name="status_enum"),
        nullable=False
    )

    def __repr__(self):
        return (
            f"<Absensi Siswa:{self.siswa_id}, "
            f"Guru:{self.guru_id}, "
            f"Mapel:{self.mata_pelajaran_id}, "
            f"Tanggal:{self.tanggal}, "
            f"Status:{self.status}>"
        )
