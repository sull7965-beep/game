print("heloo")
print(123)

#gabungan teks dan angka
print("umur saya", 20)

#menganal variabel dan type data
#type data integer "bilangan bulat"
umur = 20 
print(umur)
#float = bilangan desimal
tinggi = 168.7
print(tinggi)
#string = teks atau kalimat
nama = "sulayman"
print(nama)
#bolean = true or flase
student = True
print(student)

#input dan output
nama = input("Masukan nama: ")
print(f"hallo {nama}")

#operasi Aritmatika (+-*:)(tambah, bagi, kurang, kali)
#cara 1
print(2 + 3)    #output hasil dari 2+3 = 5
print(6 - 4)      #pengurangan
print(1 * 5)      #Perkalian
print(2 / 2)

#Cara 2
a = 12 
b = 4
c = 2

print(a + b)    #output hasil dari variabel a + b
print(a - b) 
print(a * b) 
print(a / b) 
print(a % b) 

# cara 3 (input angka dari user)
a = int(input("masukan angka pertama: "))
b = int(input("masukan angka kedua: "))

print(a + b) 
print(a - b) 
print(a * b) 
print(a / b) 
print(a % b) 

#Perbandingan true dan fale

a = 5
b = 2
 
print(a == b)  #sama dengan  output False
print(a != b)  #tidak sama dengan   output true
print(a > b)   #lebih besar dari   output true
print(a < b)   #lebih kecil dari   output False
print(a >= b)  #lebih besar dari sama dengan  output true
print(a <= b)  #lebih besar dari sama dengan  output False


#operasi logika 

# AND '"JIKA SEMUA BENAR = TRUE"
a = 5
b = 10

print(a > 0 and b > 0) #TRUE
print(a < 0 and b < 0) #FALSE

# OR "SALAH SATU BENAR = TRUE" 
a = 5
b = 10

print(a > 0 or b < 0) #TRUE
print(a > 0 or b > 0) #FALSE

# NOT "KEBALIKAN (TRUE = FALSE)"
a = 5
b = 10

print(not(a < 0)) #TRUE
print(not(a > 0)) #FALSE

#STRING DASAR
teks = "abcdef"  # indexing "mengambil karakter sesuai urutan"

print(teks[0]) #a
print(teks[1]) #b

teks = "abcdef"  #slicing  " mengambil sebagian kata"

print(teks[0:4]) #abcd
print(teks[2:]) #cdef
print(teks[:3]) #abc

teks = "abcdef"  #len  "menghitung panjang string"

print(len(teks)) # output "6"

#  STRING METHOD
teks = "Belajar python"

print(teks.upper())  #mengubah teks menjadi huruf kapital
print(teks.lower())   #mengubah teks menjadi huruf kecil
print(teks.replace("python", "java"))  #mengubah salah satu teks yang diinginkan
print(teks.split()) #mengubah teks menjadi list

# LIST DASAR
siswa = ["agus", "udin", "jono"]
print(siswa)  # output ["agus", "udin", "jono"]

# mengaplikasikan "indeksing" dalam list # Mengambil salah satu siswa sesuai urutan
print(siswa[0])  # output = agus 
print(siswa[1])  # output = udin
print(siswa[2])  #output = jono

#mengupdate elemen atau mengantinya
siswa[0] = "ipin"
siswa[1] = "mail"
siswa[2] = "upin"
print(siswa)    # output ['ipin', 'mail', 'upin']

#list dapat menyimpan berbagai tipe data
campur = [1, 3.5, "kata", True]
print(campur)  #output  

 #LIST METODE

siswa = ["agus", "udin", "jono"]

siswa.append("mail")  #untuk menambahkan daftar list
print(siswa)   #output ["agus", "udin", "jono", "mail"]

siswa.insert(0, "upin") #menambahkan list dan mengatur list tersebut berada di posisi/index ke berapa
print(siswa)   #output ["upin", "agus", "udin", "jono", "mail"]

siswa.remove("agus") #untuk menghapus/menghilangkan data dari sebuah list
print(siswa)   #output ["upin", "udin", "jono", "mail"]

#TUPLE (sama seperti list tapi tidak bisa di otak atik alias sifatnya "IMMUTABLE" tidak bisa di ubah)

angka = (1, 2, 3, 4, 5) #perbedaan dengan list adalah list menggunakan kurung siku [] sedangkan tuple menggunakan kurung biasa ()
print(angka) #output (1, 2, 3, 4, 5)

#contoh ketika mau di ubah
# angka = (1, 2, 3, 4, 5) #TUPLE (read only) yang biasa di pake untuk data yang sifatnya tetap seperti titik koordinat/data yang ngak bisa di ubah
# angka[0] = 99 

# print(angka)  #output nya bakalan error karena sifatnya yang tidak bisa di ubah tadi

#APA ITU "SET" sama seperti list ,bedanya set hanya menyimpan data unik dan data nya ngak boleh ada yang duplikat

angka = {9, 8, 8, 7, 6, 11}
print(angka) #output {9, 8, 7, 6, 11} # karna ini set data yang duplikat atau sama maka salah satu yang terduplikat akan otomatis terhapus

#set juga bisa mengabungkan data list 
a = {1, 2, 3}
b = {3, 4, 5}
print(a | b) #output {1, 2, 3, 4, 5, 6} otomatis data akan tergabung

#SET "INTERSECTION" mengambil/mencari data yang sama
a = {1, 2, 3}
b = {3, 4, 5}
print(a & b) #output "3"

 #untuk mengecek keanggotaan dari set 
print(2 in a) #output "True" karna komputer akan cek apakah data 2 ada di set (a)
print(4 in a) #output "False" karena data (4) bukan dari data set (a)

#DICTIONARY DASAR ,kaya list tapi ini menngunakan pasangan anatara Q dan value
# nama adalah (Q) dan mail/17 adalah value
siswa = {
    "nama": "Mail",  
    "umur": 17,
    "kelas": "X"
}
print(siswa)

#cara untuk memanggil data "DICTIONARY"
print(siswa["nama"]) 

#cara menambahkan data "DICTIONARY"
siswa["nilai"] = 90
print(siswa)   #nanti otomatis data akan tertambah


#cara hapus data  "DICTIONARY"
del siswa["kelas"]
print(siswa)  #output otomatis data "kelas" akan terhapus

# "IF" "ELSE" agar program bisa berpikir dan mengambil keputusan
nilai = int(input("masukan niali: "))

if nilai >= 70:
   print("kamu lulus")    #jika nilai lebih dari 70 atau sama dengan maka muncul kamu lulus
else:
   print("kamu tidak lulus") #jika nilai kurang dari 70 maka tidak lulus

   #"ELIF" KONDISI 3 ATAU LEBIH 

   nilai = int(input("masukan kamu: "))

   if nilai >= 90:
    print("kamu dapat nilai A")  #jika nilai lebih dari atau sama dengan 90 maka "dapat nilai A"
   elif nilai >= 80:
    print("kamu dapat nilai B")  #jika lebih 80 dapat nilai B
   elif nilai >= 70:
    print("kamu dapat nilai C")  #jika lebih 70 dapat nilai C
   else:
    print("kamu dapat nilai D")   #jika jika tidak dapat nilai D

