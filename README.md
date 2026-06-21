# UAS Struktur Data - Deteksi Penipuan Transaksi Keuangan

Repository ini berisi source code program simulasi deteksi penipuan transaksi keuangan menggunakan struktur data FIFO, LIFO, Tree, dan Graph.

## Identitas

Kelompok 5
Mata Kuliah: Struktur Data
Program Studi Informatika
Universitas Majalengka
Tahun: 2026

## Anggota Kelompok

1. Ahmad Gifariya - 2514101003
2. Andika Hikmawan - 2514101061
3. Dan Jago Anugrah - 2514101012
4. Fian Abdullah Mirza - 2514101005

## Deskripsi Program

Program ini dibuat menggunakan bahasa Python. Studi kasus yang digunakan adalah simulasi deteksi penipuan transaksi keuangan.

Struktur data yang digunakan:

* FIFO / Queue untuk memproses transaksi berdasarkan urutan masuk.
* LIFO / Stack untuk menyimpan transaksi mencurigakan sebagai daftar investigasi.
* Tree untuk mengklasifikasikan status transaksi.
* Graph untuk memodelkan hubungan antar akun dan mendeteksi siklus transaksi.

## File

* `fraud_std.py` : Source code utama program.
* `MAKALAH STD UAS.pdf` : Laporan tugas UAS Struktur Data.

## Cara Menjalankan Program

Pastikan Python sudah terinstall di komputer.

Jalankan program dengan perintah:

```bash
python fraud_std.py
```

## Output Program

Program akan menampilkan:

1. Data transaksi simulasi.
2. Queue transaksi berdasarkan prinsip FIFO.
3. Representasi graph menggunakan adjacency list.
4. Hasil deteksi siklus transaksi.
5. Hasil klasifikasi transaksi menjadi AMAN, MENCURIGAKAN, atau FRAUD.
6. Daftar investigasi transaksi menggunakan Stack.
7. Ringkasan hasil akhir.

## Struktur Data yang Digunakan

### FIFO / Queue

Queue digunakan untuk memproses transaksi sesuai urutan masuk.

### LIFO / Stack

Stack digunakan untuk menyimpan transaksi mencurigakan atau fraud.

### Tree

Tree digunakan sebagai pohon keputusan sederhana untuk menentukan status transaksi.

### Graph

Graph digunakan untuk memodelkan hubungan antar akun. Akun direpresentasikan sebagai vertex, transaksi sebagai edge, dan nominal transaksi sebagai weight.
