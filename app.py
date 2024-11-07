from flask import Flask, redirect, request, render_template, url_for, session, flash
from flask_mysqldb import MySQL
import pymysql
from sklearn.svm import SVC
from sklearn.metrics import accuracy_score, precision_score, recall_score, f1_score, confusion_matrix
from sklearn.preprocessing import LabelEncoder 
from sklearn.preprocessing import StandardScaler
import numpy as np
import random
from math import sqrt
from sklearn.preprocessing import LabelEncoder
import pandas as pd
from sklearn.metrics import pairwise_distances_argmin_min
from sklearn.model_selection import train_test_split
from sklearn.feature_extraction.text import TfidfVectorizer
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import io
import base64
import re
import nltk
from nltk.corpus import stopwords
nltk.download('stopwords')
from nltk.stem import WordNetLemmatizer

app = Flask(__name__)

app.secret_key = "bebas"
app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = ''
app.config['MYSQL_DB'] = 'py-kmedoids'

# app.config['MYSQL_PASSWORD'] = ''
# app.config['MYSQL_DB'] = 'db_svm'

mysql = MySQL(app)


#-------Login---------#
@app.route('/', methods=['GET', 'POST'])
def home():
   
   return render_template('auth/login.html')

@app.route('/login', methods=['GET', 'POST'])
def login():

   if request.method == 'POST':
      username = request.form['username']
      password = request.form['password']

      cur = mysql.connection.cursor()
      cur.execute('SELECT * FROM users WHERE username=%s and password=%s', (username, password))
      user = cur.fetchone()

      if user:
         session['username'] = user[1]
         session['status'] = "Login"
         return redirect(url_for('dashboard'))
      else:
         flash("Username atau Password Anda Salah")

   return render_template('auth/login.html')
   
@app.route('/register', methods=['GET', 'POST'])
def register():
   title = 'Register'
   if request.method == "GET":
      return render_template('auth/register.html', values=title)
   else :
      nama = request.form['nama']
      username = request.form['username']
      password = request.form['password']

      cur = mysql.connection.cursor()
      cur.execute("INSERT INTO users (nama,username,password) VALUES (%s,%s,%s)", (nama, username, password))
      mysql.connection.commit()
      cur.close()
      return redirect(url_for('login'))
   
@app.route('/logout')
def logout():
    title = 'logout'
    session.clear()
    return render_template('auth/login.html', values=title)
#-------Login---------#   
   
@app.route('/dashboard')
def dashboard():
   if 'status' in session and session['status'] == "Login":
      title = 'Dashboard'

      cur = mysql.connection.cursor()
      cur.execute('SELECT * FROM kecamatan LIMIT 15')
      data = cur.fetchall()
      cur.close()

      cur = mysql.connection.cursor()
      cur.execute('SELECT * FROM jenis_penyakit')
      total = cur.fetchall()
      cur.close()

      cur = mysql.connection.cursor()
      cur.execute('SELECT * FROM users')
      users = cur.fetchall()
      cur.close()
      
      cur = mysql.connection.cursor()
      cur.execute('SELECT * FROM kriteria')
      kriteria = cur.fetchall()
      cur.close()

      data_total = len(total)
      data_users = len(users)
      data_kriteria = len(kriteria)

      return render_template('dashboard/index.html',data_users=data_users,data_total=data_total, title=title , data=data, data_kriteria=data_kriteria)
   else :
      title = 'Belom Login'
      return render_template('auth/login.html', values=title)


@app.route('/users')
def users():
   if 'status' in session and session['status'] == "Login":

      title = 'Users'
      cur = mysql.connection.cursor()
      cur.execute('SELECT * FROM users')
      users = cur.fetchall()
      cur.close()

      return render_template('users/index.html', title=title, users=users)
   else :
      title = 'Belom Login'
      return render_template('auth/login.html', values=title)

@app.route('/add_user', methods=['POST'])
def add_user():
   if 'status' in session and session['status'] == "Login":

      if request.method == 'POST':
         flash("Data Berhasil Ditambah")
         nama = request.form['nama_user']
         username = request.form['username']
         password = request.form['password']

         cur = mysql.connection.cursor()
         cur.execute("INSERT INTO users (nama_user, username, password) VALUES (%s, %s, %s)" ,(nama, username, password))
         mysql.connection.commit()

         return redirect(url_for('users'))
   else :
      title = 'Belom Login'
      return render_template('auth/login.html', values=title)

@app.route('/edit_user', methods=['POST', 'GET'])
def edit_user():
   if 'status' in session and session['status'] == "Login":
    
      if request.method == 'POST':
         
         flash("Data Berhasil Diedit")
         id_user = request.form['id_user']
         nama = request.form['nama_user']
         username = request.form['username']
         password = request.form['password']

         cur = mysql.connection.cursor()
         cur.execute("UPDATE users SET nama_user = %s, username = %s, password = %s WHERE id_user = %s " ,(nama, username, password, id_user))
         mysql.connection.commit()
         return redirect(url_for('users'))
   else :
      title = 'Belom Login'
      return render_template('auth/login.html', values=title)

@app.route('/delete_user/<string:id_data>', methods=['GET'])
def delete_user(id_data):
   if 'status' in session and session['status'] == "Login":
   
      flash("Data Berhasil Dihapus")

      cur = mysql.connection.cursor()
      cur.execute("DELETE FROM users WHERE id_user=%s" ,(id_data))
      mysql.connection.commit()
      return redirect(url_for('users'))
   else :
      title = 'Belom Login'
      return render_template('auth/login.html', values=title)
# end fungsi users 

@app.route('/jenis')
def jenis():
   if 'status' in session and session['status'] == "Login":

      title = 'Jenis Penyakit'
      cur = mysql.connection.cursor()
      cur.execute('SELECT * FROM jenis_penyakit')
      jenis = cur.fetchall()
      cur.close()

      return render_template('jenis/index.html', title=title, jenis=jenis)
   else :
      title = 'Belom Login'
      return render_template('auth/login.html', values=title)

@app.route('/add_jenis', methods=['POST'])
def add_jenis():
   if 'status' in session and session['status'] == "Login":

      if request.method == 'POST':
         flash("Data Berhasil Ditambah")
         nama_jenis = request.form['nama_jenis']
         inisial_jenis = request.form['inisial_tindak']

         cur = mysql.connection.cursor()
         cur.execute("INSERT INTO jenis_penyakit (nama_jenis, inisial_tindak) VALUES (%s, %s)" ,(nama_jenis, inisial_jenis))
         mysql.connection.commit()

         return redirect(url_for('jenis'))
   else :
      title = 'Belom Login'
      return render_template('auth/login.html', values=title)

@app.route('/edit_jenis', methods=['POST', 'GET'])
def edit_jenis():
   if 'status' in session and session['status'] == "Login":
    
      if request.method == 'POST':
         
         flash("Data Berhasil Diedit")
         id_jenis = request.form['id_jenis']
         nama_jenis = request.form['nama_jenis']
         inisial_jenis = request.form['inisial_tindak']

         cur = mysql.connection.cursor()
         cur.execute("UPDATE jenis_penyakit SET nama_jenis = %s, inisial_tindak = %s  WHERE id_jenis = %s " ,(nama_jenis, inisial_jenis, id_jenis))
         mysql.connection.commit()
         return redirect(url_for('jenis'))
   else :
      title = 'Belom Login'
      return render_template('auth/login.html', values=title)

@app.route('/delete_jenis/<string:id_jenis>', methods=['GET'])
def delete_jenis(id_jenis):
   if 'status' in session and session['status'] == "Login":
   
      flash("Data Berhasil Dihapus")

      cur = mysql.connection.cursor()
      cur.execute("DELETE FROM jenis_penyakit WHERE id_jenis=%s" ,(id_jenis))
      mysql.connection.commit()
      return redirect(url_for('jenis'))
   else :
      title = 'Belom Login'
      return render_template('auth/login.html', values=title)
# end fungsi jenis penyakit 

@app.route('/kriteria')
def kriteria():
   if 'status' in session and session['status'] == "Login":

      title = 'Data Tahun'
      cur = mysql.connection.cursor()
      cur.execute('SELECT * FROM kriteria')
      kriteria = cur.fetchall()
      cur.close()

      return render_template('kriteria/index.html', title=title, kriteria=kriteria)
   else :
      title = 'Belom Login'
      return render_template('auth/login.html', values=title)

@app.route('/add_kriteria', methods=['POST'])
def add_kriteria():
   if 'status' in session and session['status'] == "Login":

      if request.method == 'POST':
         flash("Data Berhasil Ditambah")
         nama_kriteria = request.form['nama_kriteria']
         inisial_kriteria = request.form['inisial_kriteria']

         cur = mysql.connection.cursor()
         cur.execute("INSERT INTO kriteria (nama_kriteria, inisial_kriteria) VALUES (%s, %s)" ,(nama_kriteria, inisial_kriteria))
         mysql.connection.commit()

         return redirect(url_for('kriteria'))
   else :
      title = 'Belom Login'
      return render_template('auth/login.html', values=title)

@app.route('/edit_kriteria', methods=['POST', 'GET'])
def edit_kriteria():
   if 'status' in session and session['status'] == "Login":
    
      if request.method == 'POST':
         
         flash("Data Berhasil Diedit")
         id_kriteria = request.form['id_kriteria']
         nama_kriteria = request.form['nama_kriteria']
         inisial_kriteria = request.form['inisial_kriteria']

         cur = mysql.connection.cursor()
         cur.execute("UPDATE kriteria SET nama_kriteria = %s, inisial_kriteria = %s  WHERE id_kriteria = %s " ,(nama_kriteria, inisial_kriteria, id_kriteria))
         mysql.connection.commit()
         return redirect(url_for('kriteria'))
   else :
      title = 'Belom Login'
      return render_template('auth/login.html', values=title)

@app.route('/delete_kriteria/<string:id_kriteria>', methods=['GET'])
def delete_kriteria(id_kriteria):
   if 'status' in session and session['status'] == "Login":
   
      flash("Data Berhasil Dihapus")

      cur = mysql.connection.cursor()
      cur.execute("DELETE FROM kriteria WHERE id_kriteria=%s" ,(id_kriteria))
      mysql.connection.commit()
      return redirect(url_for('kriteria'))
   else :
      title = 'Belom Login'
      return render_template('auth/login.html', values=title)
# end fungsi kriteria penyakit 

# Fungsi untuk melihat data jenis penyakit
@app.route('/data_penyakit')
def data_penyakit():
   if 'status' in session and session['status'] == "Login":
         
      title = 'Data Jenis Penyakit'
      cur = mysql.connection.cursor()
      cur.execute('SELECT * FROM jenis_penyakit')
      jenis_penyakit = cur.fetchall()
      cur.close()

      return render_template('kecamatan/jenis_penyakit.html', title=title, jenis_penyakit=jenis_penyakit)
   else:
      return redirect(url_for('auth/login.html'))
   
# Fungsi untuk melihat detail dataenis penyakit  
@app.route('/kecamatan/<int:id>')
def lihat_kecamatan(id):
   if 'status' in session and session['status'] == "Login":
      # Mendapatkan data jenis penyakit berdasarkan id
      title = 'Data Jenis Penyakit'
      cur = mysql.connection.cursor()
      cur.execute('SELECT * FROM jenis_penyakit WHERE id_jenis = %s', (id,))
      jenis_penyakit = cur.fetchone()

      # Mendapatkan daftar kecamatan berdasarkan jenis penyakit
      cur.execute('SELECT * FROM kecamatan WHERE id_jenis = %s', (id,))
      kecamatan = cur.fetchall()

      # Mendapatkan daftar kriteria
      cur.execute('SELECT * FROM kriteria')
      kriteria = cur.fetchall()
      
      kecamatan_data = []
      
      # Ambil bobot untuk setiap kecamatan
      for kec in kecamatan:
         cur.execute('SELECT * FROM data_bobot WHERE id_kecamatan = %s', (kec[0],))
         bobot = cur.fetchall()  # Asumsikan menghasilkan list dari tuple [(bobot1,), (bobot2,), ...]
         kecamatan_data.append((kec, bobot))

      cur.close()

      return render_template('kecamatan/kecamatan.html', title=title, jenis_penyakit=jenis_penyakit, kecamatan=kecamatan_data, kriteria=kriteria)
   else:
        return redirect(url_for('auth/login.html'))
   
# Menambahkan kecamatan dan nilai kriteria
@app.route('/add_kecamatan', methods=['POST'])
def add_kecamatan():
   if 'status' in session and session['status'] == "Login":
      nama_kecamatan = request.form['nama_kecamatan']
      inisial_kecamatan = request.form['inisial_kecamatan']
      id_jenis = request.form['id_jenis']

      cur = mysql.connection.cursor()
      cur.execute("INSERT INTO kecamatan (id_jenis, nama_kecamatan, inisial_kecamatan) VALUES (%s, %s, %s)", (id_jenis, nama_kecamatan, inisial_kecamatan))
      mysql.connection.commit()
      id_kecamatan = cur.lastrowid

      kriteria = request.form.getlist('kriteria[]')
      nilai = request.form.getlist('nilai[]')

      for i in range(len(kriteria)):
         cur.execute("INSERT INTO data_bobot (id_kecamatan, id_kriteria, bobot) VALUES (%s, %s, %s)", (id_kecamatan, kriteria[i], nilai[i]))
        
      mysql.connection.commit()
      cur.close()

      flash("Data kecamatan berhasil ditambahkan")
      return redirect(url_for('lihat_kecamatan', id=id_jenis))
   else:
      return redirect(url_for('auth/login.html'))
     
# Menghapus kecamatan
@app.route('/delete_kecamatan/<int:id_kecamatan>')
def delete_kecamatan(id_kecamatan):
   if 'status' in session and session['status'] == "Login":
      cur = mysql.connection.cursor()
      cur.execute("DELETE FROM kecamatan WHERE id_kecamatan = %s", (id_kecamatan,))
      cur.execute("DELETE FROM data_bobot WHERE id_kecamatan = %s", (id_kecamatan,))
      mysql.connection.commit()
      cur.close()

      flash("Data kecamatan berhasil dihapus")
      return redirect(request.referrer)
   else:
      return redirect(url_for('auth/login.html'))

# Mengedit Data kecamatan
@app.route('/edit_kecamatan', methods=['POST'])
def edit_kecamatan():
   if 'status' in session and session['status'] == "Login":
      # Ambil data dari form
      id_kecamatan = request.form['id_kecamatan']
      nama_kecamatan = request.form['nama_kecamatan']
      inisial_kecamatan = request.form.get('inisial_kecamatan', None)
      id_jenis = request.form['id_jenis']

      cur = mysql.connection.cursor()
      
      # Update data kecamatan
      cur.execute("UPDATE kecamatan SET nama_kecamatan = %s, inisial_kecamatan = %s WHERE id_kecamatan = %s", 
                  (nama_kecamatan, inisial_kecamatan, id_kecamatan))
      
      # Ambil data kriteria dan bobot baru
      kriteria_ids = request.form.getlist('kriteria_ids[]')
      nilai_bobot = request.form.getlist('nilai_bobot[]')

      # Validasi: Pastikan jumlah kriteria dan bobot sama
      if len(kriteria_ids) == len(nilai_bobot):
         for kriteria_id, bobot in zip(kriteria_ids, nilai_bobot):
            cur.execute("UPDATE data_bobot SET bobot = %s WHERE id_kecamatan = %s AND id_kriteria = %s", 
                        (bobot, id_kecamatan, kriteria_id))

      mysql.connection.commit()
      cur.close()

      flash("Data kecamatan berhasil diupdate")
      return redirect(url_for('lihat_kecamatan', id=id_jenis))
   else:
      return redirect(url_for('auth/login.html'))


#------------ELBOW------------#
def get_data_dummy():
    data = np.array([
    [17, 14, 12],
    [9, 11, 9],
    [7, 7, 6],
    [12, 14, 7],
    [6, 1, 7],
    [2, 2, 3],
    [1, 4, 5],
    [3, 4, 8],
    [2, 4, 6],
    [2, 1, 4],
    [5, 6, 6],
    [21, 20, 11],
    [2, 1, 1],
    [1, 2, 4],
    [1, 3, 4],
    [5, 5, 2],
    [4, 1, 5]
])


    # List of kecamatan names from your table
    kecamatan_names = [
        "Kota Juang", "Jeumpa", "Kuala", "Juli", "Jeunieb", "Peulimbang", 
        "Pandrah", "Peudada", "Samalanga", "Simpang Mamplam", "Jangka", 
        "Peusangan", "Peusangan Selatan", "Peusangan Siblah Krueng", 
        "Makmur", "Kuta Blang", "Gandapura"
    ]
    
    return data, kecamatan_names

data, kecamatan = get_data_dummy()

def hitung_jarak_euclidean(vektor1, vektor2):
    jarak = np.sum((np.array(vektor1) - np.array(vektor2)) ** 2)
    return np.sqrt(jarak)

def tentukan_medoid_terdekat(data, medoids):
    cluster_terdekat = []
    for row in data:
        jarak_min = float('inf')
        medoid_min = None
        for i, medoid in enumerate(medoids):
            jarak = hitung_jarak_euclidean(row, medoid)
            if jarak < jarak_min:
                jarak_min = jarak
                medoid_min = i
        cluster_terdekat.append(medoid_min)
    return np.array(cluster_terdekat)

def perbarui_medoid(data, cluster_terdekat, k):
    medoids = np.zeros((k, data.shape[1]))
    for i in range(k):
        # Pilih anggota dari cluster i
        anggota_cluster = data[cluster_terdekat == i]
        if len(anggota_cluster) == 0:
            continue
        
        # Hitung total jarak untuk setiap anggota dan pilih sebagai medoid baru
        jarak_terkecil = float('inf')
        medoid_baru = anggota_cluster[0]
        
        for calon_medoid in anggota_cluster:
            total_jarak = np.sum([hitung_jarak_euclidean(calon_medoid, anggota) for anggota in anggota_cluster])
            if total_jarak < jarak_terkecil:
                jarak_terkecil = total_jarak
                medoid_baru = calon_medoid
        
        medoids[i] = medoid_baru

    return medoids

def hitung_wcss(data, medoids, cluster_terdekat):
    wcss = 0
    for i, row in enumerate(data):
        medoid = medoids[cluster_terdekat[i]]
        wcss += np.sum((row - medoid) ** 2)
    return wcss

def metode_elbow(data, max_k=10):
    wcss_values = []
    
    for k in range(1, max_k + 1):
        # Inisialisasi medoid secara acak dari data
        medoids = data[np.random.choice(data.shape[0], k, replace=False)]
        cluster_terdekat = np.zeros(data.shape[0])

        for _ in range(100):  # Maksimal 100 iterasi
            cluster_terdekat = tentukan_medoid_terdekat(data, medoids)
            medoids_baru = perbarui_medoid(data, cluster_terdekat, k)
            if np.all(medoids == medoids_baru):
                break
            medoids = medoids_baru

        # Hitung WCSS
        wcss = hitung_wcss(data, medoids, cluster_terdekat)
        wcss_values.append(wcss)

    return wcss_values

@app.route('/elbow')
def elbow():
    # Dapatkan data dummy
    data, kecamatan = get_data_dummy()

    # Jalankan metode Elbow
    wcss_values = metode_elbow(data)

    # Kirim hasil ke template untuk ditampilkan
    return render_template('elbow/index.html', wcss_values=wcss_values)
 
@app.route('/pilih_clustering')
def pilih_clustering():
   if 'status' in session and session['status'] == "Login":
         
      title = 'Data Jenis Penyakit'
      cur = mysql.connection.cursor()
      cur.execute('SELECT * FROM jenis_penyakit')
      pilih_clustering = cur.fetchall()
      cur.close()

      return render_template('algoritma/pilih_clustering.html', title=title, jenis_penyakit=pilih_clustering)
   else:
      return redirect(url_for('auth/login.html'))
  
# K-Medoids clustering functions
def calculate_distance(point1, point2):
    return np.sqrt(np.sum((point1 - point2)**2))

def initialize_medoids(data, k, initial_medoids=None):
    if initial_medoids is not None and len(initial_medoids) == k:
        return np.array([data[i] for i in initial_medoids])
    return data[np.random.choice(data.shape[0], k, replace=False)]

def assign_points_to_medoids(data, medoids):
    distances = np.array([[calculate_distance(point, medoid) for medoid in medoids] for point in data])
    return np.argmin(distances, axis=1), distances

def calculate_total_cost(distances, labels):
    return sum(distances[i, labels[i]] for i in range(len(labels)))

def k_medoids(data, k, max_iterations=100, initial_medoids=None, second_medoids=None, third_medoids=None):
    medoids = initialize_medoids(data, k, initial_medoids)
    labels, distances = assign_points_to_medoids(data, medoids)
    current_cost = calculate_total_cost(distances, labels)
    
    iteration_history = [{
        'iteration': 0,
        'medoids': medoids.tolist(),
        'labels': labels.tolist(),
        'distances': distances.tolist(),
        'total_distance': current_cost,
        'change': 0
    }]
    
    for iteration in range(1, max_iterations + 1):
        if iteration == 1 and second_medoids is not None:
            new_medoids = initialize_medoids(data, k, second_medoids)
        elif iteration == 2 and third_medoids is not None:
            new_medoids = initialize_medoids(data, k, third_medoids)
        else:
            new_medoids = data[np.random.choice(data.shape[0], k, replace=False)]
        
        new_labels, new_distances = assign_points_to_medoids(data, new_medoids)
        new_cost = calculate_total_cost(new_distances, new_labels)
        
        change = new_cost - current_cost
        
        iteration_history.append({
            'iteration': iteration,
            'medoids': new_medoids.tolist(),
            'labels': new_labels.tolist(),
            'distances': new_distances.tolist(),
            'total_distance': new_cost,
            'change': change
        })
        
        if change >= 0:
            break
        
        medoids = new_medoids
        labels = new_labels
        distances = new_distances
        current_cost = new_cost
    
    last_iteration = iteration_history[-1]
    return np.array(last_iteration['medoids']), np.array(last_iteration['labels']), iteration_history

@app.route('/clustering/<int:id>', methods=['GET', 'POST'])
def clustering(id):
    if 'status' in session and session['status'] == "Login":
        cur = mysql.connection.cursor()
        cur.execute('SELECT * FROM jenis_penyakit WHERE id_jenis = %s', (id,))
        row = cur.fetchone()
        jenis_penyakit = {
            'id_jenis': row[0],
            'nama_jenis': row[1]
        }

        # Get the kecamatan data and corresponding kriteria
        cur.execute('''
         SELECT kecamatan.id_kecamatan, kecamatan.nama_kecamatan, 
               kecamatan.latitude, kecamatan.longitude,
               data_bobot.id_kriteria, data_bobot.bobot 
         FROM kecamatan 
         INNER JOIN data_bobot ON kecamatan.id_kecamatan = data_bobot.id_kecamatan 
         WHERE id_jenis = %s
         ''', (id,))
        bobot = cur.fetchall()

        nilai = {}
        kecamatan = {}
        coordinates = {}
        for row in bobot:
            id_kecamatan = row[0]
            if id_kecamatan not in nilai:
                nilai[id_kecamatan] = []
                kecamatan[id_kecamatan] = row[1]
                coordinates[id_kecamatan] = {
                    'latitude': row[2],
                    'longitude': row[3]
                }
            nilai[id_kecamatan].append(row[5])

        # Get kriteria
        cur.execute('SELECT * FROM kriteria')
        kriteria = cur.fetchall()
        cur.close()

        # Prepare data for clustering
        data = np.array(list(nilai.values()))
        kecamatan_names = list(kecamatan.values())
        kecamatan_coords = list(coordinates.values())
        
        medoids_map = {
            1: ([0, 1, 2], [4, 5, 6]), #stroke
            2: ([0, 4, 5], [10, 7, 6]), #hipertensi
            3: ([0, 1, 4], [6, 9, 11], [7, 8, 12]), #skizoprenia
            4: ([1, 3, 4], [10, 7, 6]), #dyspepsia
            5: ([0, 1, 2], [4, 5, 6]), #pneumonia
        }
        
        medoids_config = medoids_map.get(id, ([0, 1, 2], [4, 5, 6]))  # Default jika id tidak ditemukan
        initial_medoids = medoids_config[0]
        second_medoids = medoids_config[1] if len(medoids_config) > 1 else None
        third_medoids = medoids_config[2] if len(medoids_config) > 2 else None

        # Normalize the data
        normalized_data = (data - np.min(data, axis=0)) / (np.max(data, axis=0) - np.min(data, axis=0))

        k = 3  # Number of clusters
        medoids, labels, iteration_history = k_medoids(normalized_data, k, initial_medoids=initial_medoids, second_medoids=second_medoids, third_medoids=third_medoids)

        # Prepare the results for display
        clustering_results = []
        for i, (label, original, normalized) in enumerate(zip(labels, data, normalized_data)):
            clustering_results.append({
                'kecamatan': kecamatan_names[i],
                'cluster': label + 1,
                'original_data': original.tolist(),
                'normalized_data': normalized.tolist(),
                'latitude': kecamatan_coords[i]['latitude'],
                'longitude': kecamatan_coords[i]['longitude']
            })

        # Calculate total clusters
        total_clusters = {i: np.sum(labels == i) for i in range(k)}
        
        plt.figure(figsize=(8, 6))
        labels = ['Tinggi (C1)', 'Sedang (C2)', 'Rendah (C3)']
        sizes = [total_clusters[0], total_clusters[1], total_clusters[2]]
        colors = ['#FF6384', '#36A2EB', '#FFCE56']
        plt.pie(sizes, labels=labels, colors=colors, autopct='%1.1f%%', startangle=90)
        plt.axis('equal')
        plt.title('Jumlah Klaster')
        
        buf = io.BytesIO()
        plt.savefig(buf, format='png')
        buf.seek(0)

        pie_chart = base64.b64encode(buf.getvalue()).decode('utf-8')
    
        buf.close()
        plt.close()
         
        return render_template('algoritma/clustering.html',
                               title='K-Medoids Clustering',
                               jenis_penyakit=jenis_penyakit,
                               kriteria=kriteria,
                               clustering_results=clustering_results,
                               total_clusters=total_clusters,
                               iteration_history=iteration_history,
                               final_medoids=medoids.tolist(),
                               kecamatan_names=kecamatan_names,
                               pie_chart=pie_chart)

    return redirect(url_for('login'))
 
 
if __name__ == '__main__':
   app.run(debug=True)
