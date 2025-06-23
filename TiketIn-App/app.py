import hashlib
import random
import string
from flask import Flask, render_template, request, redirect, url_for, session, flash
import mysql.connector
from dotenv import load_dotenv
import os
import qrcode
from io import BytesIO
import base64
from werkzeug.utils import secure_filename
from datetime import datetime, timedelta
from flask_socketio import SocketIO, emit, send, join_room, leave_room

# Folder untuk menyimpan file upload
UPLOAD_FOLDER = 'static/uploads'
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif', 'webp'}

load_dotenv()
app = Flask(__name__)
app.secret_key = os.getenv('SECRET_KEY')
socketio = SocketIO(app)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

# Fungsi untuk memeriksa jenis file yang diizinkan
def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

# Konfigurasi Database (dari file .env)
db_config = {
    'host': os.getenv('DB_HOST'),
    'user': os.getenv('DB_USER'),
    'password': os.getenv('DB_PASSWORD'),
    'database': os.getenv('DB_NAME')
}

# Fungsi untuk menyimpan file dengan path yang benar
def save_image_file(file):
    # Mengamankan nama file
    filename = secure_filename(file.filename)
    # Gunakan os.path.join untuk memastikan path yang benar
    filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
    # Ganti backslash dengan forward slash untuk disimpan di database
    filepath_web = filepath.replace("\\", "/")
    file.save(filepath)
    return filepath_web  # Kembalikan path yang sesuai untuk disimpan di database

# Route untuk form pendaftaran
@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        email = request.form['email']
        no_telepon = request.form['no_telepon']
        nama = request.form['nama']
        password = request.form['password']

        # Koneksi ke database
        db = mysql.connector.connect(**db_config)
        cursor = db.cursor()

        # Enkripsi password menggunakan SHA-256
        password_hash = hashlib.sha256(password.encode()).hexdigest()

        # Insert data ke tabel pengguna
        query = "INSERT INTO pengguna (email_pengguna, no_telp_pengguna, nama_pengguna, password_pengguna) VALUES (%s, %s, %s, %s)"
        cursor.execute(query, (email, no_telepon, nama, password_hash))
        db.commit()

        cursor.close()
        db.close()

        # Redirect ke halaman sukses
        return redirect(url_for('success'))
    return render_template('register.html')

# Route untuk halaman sukses
@app.route('/success')
def success():
    return render_template('success.html')

# Route untuk form login
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']

        # Koneksi ke database
        db = mysql.connector.connect(**db_config)
        cursor = db.cursor(dictionary=True)

        # Cari pengguna berdasarkan email
        query = "SELECT * FROM pengguna WHERE email_pengguna = %s"
        cursor.execute(query, (email,))
        pengguna = cursor.fetchone()

        cursor.close()
        db.close()

        if pengguna:
            if pengguna['is_blocked']:
                flash('Akun Anda telah diblokir. Silakan hubungi admin.', 'error')
                return redirect(url_for('login'))
            
            # Verifikasi password (gunakan hashing sesuai implementasi Anda)
            if hashlib.sha256(password.encode()).hexdigest() == pengguna['password_pengguna']:
                # Set session pengguna
                session['id_pengguna'] = pengguna['id_pengguna']  # Mengakses id_pengguna
                session['nama_pengguna'] = pengguna['nama_pengguna'] # Mengakses nama_pengguna
                return redirect(url_for('home'))
            else:
                flash('Password salah.', 'error')
        else:
            flash('Email tidak ditemukan.', 'error')
        
        return redirect(url_for('login'))

    return render_template('login.html')


# Route untuk form login Admin
@app.route('/admin/login', methods=['GET', 'POST'])
def admin_login():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']

        # Koneksi ke database
        db = mysql.connector.connect(**db_config)
        cursor = db.cursor()

        # Enkripsi password menggunakan SHA-256
        password_hash = hashlib.sha256(password.encode()).hexdigest()

        # Query untuk mencari pengguna dengan email dan password yang sesuai
        query = "SELECT id_admin, nama_admin FROM admin WHERE email_admin = %s AND password_admin = %s"
        cursor.execute(query, (email, password_hash))
        admin = cursor.fetchone()

        cursor.close()
        db.close()

        # Jika pengguna ditemukan, redirect ke halaman beranda
        if admin:
            # Menyimpan data pengguna ke dalam session
            session['id_admin'] = admin[0]  # Mengakses id_admin
            session['nama_admin'] = admin[1]  # Mengakses nama_admin
            return redirect(url_for('dashboard'))
        # Jika pengguna tidak ditemukan, redirect kembali ke halaman login
        else:
            flash('Login gagal, email atau password salah', 'error')
            return redirect(url_for('admin_login'))
    return render_template('admin/login.html')


# Route untuk dashboard Admin
@app.route('/admin')
def dashboard():
    if 'id_admin' not in session:
        return redirect(url_for('admin_login'))
    else:
        return render_template('admin/dashboard.html')
    
# Route untuk halaman kelola pengguna (Admin)
@app.route('/admin/kelola-pengguna')
def kelola_pengguna():
    if 'id_admin' not in session:
        return redirect(url_for('admin_login'))
    else:
        # Koneksi ke database
        db = mysql.connector.connect(**db_config)
        cursor = db.cursor(dictionary=True)

        # Query untuk mengambil data pengguna
        query = "SELECT * FROM pengguna"
        cursor.execute(query)
        pengguna_list = cursor.fetchall()

        cursor.close()
        db.close()

        # Render halaman kelola pengguna dengan data pengguna
        return render_template('admin/kelola_pengguna.html', pengguna_list=pengguna_list)
    
# Route untuk menambah pengguna
@app.route('/admin/create-pengguna', methods=['POST'])
def create_pengguna():
    if 'id_admin' not in session:
        return redirect(url_for('admin_login'))
    
    nama_pengguna = request.form['nama_pengguna']
    email_pengguna = request.form['email_pengguna']
    no_telp_pengguna = request.form['no_telp_pengguna']
    password_pengguna = request.form['password_pengguna']

    # Enkripsi password menggunakan SHA-256
    password_hash = hashlib.sha256(password_pengguna.encode()).hexdigest()

    db = mysql.connector.connect(**db_config)
    cursor = db.cursor()

    query = "INSERT INTO pengguna (nama_pengguna, email_pengguna, no_telp_pengguna, password_pengguna) VALUES (%s, %s, %s, %s)"
    cursor.execute(query, (nama_pengguna, email_pengguna, no_telp_pengguna, password_hash))
    db.commit()
    
    cursor.close()
    db.close()

    # Redirect ke halaman kelola pengguna dengan pesan sukses
    flash('Pengguna berhasil ditambahkan', 'success')
    return redirect(url_for('kelola_pengguna'))

# Route untuk mengupdate pengguna
@app.route('/admin/update-pengguna', methods=['POST'])
def update_pengguna():
    if 'id_admin' not in session:
        return redirect(url_for('admin_login'))
    
    id_pengguna = request.form['id_pengguna']
    nama_pengguna = request.form['nama_pengguna']
    email_pengguna = request.form['email_pengguna']
    no_telp_pengguna = request.form['no_telp_pengguna']
    password_pengguna = request.form['password_pengguna']

    db = mysql.connector.connect(**db_config)
    cursor = db.cursor()

    if password_pengguna:  # Jika password diubah
        # Enkripsi password baru
        password_hash = hashlib.sha256(password_pengguna.encode()).hexdigest()
        query = "UPDATE pengguna SET nama_pengguna=%s, email_pengguna=%s, no_telp_pengguna=%s, password_pengguna=%s WHERE id_pengguna=%s"
        cursor.execute(query, (nama_pengguna, email_pengguna, no_telp_pengguna, password_hash, id_pengguna))
    else:  # Jika password tidak diubah
        query = "UPDATE pengguna SET nama_pengguna=%s, email_pengguna=%s, no_telp_pengguna=%s WHERE id_pengguna=%s"
        cursor.execute(query, (nama_pengguna, email_pengguna, no_telp_pengguna, id_pengguna))
    
    db.commit()
    
    cursor.close()
    db.close()

    # Redirect ke halaman kelola pengguna dengan pesan sukses
    flash('Pengguna berhasil diupdate', 'success')
    return redirect(url_for('kelola_pengguna'))

# Route untuk menghapus pengguna
@app.route('/admin/delete-pengguna/<int:id_pengguna>', methods=['POST'])
def delete_pengguna(id_pengguna):
    if 'id_admin' not in session:
        return redirect(url_for('admin_login'))
    
    db = mysql.connector.connect(**db_config)
    cursor = db.cursor()

    query = "DELETE FROM pengguna WHERE id_pengguna = %s"
    cursor.execute(query, (id_pengguna,))
    db.commit()
    
    cursor.close()
    db.close()

    # Redirect ke halaman kelola pengguna dengan pesan sukses
    flash('Pengguna berhasil dihapus', 'success')
    return redirect(url_for('kelola_pengguna'))

# Route untuk halaman kelola tiket (tempat wisata)
@app.route('/admin/kelola-tiket')
def kelola_tiket():
    if 'id_admin' not in session:
        return redirect(url_for('admin_login'))
    else:
        # Koneksi ke database
        db = mysql.connector.connect(**db_config)
        cursor = db.cursor(dictionary=True)

        # Query untuk mengambil data tempat wisata
        query = "SELECT * FROM tempat_wisata"
        cursor.execute(query)
        tempat_list = cursor.fetchall()

        cursor.close()
        db.close()

        # Render halaman kelola_tiket dengan data tempat wisata
        return render_template('admin/kelola_tiket.html', tempat_list=tempat_list)
    
# Route untuk menambah tempat wisata dengan file upload
@app.route('/admin/create-tempat', methods=['POST'])
def create_tempat():
    if 'id_admin' not in session:
        return redirect(url_for('admin_login'))

    nama_tempat = request.form['nama_tempat']
    lokasi_tempat = request.form['lokasi_tempat']
    harga_per_orang = request.form['harga_per_orang']
    deskripsi = request.form['deskripsi']
    rating = request.form['rating']
    jam_buka = request.form['jam_buka']
    hari_buka = request.form['hari_buka']
    
     # Proses file upload
    file = request.files['image']
    if file and allowed_file(file.filename):
        image_url = save_image_file(file)  # Simpan file dan dapatkan path-nya
    else:
        image_url = None
    
    # Simpan data ke database
    db = mysql.connector.connect(**db_config)
    cursor = db.cursor()

    query = """INSERT INTO tempat_wisata (nama_tempat, lokasi_tempat, harga_per_orang, deskripsi, rating, jam_buka, hari_buka, image)
               VALUES (%s, %s, %s, %s, %s, %s, %s, %s)"""
    cursor.execute(query, (nama_tempat, lokasi_tempat, harga_per_orang, deskripsi, rating, jam_buka, hari_buka, image_url))
    db.commit()

    cursor.close()
    db.close()

    return redirect(url_for('kelola_tiket'))

# Route untuk mengupdate tempat wisata dengan file upload
@app.route('/admin/update-tempat', methods=['POST'])
def update_tempat():
    if 'id_admin' not in session:
        return redirect(url_for('admin_login'))

    id_tempat = request.form['id_tempat']
    nama_tempat = request.form['nama_tempat']
    lokasi_tempat = request.form['lokasi_tempat']
    harga_per_orang = request.form['harga_per_orang']
    deskripsi = request.form['deskripsi']
    rating = request.form['rating']
    jam_buka = request.form['jam_buka']
    hari_buka = request.form['hari_buka']
    
    db = mysql.connector.connect(**db_config)
    cursor = db.cursor()

     # Proses file upload jika ada
    file = request.files.get('image')
    if file and allowed_file(file.filename):
        image_url = save_image_file(file)  # Simpan file dan dapatkan path-nya
    else:
        image_url = request.form['existing_image']  # Gunakan gambar yang sudah ada jika tidak ada yang di-upload

    # Update data tempat wisata
    query = """UPDATE tempat_wisata 
               SET nama_tempat=%s, lokasi_tempat=%s, harga_per_orang=%s, deskripsi=%s, rating=%s, jam_buka=%s, hari_buka=%s, image=%s 
               WHERE id_tempat=%s"""
    cursor.execute(query, (nama_tempat, lokasi_tempat, harga_per_orang, deskripsi, rating, jam_buka, hari_buka, image_url, id_tempat))
    db.commit()

    cursor.close()
    db.close()

    return redirect(url_for('kelola_tiket'))

# Route untuk menghapus tempat wisata
@app.route('/admin/delete-tempat/<int:id_tempat>', methods=['POST'])
def delete_tempat(id_tempat):
    if 'id_admin' not in session:
        return redirect(url_for('admin_login'))

    db = mysql.connector.connect(**db_config)
    cursor = db.cursor()

    query = "DELETE FROM tempat_wisata WHERE id_tempat = %s"
    cursor.execute(query, (id_tempat,))
    db.commit()

    cursor.close()
    db.close()

    return redirect(url_for('kelola_tiket'))

# Route untuk logout
@app.route('/logout')
def logout():
    
    session.pop('id_pengguna', None)
    session.pop('id_admin', None)
    return redirect(url_for('login'))

# Route untuk halaman beranda
@app.route('/')
def home():
    if 'id_pengguna' not in session:
        return redirect(url_for('login'))
    else:
         # Membuat koneksi ke database
        db = mysql.connector.connect(**db_config)
        cursor = db.cursor(dictionary=True)
        
        # Query untuk mengambil data tempat wisata
        query = "SELECT * FROM tempat_wisata"
        cursor.execute(query)
        wisata_list = cursor.fetchall()
        
        cursor.close()
        db.close()
        
        # Mengirim data tempat wisata ke template
        return render_template('index.html', wisata_list=wisata_list)
    
# Route untuk halaman detail
@app.route('/detail/<int:id_tempat>')
def detail(id_tempat):
    if 'id_pengguna' not in session:
        return redirect(url_for('login'))
    else:
        # Koneksi ke database
        db = mysql.connector.connect(**db_config)
        cursor = db.cursor(dictionary=True)

        # Query untuk mengambil detail tempat wisata berdasarkan id
        query = "SELECT * FROM tempat_wisata WHERE id_tempat = %s"
        cursor.execute(query, (id_tempat,))
        wisata = cursor.fetchone()

        cursor.close()
        db.close()

        # Render halaman detail dengan data dari database
        return render_template('detail.html', wisata=wisata)

# Route untuk form pemesanan tiket
@app.route('/pesan-tiket', methods=['POST'])
def pesan_tiket():
    # Ambil data dari form
    id_tempat = request.form['id_tempat']
    nama_pengguna = request.form['nama_pengguna']
    email_pengguna = request.form['email_pengguna']
    jumlah_orang = request.form['jumlah_orang']
    nama_tempat = request.form['nama_tempat']
    lokasi_tempat = request.form['lokasi_tempat']
    tgl_pemesanan = request.form['tgl_pemesanan']
    harga_per_orang = request.form['harga_per_orang']
    nomor_hp = request.form['nomor_hp']
    status = 'lunas'

    # Generate id_pemesanan (nomor acak 8 digit)
    id_pemesanan = ''.join(random.choices(string.digits, k=8))

    # Koneksi ke database
    db = mysql.connector.connect(**db_config)
    cursor = db.cursor()

    # Insert data ke tabel 'pemesanan'
    query = """
    INSERT INTO pemesanan (id_pemesanan, id_tempat, nama_pengguna, email_pengguna, jumlah_orang, nama_tempat, lokasi_tempat, tgl_pemesanan, harga_per_orang, nomor_hp, status)
    VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
    """
    cursor.execute(query, (id_pemesanan, id_tempat, nama_pengguna, email_pengguna, jumlah_orang, nama_tempat, lokasi_tempat, tgl_pemesanan, harga_per_orang, nomor_hp, status))
    db.commit()

    # Ambil id_pemesanan dari data yang baru saja dibuat
    id_pemesanan = cursor.lastrowid

    cursor.close()
    db.close()

    # Redirect ke halaman pembayaran dengan id_pemesanan
    return redirect(url_for('pembayaran', id_pemesanan=id_pemesanan))

# Route untuk halaman pembayaran
@app.route('/pembayaran/<int:id_pemesanan>')
def pembayaran(id_pemesanan):
    if 'id_pengguna' not in session:
        return redirect(url_for('login'))
    else:
         # Koneksi ke database
        db = mysql.connector.connect(**db_config)
        cursor = db.cursor(dictionary=True)

        # Query untuk mengambil detail pemesanan dan data tempat wisata berdasarkan id_pemesanan
        query = """
        SELECT pemesanan.*, tempat_wisata.*
        FROM pemesanan
        JOIN tempat_wisata ON pemesanan.id_tempat = tempat_wisata.id_tempat
        WHERE pemesanan.id_pemesanan = %s
        """
        cursor.execute(query, (id_pemesanan,))
        pemesanan = cursor.fetchone()

        cursor.close()
        db.close()

        # Render halaman pembayaran dengan data pemesanan dan tempat wisata
        return render_template('pembayaran.html', pemesanan=pemesanan)
    
# Route untuk cetak tiket
@app.route('/cetak-tiket/<int:id_pemesanan>')
def cetak_tiket(id_pemesanan):
    if 'id_pengguna' not in session:
        return redirect(url_for('login'))
    else:
        # Generate QR code dari id_pemesanan
        qr = qrcode.QRCode(
            version=1,
            error_correction=qrcode.constants.ERROR_CORRECT_L,
            box_size=10,
            border=4,
        )
        qr.add_data(f'Tiket ID: {{ pemesanan.id_pemesanan }}')
        qr.make(fit=True)
        img = qr.make_image(fill_color="black", back_color="white")
        buffer = BytesIO()
        img.save(buffer)
        qr_code = base64.b64encode(buffer.getvalue()).decode()

        # Koneksi ke database
        db = mysql.connector.connect(**db_config)
        cursor = db.cursor(dictionary=True)

        # Query untuk mengambil detail pemesanan dan data tempat wisata berdasarkan id_pemesanan
        query = """
        SELECT pemesanan.*, tempat_wisata.*
            FROM pemesanan
            JOIN tempat_wisata ON pemesanan.id_tempat = tempat_wisata.id_tempat
            WHERE pemesanan.id_pemesanan = %s
        """
        cursor.execute(query, (id_pemesanan,))
        data_pemesanan = cursor.fetchone()

        cursor.close()
        db.close()

        # Render halaman cetak tiket dengan data pemesanan dan QR code
        return render_template('cetak_tiket.html', pemesanan=data_pemesanan, qr_code=qr_code)
    
# Route untuk halaman riwayat pemesanan
@app.route('/admin/riwayat')
def riwayat_pemesanan():
    if 'id_admin' not in session:
        return redirect(url_for('admin_login'))
    
    # Koneksi ke database
    db = mysql.connector.connect(**db_config)
    cursor = db.cursor(dictionary=True)

    # Query untuk mengambil data pemesanan
    query = "SELECT id_pemesanan, nama_pengguna, tgl_pemesanan, status FROM pemesanan"
    cursor.execute(query)
    pemesanan_list = cursor.fetchall()

    cursor.close()
    db.close()

    # Render template riwayat.html dengan data pemesanan
    return render_template('admin/riwayat.html', pemesanan_list=pemesanan_list)

# Route untuk halaman detail pemesanan
@app.route('/admin/laporan-admin', methods=['GET', 'POST'])
def laporan_admin():
    if 'id_admin' not in session:
        return redirect(url_for('admin_login'))

    # Default ke laporan bulanan
    filter_waktu = request.form.get('filter_waktu', 'bulanan')

    # Hitung tanggal awal dan akhir berdasarkan filter waktu
    now = datetime.now()
    if filter_waktu == 'harian':
        start_date = now.replace(hour=0, minute=0, second=0, microsecond=0)
        end_date = now
    elif filter_waktu == 'mingguan':
        start_date = now - timedelta(days=now.weekday())
        end_date = now
    else:  # bulanan
        start_date = now.replace(day=1, hour=0, minute=0, second=0, microsecond=0)
        end_date = now

    # Koneksi ke database
    db = mysql.connector.connect(**db_config)
    cursor = db.cursor(dictionary=True)

    # Hitung jumlah pemesanan
    query_pemesanan = "SELECT COUNT(*) as total_pemesanan FROM pemesanan WHERE tgl_pemesanan BETWEEN %s AND %s"
    cursor.execute(query_pemesanan, (start_date, end_date))
    jumlah_pemesanan = cursor.fetchone()['total_pemesanan']

    # Hitung pendapatan
    query_pendapatan = """
    SELECT SUM(harga_per_orang * jumlah_orang + 5000) as total_pendapatan 
    FROM pemesanan 
    WHERE tgl_pemesanan BETWEEN %s AND %s
    """
    cursor.execute(query_pendapatan, (start_date, end_date))
    total_pendapatan = cursor.fetchone()['total_pendapatan'] or 0

    # Hitung jumlah pengguna aktif
    query_pengguna_aktif = "SELECT COUNT(*) as total_pengguna FROM pengguna"
    cursor.execute(query_pengguna_aktif)
    jumlah_pengguna_aktif = cursor.fetchone()['total_pengguna']

    # Hitung tiket terjual per tempat wisata
    query_tiket_terjual = """
    SELECT t.nama_tempat, COUNT(p.id_tempat) as tiket_terjual
    FROM pemesanan p
    JOIN tempat_wisata t ON p.id_tempat = t.id_tempat
    WHERE p.tgl_pemesanan BETWEEN %s AND %s
    GROUP BY p.id_tempat
    """
    cursor.execute(query_tiket_terjual, (start_date, end_date))
    tiket_terjual = cursor.fetchall()

    cursor.close()
    db.close()

    # Render template laporan dengan data statistik
    return render_template('admin/laporan-admin.html', 
                           jumlah_pemesanan=jumlah_pemesanan,
                           total_pendapatan=total_pendapatan,
                           jumlah_pengguna_aktif=jumlah_pengguna_aktif,
                           tiket_terjual=tiket_terjual,
                           filter_waktu=filter_waktu)

# Route untuk halaman laporan akun pengguna
@app.route('/admin/laporan-akun', methods=['GET', 'POST'])
def laporan_akun():
    if 'id_admin' not in session:
        return redirect(url_for('admin_login'))

    # Koneksi ke database
    db = mysql.connector.connect(**db_config)
    cursor = db.cursor(dictionary=True)

    # Query untuk mendapatkan data semua pengguna
    query = "SELECT id_pengguna, nama_pengguna, email_pengguna, is_blocked FROM pengguna"
    cursor.execute(query)
    pengguna_list = cursor.fetchall()

    cursor.close()
    db.close()

    # Render halaman laporan-akun.html dengan data pengguna
    return render_template('admin/laporan-akun.html', pengguna_list=pengguna_list)

# Route untuk memblokir atau membuka blokir pengguna
@app.route('/admin/update-blokir/<int:id_pengguna>', methods=['POST'])
def update_blokir(id_pengguna):
    if 'id_admin' not in session:
        return redirect(url_for('admin_login'))

    # Ambil status blokir dari form
    is_blocked = request.form.get('is_blocked') == 'on'

    # Koneksi ke database
    db = mysql.connector.connect(**db_config)
    cursor = db.cursor()

    # Update status blokir pengguna
    query = "UPDATE pengguna SET is_blocked = %s WHERE id_pengguna = %s"
    cursor.execute(query, (is_blocked, id_pengguna))
    db.commit()

    cursor.close()
    db.close()

    # Redirect kembali ke halaman laporan akun
    return redirect(url_for('laporan_akun'))


# Route untuk halaman Customer Support (Admin)
@app.route('/admin/cs')
def customer_support():
    if 'id_admin' not in session:
        return redirect(url_for('admin_login'))

    # Render halaman cs.html
    return render_template('admin/cs.html')

# Route untuk halaman chat pengguna
@app.route('/chat')
def chat():
    return render_template('chat.html')

# Handling WebSocket connection
@socketio.on('join')
def handle_join(data):
    room = data['room']
    join_room(room)
    send(f"{data['username']} has entered the room.", room=room)

@socketio.on('leave')
def handle_leave(data):
    room = data['room']
    leave_room(room)
    send(f"{data['username']} has left the room.", room=room)

@socketio.on('message')
def handle_message(data):
    room = data['room']
    message = data['message']
    username = data['username']
    send(f"{username}: {message}", room=room)

# Jalankan SocketIO
if __name__ == '__main__':
    socketio.run(app, debug=True)