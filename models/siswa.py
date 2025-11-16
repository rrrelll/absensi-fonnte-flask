from extensions import db
from models.mapel import MataPelajaran  # pastikan ini import model MataPelajaran

class Siswa(db.Model):
    __tablename__ = "siswa"

    id = db.Column(db.Integer, primary_key=True)
    nama = db.Column(db.String(100), nullable=False)
    nisn = db.Column(db.String(50), nullable=False)  # hapus unique=True
    kelas = db.Column(db.String(10), nullable=False)
    jurusan = db.Column(db.String(50), nullable=False)
    
    mapel_id = db.Column(db.Integer, db.ForeignKey('mata_pelajaran.id'), nullable=False)
    mapel = db.relationship('MataPelajaran', back_populates='siswa_list')

    nama_ortu = db.Column(db.String(100), nullable=False)
    no_ortu = db.Column(db.String(20), nullable=False)

    # Unique constraint gabungan nisn + mapel_id
    __table_args__ = (
        db.UniqueConstraint('nisn', 'mapel_id', name='unique_nisn_mapel'),
    )

    def __repr__(self):
        return f"<Siswa {self.nama} - {self.nisn}>"
