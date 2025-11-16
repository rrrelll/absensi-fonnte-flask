from flask import Blueprint, render_template, request, redirect, url_for, flash, jsonify, send_file
from flask_login import login_required, current_user
from extensions import db
from models.siswa import Siswa
from models.jurusan import Jurusan
from models.mapel import MataPelajaran
from models.absensi import Absensi
import requests
from datetime import datetime, date
import pytz
from sqlalchemy import func, case
from io import BytesIO
from reportlab.lib.pagesizes import A4
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Image, Spacer, Table as PlatypusTable

# ==================================================
# Blueprint Absensi
# ==================================================
absensi_bp = Blueprint('absensi', __name__, url_prefix='/absensi')

# Token WhatsApp Gateway (Fonnte)
FONNTE_TOKEN = "wJtSEyAqoZsHcHoHcN1g"
WIB = pytz.timezone('Asia/Jakarta')


# ==================================================
# Halaman Utama Absensi
# ==================================================
@absensi_bp.route('/', methods=['GET'])
@login_required
def absen_page():
    kelas = request.args.get('kelas')
    jurusan_selected = request.args.get('jurusan')
    mapel_selected = request.args.get('mapel')

    # Filter siswa
    siswa_query = Siswa.query
    if kelas:
        siswa_query = siswa_query.filter_by(kelas=kelas)
    if jurusan_selected:
        siswa_query = siswa_query.filter_by(jurusan=jurusan_selected)
    if mapel_selected and mapel_selected.isdigit():
        siswa_query = siswa_query.filter_by(mapel_id=int(mapel_selected))

    siswa_list = siswa_query.order_by(Siswa.nama.asc()).all()
    jurusan_list = [j.nama_jurusan for j in Jurusan.query.order_by(Jurusan.nama_jurusan).all()]
    mapel_list = MataPelajaran.query.order_by(MataPelajaran.nama_mapel).all()

    # Semester rekap setup
    mapel_rekap_id = request.args.get('mapel_rekap')
    semester = request.args.get('semester')
    rekap_results, mapel_nama = [], None

    if mapel_rekap_id:
        mapel_obj = MataPelajaran.query.get(mapel_rekap_id)
        mapel_nama = mapel_obj.nama_mapel if mapel_obj else None

        # Periode semester
        if semester == '2025-1':
            start_date, end_date = date(2025, 7, 1), date(2025, 12, 31)
        elif semester == '2025-2':
            start_date, end_date = date(2026, 1, 1), date(2026, 6, 30)
        else:
            start_date, end_date = date(2025, 7, 1), date(2026, 6, 30)

        rekap_results = (
            db.session.query(
                Siswa.nama,
                func.sum(case((Absensi.status == 'Hadir', 1), else_=0)).label('hadir'),
                func.sum(case((Absensi.status == 'Tidak Hadir', 1), else_=0)).label('alfa'),
                func.sum(case((Absensi.status == 'Izin', 1), else_=0)).label('izin'),
                func.sum(case((Absensi.status == 'Sakit', 1), else_=0)).label('sakit')
            )
            .join(Siswa, Siswa.id == Absensi.siswa_id)
            .filter(
                Absensi.mata_pelajaran_id == mapel_rekap_id,
                Absensi.tanggal.between(start_date, end_date)
            )
            .group_by(Siswa.id)
            .order_by(Siswa.nama)
            .all()
        )

    semester_list = ['2025-1', '2025-2']

    return render_template(
        'absensi.html',
        siswa=siswa_list,
        jurusan_list=jurusan_list,
        mapel_list=mapel_list,
        selected_kelas=kelas,
        selected_jurusan=jurusan_selected,
        selected_mapel=mapel_selected,
        rekap_results=rekap_results,
        mapel_nama=mapel_nama,
        selected_semester=semester,
        semester_list=semester_list
    )


# ==================================================
# Fungsi Pesan WhatsApp
# ==================================================
def pesan_template(status_kode, siswa, mapel_nama):
    teks = {
        "H": f"""Assalamu'alaikum Bapak/Ibu {siswa.nama_ortu},

Siswa/i *{siswa.nama}* hadir di pelajaran *{mapel_nama}* hari ini. Terima kasih atas perhatiannya 🙏""",

        "A": f"""Assalamu'alaikum Bapak/Ibu {siswa.nama_ortu},

Siswa/i *{siswa.nama}* hari ini *TIDAK HADIR* di pelajaran *{mapel_nama}* tanpa keterangan. Mohon konfirmasinya 🙏""",

        "S": f"""Assalamu'alaikum Bapak/Ibu {siswa.nama_ortu},

Siswa/i *{siswa.nama}* tidak hadir karena *Sakit* di pelajaran *{mapel_nama}*. Semoga cepat sembuh 🙏""",

        "I": f"""Assalamu'alaikum Bapak/Ibu {siswa.nama_ortu},

Siswa/i *{siswa.nama}* tidak hadir karena *Izin* di pelajaran *{mapel_nama}*. Terima kasih telah memberi kabar 🙏"""
    }
    return teks.get(status_kode)


# ==================================================
# Simpan Absensi
# ==================================================
@absensi_bp.route('/submit', methods=['POST'])
@login_required
def submit_absen():
    guru_id = current_user.id
    tanggal_wib = datetime.now(WIB).date()
    mapel_id = request.form.get('mapel')

    if not mapel_id or not mapel_id.isdigit():
        flash("❌ Pilih mata pelajaran terlebih dahulu!", "danger")
        return redirect(url_for('absensi.absen_page'))

    mapel_id = int(mapel_id)
    mapel_obj = MataPelajaran.query.get(mapel_id)
    mapel_nama = mapel_obj.nama_mapel if mapel_obj else "Tidak Diketahui"

    kode_status = {"H": "Hadir", "A": "Tidak Hadir", "I": "Izin", "S": "Sakit"}
    existing = {a.siswa_id for a in Absensi.query.filter_by(tanggal=tanggal_wib, mata_pelajaran_id=mapel_id).all()}

    total_kirim, total_gagal = 0, 0

    for key, val in request.form.items():
        if not key.startswith("status_"):
            continue

        siswa_id = int(key.split("_")[1])
        status = kode_status.get(val)
        if not status or siswa_id in existing:
            continue

        absen = Absensi(
            siswa_id=siswa_id,
            guru_id=guru_id,
            mata_pelajaran_id=mapel_id,
            tanggal=tanggal_wib,
            status=status
        )
        db.session.add(absen)

        siswa = Siswa.query.get(siswa_id)
        if siswa and siswa.no_ortu:
            pesan = pesan_template(val, siswa, mapel_nama)
            if pesan:
                try:
                    r = requests.post(
                        "https://api.fonnte.com/send",
                        headers={"Authorization": FONNTE_TOKEN},
                        data={"target": siswa.no_ortu, "message": pesan},
                        timeout=10
                    )
                    result = r.json() if r.headers.get("Content-Type", "").startswith("application/json") else {}
                    if r.status_code == 200 and result.get("status") == True:
                        total_kirim += 1
                    else:
                        total_gagal += 1
                        print(f"Gagal kirim WA ke {siswa.nama}: {r.text}")
                except Exception as e:
                    total_gagal += 1
                    print(f"Error kirim ke {siswa.nama}: {e}")

    db.session.commit()

    # Kirim hasil via query string agar bisa muncul popup
    return redirect(url_for('absensi.absen_page', sent=total_kirim, failed=total_gagal))



# ==================================================
# Rekap Absensi Harian JSON
# ==================================================
@absensi_bp.route('/rekap', methods=['GET'])
@login_required
def rekap_absensi_harian():
    today = date.today()
    data = {
        'hadir': Absensi.query.filter_by(tanggal=today, status='Hadir').count(),
        'sakit': Absensi.query.filter_by(tanggal=today, status='Sakit').count(),
        'izin': Absensi.query.filter_by(tanggal=today, status='Izin').count(),
        'alfa': Absensi.query.filter_by(tanggal=today, status='Tidak Hadir').count(),
    }
    return jsonify(data)


# ==================================================
# Rekap Absensi ke PDF
# ==================================================
@absensi_bp.route('/rekap/pdf', methods=['GET'])
@login_required
def rekap_absensi_pdf():
    kelas = request.args.get('kelas')
    jurusan = request.args.get('jurusan')
    mapel_id = request.args.get('mapel')

    siswa_query = Siswa.query
    if kelas:
        siswa_query = siswa_query.filter_by(kelas=kelas)
    if jurusan:
        siswa_query = siswa_query.filter_by(jurusan=jurusan)
    if mapel_id and mapel_id.isdigit():
        siswa_query = siswa_query.filter_by(mapel_id=int(mapel_id))

    siswa_list = siswa_query.order_by(Siswa.nama.asc()).all()

    mapel_nama = ""
    if mapel_id and mapel_id.isdigit():
        mapel_obj = MataPelajaran.query.get(mapel_id)
        mapel_nama = mapel_obj.nama_mapel if mapel_obj else ""

    # Data rekap
    rekap_results = (
        db.session.query(
            Siswa.id,
            func.sum(case((Absensi.status == 'Hadir', 1), else_=0)).label('hadir'),
            func.sum(case((Absensi.status == 'Tidak Hadir', 1), else_=0)).label('alfa'),
            func.sum(case((Absensi.status == 'Izin', 1), else_=0)).label('izin'),
            func.sum(case((Absensi.status == 'Sakit', 1), else_=0)).label('sakit')
        )
        .join(Siswa, Siswa.id == Absensi.siswa_id)
        .group_by(Siswa.id)
        .all()
    )
    rekap_dict = {r.id: r for r in rekap_results}

    # === PDF ===
    buffer = BytesIO()
    doc = SimpleDocTemplate(buffer, pagesize=A4, rightMargin=40, leftMargin=40, topMargin=70, bottomMargin=40)
    elements = []

    styles = getSampleStyleSheet()
    header_style = ParagraphStyle('header', parent=styles['Heading1'], fontSize=16, alignment=1)

    # Kop surat
    logo1, logo2 = "static/logo.png", "static/logo_pendidikan.png"
    try:
        img1 = Image(logo1, width=60, height=60)
    except:
        img1 = Paragraph("", styles['Normal'])
    try:
        img2 = Image(logo2, width=60, height=60)
    except:
        img2 = Paragraph("", styles['Normal'])

    header = [[img1, Paragraph(f"<b>SMK MULIA BUANA<br/>Rekap Absensi Pelajaran: {mapel_nama}<br/>Kelas {kelas or 'Semua'} {jurusan or ''}</b>", header_style), img2]]
    header_table = PlatypusTable(header, colWidths=[60, 360, 60])
    header_table.setStyle(TableStyle([
        ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
        ('ALIGN', (1, 0), (1, 0), 'CENTER'),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 10)
    ]))
    elements.append(header_table)
    elements.append(Spacer(1, 20))

    # Isi tabel
    data = [["No", "Nama", "Hadir", "Alfa", "Izin", "Sakit"]]
    for idx, s in enumerate(siswa_list, 1):
        r = rekap_dict.get(s.id)
        data.append([
            idx,
            s.nama,
            r.hadir if r else 0,
            r.alfa if r else 0,
            r.izin if r else 0,
            r.sakit if r else 0
        ])

    table = Table(data, colWidths=[30, 200, 50, 50, 50, 50])
    table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor("#007bff")),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.white),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
        ('GRID', (0, 0), (-1, -1), 0.4, colors.grey),
    ]))
    elements.append(table)

    doc.build(elements)
    buffer.seek(0)
    return send_file(buffer, as_attachment=True, download_name="rekap_absensi.pdf", mimetype='application/pdf')
