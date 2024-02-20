# Penjelasan step-by-step Pembuatan Aplikasi study-tracker
## Tugas 2
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

## Tugas 3
### Membuat input `form` untuk menambahkan objek model pada app sebelumnya.
1. Buat berkas baru pada direktori `main` bernama `forms.py` dan isi dengan kode berikut.
   ```
   from django.forms import ModelForm
   from main.models import Progress

   class ProgressForm(ModelForm):
       class Meta:
           model = Progress
           fields = ["subject", "start_Study", "progress", "catatan"]
   ```
2. Buka berkas `views.py` pada direktori `main`.
   Tambahkan beberapa import berikut.
   ```
   from main.forms import ProgressForm
   from main.models import Progress
   from django.shortcuts import redirect
   ```
   Tambahkan juga fungsi berikut.
   ```
   def create_progress(request):
    form = ProgressForm(request.POST or None)

    if form.is_valid() and request.method == "POST":
        form.save()
        return redirect('main:show_main')

    context = {'form': form}
    return render(request, "create_progress.html", context)
    ```
   Masih di berkas yang sama, update fungsi show_main menjadi seperti berikut ini.
   ```
   def show_main(request):
    books = Book.objects.all()

    context = {
        'name': 'Pak Bepe',
        'class': 'PBP A',
        'books': books
    }

    return render(request, "main.html", context)
    ```
3. Buka berkas `urls.py` pada direktori `main`.
   Tambahkan import berikut.
   ```
   from main.views import show_main, create_progress
   ```
   Tambahkan `path('create-progress', create_progress, name='create_progress'),` ke `urlpatterns`.
   ```
   urlpatterns = [
      ...
      path('create-progress', create_progress, name='create_progress'),
   ]
   ```
4. Pada direktori `main/templates`, buat berkas HTML baru bernama `create_progress.html` dan isilah dengan kode berikut ini.
   ```
   {% extends 'base.html' %} {% block content %}
   <h1>Add New Progress</h1>

   <form method="POST">
     {% csrf_token %}
     <table>
       {{ form.as_table }}
       <tr>
         <td></td>
         <td>
           <input type="submit" value="Add New Progress" />
         </td>
       </tr>
     </table>
   </form>

   {% endblock %}
   ```
5. Pada direktori `main/templates`, buka berkas `main.html` dan tambahkan kode di dalam bagian `{% block content %}`.
   ```
   <table>
     <tr>
       <th>Subject</th>
       <th>Start Study</th>
       <th>Progress (%)</th>
       <th>Catatan</th>
       <th>Date Added</th>
     </tr>

     {% comment %} Berikut cara memperlihatkan data produk di bawah baris ini
     {%endcomment %} {% for progres in progresses %}
     <tr>
       <td>{{progres.subject}}</td>
       <td>{{progres.start_Study}}</td>
       <td>{{progres.progress}}</td>
       <td>{{progres.catatan}}</td>
       <td>{{progres.date_added}}</td>
     </tr>
     {% endfor %}
   </table>

   <br />

   <a href="{% url 'main:create_progress' %}">
     <button>Add New Progress</button>
   </a>
   ```
### Menambahkan 4 fungsi `views` baru untuk melihat objek yang sudah ditambahkan dalam format XML, JSON, XML by ID, dan JSON by ID.
1. Buka `views.py` pada direktori `main` dan tambahkan import berikut.
   ```
   from django.http import HttpResponse
   from django.core import serializers
   ```
2. Untuk format XML, tambahkan fungsi berikut pada `views.py`.
   ```
   def show_xml(request):
       data = Progress.objects.all()
       return HttpResponse(serializers.serialize("xml", data), content_type="application/xml")
   ```
3. Untuk format JSON, tambahkan fungsi berikut pada `views.py`.
   ```
   def show_json(request):
       data = Progress.objects.all()
       return HttpResponse(serializers.serialize("json", data), content_type="application/json")
   ```
4. Untuk format XML by ID, tambahkan fungsi berikut pada `views.py`.
   ```
   def show_xml_by_id(request, id):
       data = Progress.objects.filter(pk=id)
       return HttpResponse(serializers.serialize("xml", data), content_type="application/xml")
   ```
5. Untuk format JSON by ID, tambahkan fungsi berikut pada `views.py`.
   ```
   def show_json_by_id(request, id):
      data = Progress.objects.filter(pk=id)
      return HttpResponse(serializers.serialize("json", data), content_type="application/json")
   ```
### Membuat routing URL untuk masing-masing `views` yang telah ditambahkan pada poin 2.
1. Buka berkas `urls.py`, lalu import 4 fungsi show yang telah kita buat.
   ```
   from main.views import show_main, create_progress, show_xml, show_json, show_xml_by_id, show_json_by_id
   ```
2. Tambahkan path untuk setiap fungsi di dalam `urlpatterns`.
   ```
   path('json/', show_json, name='show_json'),
   path('xml/', show_xml, name='show_xml'),
   path('xml/<int:id>/', show_xml_by_id, name='show_xml_by_id'),
   path('json/<int:id>/', show_json_by_id, name='show_json_by_id'),
   ```

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
### Apa perbedaan antara form `POST` dan form `GET` dalam Django?
Form `POST` digunakan oleh klien untuk mengirimkan data ke server, sedangkan form `GET` digunakan untuk mengambil data dari server.
### Apa perbedaan utama antara XML, JSON, dan HTML dalam konteks pengiriman data?
1. JSON (JavaScript Object Notation)
   - Secara sintaks, kode JSON identik dengan kode JavaScript, sehingga lebih mudah untuk dikonversi menjadi JavaScript.
   - JSON mereprentasikan data dalam bentuk _key-value_.
2. XML (eXtensible Markup Language)
   - Mempresentasikan data dalam bentuk hirearki, sehingga lebih mudah dibaca.
   - Digunakan untuk mengirimkan data.
3. HTML (HyperText Marukup Language)
   - Memiliki format yang mirip dengan XML.
   - Lebih umum digunakan untuk membuat struktur dan halaman web.
### Mengapa JSON sering digunakan dalam pertukaran data antara aplikasi web modern?
Karena JSON mudah dikonversi menjadi JavaScript, dan kebanyakan browser web menggunakan JavaScript sehingga lebih mudah untuk diproses oleh browser.

