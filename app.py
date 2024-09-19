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



@app.route('/', methods=['GET', 'POST'])
def home():
   if request.method == 'POST':
      title = "Analisis"
      id_produk = int(request.form['produk'])
      input_komentar = request.form['komentar']

      cur = mysql.connection.cursor()
      # cur.execute('SELECT * FROM komentar WHERE id_produk = %s', (id_produk,))
      cur.execute('SELECT * FROM komentar')
      dataset = cur.fetchall()
      cur.close()

      cur = mysql.connection.cursor()
      cur.execute('SELECT kata_positif, nilai FROM frasa_positif')
      positif_data = cur.fetchall()
      cur.close()

      cur = mysql.connection.cursor()
      cur.execute('SELECT kata_negatif, nilai FROM frasa_negatif')
      negatif_data = cur.fetchall()
      cur.close()

      phrase_score = {}
      for kata, bobot in positif_data:
         phrase_score[kata] = float(bobot)

      for kata, bobot in negatif_data:
         phrase_score[kata] = float(bobot)

      X_komen = []
      y_label = []

      for row in dataset:
         X_komen.append(preprocess_text(row[3]))
         y_label.append(row[4])
      
      vectorizer = TfidfVectorizer()
      vectorizer.fit(X_komen)

      preprocess_input = [preprocess_text(comment) for comment in input_komentar.split()]
      tf_input_komen = vectorizer.transform([' '.join(preprocess_input)])

      input_score = []
      # count preprocess input score using phrase_score
      for word in preprocess_input:
         score = phrase_score[word] if word in phrase_score else 0
         label = 'netral'
         if score > 0:
            label = 'positif'
         elif score < 0:
            label = 'negatif'
         else:
            label = 'netral'
         input_score.append([word, score, label])

      values, counts = np.unique(y_label, return_counts=True)
      print(f"RAW DATA: {values[0]}: {counts[0]} | {values[1]}: {counts[1]}")

      NEGATIVE_COUNT = 0
      POSITIVE_COUNT = 0
      MAX_COUNT = min(counts)

      X_train = []
      y_train = []

      for i in range(len(y_label)):
         X_train.append(X_komen[i])
         y_train.append(y_label[i])
         # if y_label[i] == 'negatif' and NEGATIVE_COUNT < MAX_COUNT:
         #    X_train.append(X_komen[i])
         #    y_train.append(y_label[i])
         #    NEGATIVE_COUNT += 1
         # elif y_label[i] == 'positif' and POSITIVE_COUNT < MAX_COUNT:
         #    X_train.append(X_komen[i])
         #    y_train.append(y_label[i])
         #    POSITIVE_COUNT += 1

      values, counts = np.unique(y_train, return_counts=True)
      print(f"FILTERED DATA: {values[0]}: {counts[0]} | {values[1]}: {counts[1]}")

      X_train = vectorizer.transform(X_train)
      model_svm = SVC(kernel='linear')
      model_svm.fit(X_train, y_train)

      # # Predict sentiment on the testing data
      y_pred = model_svm.predict(tf_input_komen)

      print(y_pred)
      return render_template('frontend/index.html',title=title, komentar=input_komentar, prediksi=y_pred, corpus=input_score)

   else:
      title = "Analisis"

      cur = mysql.connection.cursor()
      cur.execute('SELECT * FROM produk')
      produk = cur.fetchall()
      cur.close()

      return render_template('frontend/index.html', title=title, produk=produk)

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

 
# Preprocessing function
def preprocess_text(text):
    # Case Folding 
    # Lowercase
    text = text.lower()
    
    # Remove special characters and digits
    text = re.sub(r'\W', ' ', text)
    text = re.sub(r'\d+', '', text)
    
    # Tokenization
    words = text.split()
    
    #Filtering
    # Remove stopwords
    stop_words = set(stopwords.words('english'))
    words = [word for word in words if word not in stop_words]
    
    # Lemmatization
    lemmatizer = WordNetLemmatizer()
    words = [lemmatizer.lemmatize(word) for word in words]
    
    # Join the words back into a single string
    processed_text = ' '.join(words)
    
    return processed_text

# algoritma
@app.route('/algoritma')
def algoritma():
   if 'status' in session and session['status'] == "Login":
      title = 'Algoritma SVM'

      cur = mysql.connection.cursor()
      cur.execute('SELECT p.id_produk, k.kategori, p.produk FROM produk p JOIN kategori k ON p.id_kategori = k.id_kategori')
      produk = cur.fetchall()
      cur.close()

      return render_template('algoritma/index.html', title=title, produk=produk)
   else :
      title = 'Belom Login'
      return render_template('auth/login.html', values=title)

@app.route('/komentar_algoritma', methods=['POST'])
def komentar_algoritma():
   if 'status' in session and session['status'] == "Login":

      if request.method == 'POST':
         nama = request.form['nama']
         id_produk = int(request.form['produk'])

         title = nama
         id = id_produk
         cur = mysql.connection.cursor()
         cur.execute('SELECT * FROM komentar WHERE id_produk = %s', (id_produk,))
         data_komentar = cur.fetchall()
         cur.close()

         cur = mysql.connection.cursor()
         cur.execute('SELECT * FROM komentar WHERE id_produk = %s', (id_produk,))
         dataset = cur.fetchall()
         cur.close()
         

         usernames = []
         komentars = []

         for row in dataset:
            username = row[2]
            komentar = row[3]

            usernames.append(username)
            komentars.append(komentar)
         
         # Menerapkan preprocess_text pada setiap komentar
         komentars = [preprocess_text(comment) for comment in komentars]
         
         cur = mysql.connection.cursor()
         cur.execute('SELECT kata_positif, nilai FROM frasa_positif')
         positif_data = cur.fetchall()
         cur.close()

         cur = mysql.connection.cursor()
         cur.execute('SELECT kata_negatif, nilai FROM frasa_negatif')
         negatif_data = cur.fetchall()
         cur.close()

         positif = {}
         for kata, bobot in positif_data:
            positif[kata] = float(bobot)

         negatif = {}
         for kata, bobot in negatif_data:
            negatif[kata] = float(bobot)
        
         # Tokenisasi kalimat
         skor_sentimen_kalimat = []

         for kal in komentars:
            kata_kalimat = kal.split()
            # Menghitung skor sentimen kalimat untuk setiap kata
            skor_sentimen_kata = []
            for kata in kata_kalimat:
               if kata in positif:
                     skor_sentimen_kata.append(str(positif[kata]))
               elif kata in negatif:
                     skor_sentimen_kata.append(str(negatif[kata]))
               else:
                     skor_sentimen_kata.append("0")

            # Menghitung jumlah total sentimen dari semua kata dalam kalimat
            jumlah_total_sentimen = sum(map(float, skor_sentimen_kata))
            
            if jumlah_total_sentimen >= 0:
               label = "positif"
            else:
               label = "negatif"
               
            # Menyimpan hasil sentimen kalimat dan label
            # skor_sentimen_kalimat.append((kal, skor_sentimen_kata, jumlah_total_sentimen, label))
            skor_sentimen_kalimat.append((kal, label))
         # menambahkan username pada komentar yang sudah di labelin 
         for i in range(len(skor_sentimen_kalimat)):
               skor_sentimen_kalimat[i] = (usernames[i],) + skor_sentimen_kalimat[i]

         pelabelan = skor_sentimen_kalimat
         pengguna = []
         komen = []
         label = []


         for row in skor_sentimen_kalimat:
            pengguna.append(row[0])
            komen.append(row[1])
            label.append(row[2])
         
         text_bersih = [pengguna, komen]

         vectorizer = TfidfVectorizer(max_features=5000)
         komen = vectorizer.fit_transform(komen)

         text_nilai = [pengguna, komen, label]

         train_size = int(0.8 * komen.shape[0])

         # Bagi data latih dan data uji
         
         z_train = pengguna[:train_size]
         X_train = komen[:train_size]
         y_train = label[:train_size]
         z_test = pengguna[train_size:]
         X_test = komen[train_size:]
         y_test = label[train_size:]

         data_latih = [z_train, X_train, y_train]
         data_uji = [z_test, X_test, y_test]

         
         model_svm = SVC(kernel='linear', C=1)
         model_svm.fit(X_train, y_train)

         # # Predict sentiment on the testing data
         y_pred = model_svm.predict(X_test)


         data_prediksi = [z_test, X_test, y_test, y_pred]

         label_encode = LabelEncoder()
         # numerik label 
         label_uji_encode = label_encode.fit_transform(y_test)
         prediksi_encode = label_encode.fit_transform(y_pred)

         print(label_uji_encode)
         print(prediksi_encode)
         # evaluasi
         akurasi = accuracy_score(label_uji_encode, prediksi_encode)
         presisi = precision_score(label_uji_encode, prediksi_encode)
         recall = recall_score(label_uji_encode, prediksi_encode)
         f1 = f1_score(label_uji_encode, prediksi_encode)

         print(akurasi)

         return render_template('algoritma/komentar.html',
                              title=title,
                              akurasi=akurasi,
                              presisi=presisi,
                              recall=recall,
                              f1=f1,
                              data_prediksi=data_prediksi,
                              data_latih=data_latih,
                              data_uji=data_uji, 
                              data_komentar=data_komentar,
                              text_nilai=text_nilai,
                              pelabelan=pelabelan
                              )

   else :   
      title = 'Belom Login'
      return render_template('auth/login.html', values=title)

if __name__ == '__main__':
   app.run(debug=True)
