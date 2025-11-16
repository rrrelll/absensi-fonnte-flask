from extensions import db

class Jurusan(db.Model):
    __tablename__ = 'jurusan'

    id = db.Column(db.Integer, primary_key=True)
    nama_jurusan = db.Column(db.String(100), unique=True, nullable=False)  # Sesuai dengan database

    # Hapus relasi otomatis ke Siswa karena tidak ada foreign key
    # Gunakan query manual: Siswa.query.filter_by(jurusan=nama_jurusan).all()

    def __repr__(self):
        return f"<Jurusan {self.nama_jurusan}>"
