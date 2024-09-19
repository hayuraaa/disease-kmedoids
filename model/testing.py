 # Daftar kata positif beserta bobot sentimennya
positif = {'bener': 0.1, 'sesuai': 0.1}

# Daftar kata negatif beserta bobot sentimennya
negatif = {'bingung': -0.1, 'labil': -0.1}

# Kalimat yang akan dianalisis
kalimat = ['bener bgt ak lg labil pilih diantara ini dan akhrnya ak co make sesuai kondisi kulit mukaku', 'pa bgt ada vidio ini lg bingung pilih produk ini']

# Tokenisasi kalimat
skor_sentimen_kalimat = []

for kal in kalimat:
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
    
    if jumlah_total_sentimen > 0:
        label = "positif"
    else:
        label = "negatif"
        
    # Menyimpan hasil sentimen kalimat dan label
    skor_sentimen_kalimat.append((kal, skor_sentimen_kata, jumlah_total_sentimen, label))

# Menampilkan hasil sentimen untuk setiap kalimat
for kalimat, skor_kata, total_sentimen, label in skor_sentimen_kalimat:
    print("Kalimat:", kalimat)
    print("Hasil sentimen untuk setiap kata dalam kalimat:", skor_kata)
    print("Jumlah total sentimen:", total_sentimen)
    print("Label kalimat:", label)
    print()
