from flask import Flask, redirect, request, render_template, url_for, session, flash
from flask_mysqldb import MySQL
from sklearn.svm import SVC
from sklearn.metrics import accuracy_score, precision_score, recall_score, f1_score, confusion_matrix
from sklearn.preprocessing import LabelEncoder 
import numpy as np
from sklearn.preprocessing import LabelEncoder
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.feature_extraction.text import TfidfVectorizer
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
app.config['MYSQL_DB'] = 'tbc-kmedoids'

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
         nama = request.form['nama']
         username = request.form['username']
         password = request.form['password']

         cur = mysql.connection.cursor()
         cur.execute("INSERT INTO users (nama, username, password) VALUES (%s, %s, %s)" ,(nama, username, password))
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
         id_user = request.form['id']
         nama = request.form['nama']
         username = request.form['username']
         password = request.form['password']

         cur = mysql.connection.cursor()
         cur.execute("UPDATE users SET nama = %s, username = %s, password = %s WHERE id_user = %s " ,(nama, username, password, id_user))
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
         inisial_jenis = request.form['inisial_jenis']

         cur = mysql.connection.cursor()
         cur.execute("INSERT INTO jenis_penyakit (nama_jenis, inisial_jenis) VALUES (%s, %s)" ,(nama_jenis, inisial_jenis))
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
         inisial_jenis = request.form['inisial_jenis']

         cur = mysql.connection.cursor()
         cur.execute("UPDATE jenis_penyakit SET nama_jenis = %s, inisial_jenis = %s  WHERE id_jenis = %s " ,(nama_jenis, inisial_jenis, id_jenis))
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
   
   
@app.route('/kecamatan/<int:id>')
def lihat_kecamatan(id):
   if 'status' in session and session['status'] == "Login":
      # Mendapatkan data jenis penyakit berdasarkan id
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

      return render_template('kecamatan/kecamatan.html', jenis_penyakit=jenis_penyakit, kecamatan=kecamatan_data, kriteria=kriteria)
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



if __name__ == '__main__':
   app.run(debug=True)
