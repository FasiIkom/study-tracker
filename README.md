# Penjelasan step-by-step Pembuatan Aplikasi study-tracker
### Membuat Proyek Django Baru
1. Buat direktori baru bernama `study-tracker` dan nyalakan _virtual environment_ dengan menjalankan perintah berikut di CMD yang sudah berada di direktori `study-tracker`.
   
   `python -m venv env`
   
   `env\Scripts\activate`
2. Di direktori tersebut, buat file txt baru bernama `requirements.txt` yang berisi beberapa _dependencies_ berikut.
   ```
   django
   gunicorn
   whitenoise
   psycopg2-binary
   requests
   urllib3
   ```
3. Lakukan instalasi terhadap _dependencies_ tersebut dengan menjalankan perintah berikut di CMD.
   
   `pip install -r requirements.txt`
4. Buat proyek Django bernama `study-tracker` dengan menjalankan perintah berikut di CMD.

   `django-admin startproject study_tracker .`

   Proyek Django bernama `study_tracker` akan muncul di dalam direktori.

### Membuat Aplikasi `main`
1. Jalankan perintah berikut di CMD untuk membuat aplikasi baru.
   
   `python manage.py startapp main`
2. Daftarkan `main` ke dalam proyek dengan cara B]buka berkas `settings.py` dalam direktory `study-tracker`, lalu tambahkan `'main',` di dalam `INSTALLED_APPS`.
   ```
   INSTALLED_APPS = [
    ...,
    'main',
    ...
   ]
   ```
   
### Melakukan _routing_
1. Buka `urls.py` yang ada di dalam direktori `study_tracker`.
2. Pada bagian `import`, tambahkan baris berikut.

   ```
   ...
   from django.urls import path, include
   ...
   ```
3. Di dalam `urlpatterns` tambahkan baris berikut.

   ```
   urlpatterns = [
    ...
    path('', include('main.urls')),
    ...
   ]
   ```

### Membuat Model pada Aplikasi `main`
1. Buka berkas `models.py` pada aplikasi `main`, lalu isi dengan kode berikut.

   ```
   from django.db import models
   
   class Study(models.Model):
       name = models.CharField(max_length=255)
       date_added = models.DateField(auto_now_add=True)
       page = models.IntegerField()
       description = models.TextField()
   ```
2. Buat migrasi model dengan cara menjalankan perintah berikut di CMD.

   `python manage.py makemigrations`
   
   Lalu, jalankan perintah berikut untuk menerapkan migrasi.

   `python manage.py migrate`

### Membuat Fungsi pada `views.py`
1. Buka berkas `views.py` pada aplikasi `main`, kemudian tambahkan baris berikut pada bagian `import`.

   `from django.shortcuts import render`
2. Tambahkan fungsi `show_main` di bawah `import`.

   ```
   def show_main(request):
    context = {
        'name': 'Maul',
        'class': 'XII-Science-3',
        'subject': 'Biology',
        'start_date': '23 January 2023',
        'progress': '80' 
    }

    return render(request, "main.html", context)
   ```
### Melakukan _deployment_ ke PWS
(Belum dilakukan karena ada kendala teknis)

# Bagan Aplikasi Django

![Screenshot 2024-02-13 175909](https://github.com/FasiIkom/study-tracker/assets/158117087/627dbd25-7467-45df-be4c-302a208995e7)

# Pertanyaan
### Mengapa Kita Menggunakan _virtual environment_? Apakah Bisa Membuat Aplikasi Tanpa _virtual environment_?

- _virtual environment_ berfungsi untuk mengisolasi dependesi dan paket yang diperlukan untuk setiap proyek secara terpisah, sehingga dapat menghindari kemungkinan terjadinya konflik dependensi antar proyek.
-  Walaupun tanpa _virtual environment_, aplikasi tetap masih bisa berjalan. Hal ini dikarenakan _virtual environment_ bukanlah syarat utama suatu aplikasi bisa berjalan, melainkan hanya alat yang dapat digunakan untuk mengembangkan aplikasi, terutama untuk mencegah terjadinya konflik dependensi antar proyek.
### Apa Itu MVC, MVT, dan MVVM? Apa perbedaan dari ketiganya?
Ketiganya merupakan pola desain yang umum digunakan dalam pengembangan perangkat lunak. Perbedaan ketiganya adalah :
1. MVC (_model-view-controller_)
   Terdiri dari 3 unsur :
   - _model_ : Bagian yang berfungsi untuk menyiapkan, mengatur, memanipulasi, dan mengelola data, logika, serta batasan aplikasi lainnya yang ada di database.
   - _view_ : Bagian yang bertugas untuk menampilkan informasi dalam bentuk _Graphical User Interface_ (GUI).
   - _controller_ : Bagian yang menjembatani antara _model_ dan _view_, mengatur keduanya agar saling terhubung.
2. MVT (_model-view-template_)
   Terdiri dari 3 unsur :
   - _model_ : Bagian yang berfungsi untuk menyiapkan, mengatur, memanipulasi, dan mengelola data, logika, serta batasan aplikasi lainnya yang ada di database.
   - _view_ : Bagian yang bertugas untuk menampilkan informasi dalam bentuk _Graphical User Interface_ (GUI).
   - _template_ : Bagian yang menentukan bagian _user interface_.
3. MVVM (_model-view-viewmodel_)
   Terdiri dari 3 unsur :
   - _model_ : Bagian yang berfungsi untuk menyiapkan, mengatur, memanipulasi, dan mengelola data, logika, serta batasan aplikasi lainnya yang ada di database.
   - _view_ : Bagian yang bertugas untuk menampilkan informasi dalam bentuk _Graphical User Interface_ (GUI).
   - _viewmodel_ : Bagian yang berinteraksi langsung dengan _model_ dan menyajikan data untuk _view_.
