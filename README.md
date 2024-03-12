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
### Membuat input `form` untuk menambahkan objek model pada app sebelumnya
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
    progresses = Progress.objects.all()

    context = {
        'name': 'Pak Bepe',
        'class': 'PBP A',
        'progresses': progresses
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
### Membuat routing URL untuk masing-masing `views` yang telah ditambahkan pada poin 2
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

## Tugas 4
### Membuat Fungsi Registrasi, Login, dan Logout
1. Buka `views.py` pada direktori `main`. Tambahkan beberapa import berikut.
   ```
   #register
   from django.shortcuts import redirect
   from django.contrib.auth.forms import UserCreationForm
   from django.contrib import messages

   #login dan logout
   from django.contrib.auth import authenticate, login, logout
   ```
   Masih di berkas yang sama, buat fungsi `register`, `login`, dan `logout`.
   Fungsi register
   ```
   def register(request):
    form = UserCreationForm()

    if request.method == "POST":
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Your account has been successfully created!')
            return redirect('main:login')
    context = {'form':form}
    return render(request, 'register.html', context)
   ```
   Fungsi login
   ```
   def login_user(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('main:show_main')
        else:
            messages.info(request, 'Sorry, incorrect username or password. Please try again.')
    context = {}
    return render(request, 'login.html', context)
   ```
   Fungsi logout
   ```
   def logout_user(request):
    logout(request)
    return redirect('main:login')
   ```
2. Buat berkas baru bernama `register.html` di direktori `templates`. Isilah dengan teks berikut.
   ```
   {% extends 'base.html' %} 

   {% block meta %}
   <title>Register</title>
   {% endblock meta %} 

   {% block content %}

   <div class="login">
     <h1>Register</h1>

     <form method="POST">
       {% csrf_token %}
       <table>
         {{ form.as_table }}
         <tr>
           <td></td>
           <td><input type="submit" name="submit" value="Daftar" /></td>
         </tr>
       </table>
     </form>

     {% if messages %}
     <ul>
       {% for message in messages %}
       <li>{{ message }}</li>
       {% endfor %}
     </ul>
     {% endif %}
   </div>

   {% endblock content %}
   ```
3. Buat berkas baru bernama `login.html` di direktori `templates`. Isilah dengan teks berikut.
   ```
   {% extends 'base.html' %}

   {% block meta %}
   <title>Login</title>
   {% endblock meta %} 

   {% block content %}
   <div class="login">
     <h1>Login</h1>

     <form method="POST" action="">
       {% csrf_token %}
       <table>
         <tr>
           <td>Username:</td>
           <td>
             <input
               type="text"
               name="username"
               placeholder="Username"
               class="form-control"
             />
           </td>
         </tr>

         <tr>
           <td>Password:</td>
           <td>
             <input
               type="password"
               name="password"
               placeholder="Password"
               class="form-control"
             />
           </td>
         </tr>

         <tr>
           <td></td>
           <td><input class="btn login_btn" type="submit" value="Login" /></td>
         </tr>
       </table>
     </form>

     {% if messages %}
     <ul>
       {% for message in messages %}
       <li>{{ message }}</li>
       {% endfor %}
     </ul>
     {% endif %} Don't have an account yet?
     <a href="{% url 'main:register' %}">Register Now</a>
   </div>

   {% endblock content %}
   ```
4. Buat tombol logout dengan cara tambahkan teks berikut di berkas `main.html` pada direktori `templates` setelah bagian `add new progress`.
   ```
   <a href="{% url 'main:logout' %}">
      <button>Logout</button>
   </a>
   ```
5. Lakukan routing. Pada `urls.py` di direktori `main`, tambahkan import fungsi yang telah kita buat.
   ```
   from main.views import register, login_user, logout_user
   ```
   Masih di berkas yang sama, tambahkan beberapa baris berikut di urlpatterns.
   ```
   path('register/', register, name='register'),
   path('login/', login_user, name='login'),
   path('logout/', logout_user, name='logout'),
   ```
### Membuat Dua Akun dengan Masing-Masing Tiga Data Dummy
1. Jalankan server, lalu buka `http://localhost:8000/` pada web browser.
2. Pada halaman login, klik `register now`, lalu buat dua buah akun.
3. Masuk dengan salah satu akun. Klik `add new progress` untuk menambah sebuah progress. Lakukan tiga kali untuk menambah tiga buah progress.
4. Lakukan hal yang sama pada akun lainnya.
### Menghubungkan Model `Item` dengan `User`
1. Buka berkas `models.py` pada direktori `main`. Tambahkan import berikut.
   ```
   from django.contrib.auth.models import User
   ```
   Masih di berkas yang sama, di dalam `class Progress`, tambahkan baris berikut.
   ```
   user = models.ForeignKey(User, on_delete=models.CASCADE)
   ```
2. Buka berkas `views.py` pada direktori `main`. Ubah fungsi `create_progress` menjadi seperti berikut ini.
   ```
   def create_progress(request):
       form = ProgressForm(request.POST or None)

       if form.is_valid() and request.method == "POST":
           progress = form.save(commit=False)
           progress.user = request.user
           progress.save()
           return redirect('main:show_main')
       context = {'form': form}
       return render(request, "create_progress.html", context)
   ```
   Masih di berkas yang sama, ubah fungsi `show_main` menjadi seperti berikut ini.
   ```
   def show_main(request):
    progresses = Progress.objects.filter(user=request.user)
    context = {
        'name': request.user.username,
        'class': 'XII-Science-3',
        'number': '20',
        'progresses': progresses,
    }
    return render(request, "main.html", context)
   ```
3. Lakukan migration dengan cara `py manage.py makemigrations` lalu `py manage.py migrate`
### Menampilkan Detail Informasi Pengguna yang Sedang Logged In pada halaman utama aplikasi
1. Buka berkas `views.py` pada direktori `main`. Tambahkan beberapa import berikut.
   ```
   import datetime
   from django.http import HttpResponseRedirect
   from django.urls import reverse
   ```
   Masih di berkas yang sama, pada fungsi `login_user`, ganti kode pada blok `if user is not None` menjadi seperti berikut ini.
   ```
   if user is not None:
      login(request, user)
      response = HttpResponseRedirect(reverse("main:show_main"))
      response.set_cookie('last_login', str(datetime.datetime.now()))
      return response
   ```
   Masih di berkas yang sama, pada fungsi `show_main`, tambahkan baris berikut pada `context`.
   ```
   'last_login': request.COOKIES['last_login'],
   ```
   Masih di berkas yang sama, ubah fungsi `logout_user`.
   ```
   def logout_user(request):
    logout(request)
    response = HttpResponseRedirect(reverse('main:login'))
    response.delete_cookie('last_login')
    return response
   ```
2. Untuk menampilkan sesi terakhir login, tambahkan baris berikut setelah tombol logout.
   ```
   <h5>Sesi terakhir login: {{ last_login }}</h5>
   ```
## Tugas 5
### Melakukan kustomisasi pada halaman login, register, dan main
Untuk melakukan kusotmisasi, kita dapat menambahkan beberapa _style_ pada bagian-bagian yang ingin dikustomisasi. Seperti pada `study-tracker` ini, saya sudah mengkustomisasi daftar item menjadi menggunakan _card_, mengkustomisasi tombol, mengatur posisi teks, dan mengatur warna latar belakang _website_.
### Menambahkan Fitur _Update_ dan _Delete_ untuk Masing-Masing _Item_
1. Di berkas `views.py` pada folder `main`, tambahkan fungsi `delete` dan `update`.
   ```
   def delete_progress(request, id):
      progress = Progress.objects.get(pk = id)
      progress.delete()
      return HttpResponseRedirect(reverse('main:show_main'))
   ```
   ```
   def edit_progress(request, id):
    progress = Progress.objects.get(pk = id)
    form = ProgressForm(request.POST or None, instance=progress)

    if form.is_valid() and request.method == "POST":
        form.save()
        return HttpResponseRedirect(reverse('main:show_main'))

    context = {'form': form}
    return render(request, "edit_progress.html", context)
   ```
2. Di folder yang sama, buka berkas `urls.py`, lalu import fungsi delete dan edit.
   ```
   from main.views import delete_progress, edit_progress 
   ```
   Masih di berkas yang sama, tambahkan `path` berikut pada `urlpatterns`
   ```
   path('edit-progress/<int:id>', edit_progress, name='edit_progress'),
   path('delete/<int:id>', delete_progress, name='delete_progress'),
   ```
## Tugas 6
### Mengubah kode cards data item agar dapat mendukung AJAX GET dan melakukan pengambilan task menggunakan AJAX GET
Pada file `main.html`, hapus card yang ada di bagian body. Lalu, tambahkan _script_ berikut untuk melakukan refresh buku secara _asyncronous_.
   ```
   <script>
   async function getProgresses() {
         return fetch("{% url 'main:show_json' %}").then((res) => res.json())
   }
   async function refreshProgresses() {
      document.getElementById("progress_table").innerHTML = ""
      const progress = await getProgresses()
      let htmlString = '<div class="row">'
      if (progress.length > 0) {
         progress.forEach((item) => {
         htmlString += `<div class="col-md-4">
               <div class="card-body" style="background-color:#9AD0C2; color: #265073;">
               <h3 class="card-title">${item.fields.subject}</h3>
               <p class="card-text">Start study : ${item.fields.start_Study}</p>
               <p class="card-text">Progress (%) : ${item.fields.progress}</p>
               <p class="card-text">Catatan</p>
               <div class = "catatan">${item.fields.catatan}</div>
               
               <a href="/edit-progress/${item.pk}" style="text-decoration: none; padding-left: 0; margin-bottom: 1vh">
                  <button type="button" class="btn btn-info" style = "color: white; display: inline-block;">
                     <i class="fas fa-pencil-alt"></i> 
                     Edit Progress
                  </button>
               </a>
               <a href = "/delete/${item.pk}" style="text-decoration: none; padding-left: 0;">
                  <button type="button" class="btn btn-warning" style = "display: inline-block;">
                  <i class="fas fa-trash-alt"></i> Delete Progress
                  </button>
               </a>
               <div style="margin-top: 2vh; padding-bottom: 1vh;">
                  <p class="card-text">Date added : ${item.fields.date_added}</p>
               </div>
               </div>
         </div>`
         })
      } else {
         htmlString = `<div class="col-md-12 text-center" id="no-progress" style="margin-bottom: 16vh; margin-top: 16vh;">
         <p>No progress available.</p>
         </div>`
      }
      htmlString += '</div>'
      document.getElementById("progress_table").innerHTML = htmlString
   }

   refreshProgresses()
   ```
   Tambahkan juga `<div id="progress_table"></div>` sebagai target untuk menampilkan progress tersebut.
### Membuat Fitur add progress by AJAX
1. Pada berkas `views.py`, tambahkan import berikut

   `from django.views.decorators.csrf import csrf_exempt`

   Tambahkan juga fungsi berikut untuk menambahkan buku dengan AJAX.
   ```
   @csrf_exempt
   def add_progress_ajax(request):
      if request.method == 'POST':
         subject = request.POST.get("subject")
         start_Study = request.POST.get("start_Study")
         progress = request.POST.get("progress")
         catatan = request.POST.get("catatan")
         user = request.user

         new_progress = Progress(subject=subject, start_Study=start_Study, progress=progress, catatan=catatan, user=user)
         new_progress.save()

         return HttpResponse(b"CREATED", status=201)

      return HttpResponseNotFound()
   ```
2. Lakukan routing dengan mengimpor fungsi tersebut di `urls.py`, lalu tambahkan path di `urlpatterns`.
3. Di berkas `main.html`, tambahkan script berikut.
   ```
   function addProgress() {
      fetch("{% url 'main:add_progress_ajax' %}", {
          method: "POST",
          body: new FormData(document.querySelector('#form'))
      }).then(refreshProgresses)

      document.getElementById("form").reset()
      return false
   }
      document.getElementById("button_add").onclick = addProgress
   ```
4. Tambahkan tombol untuk membuka form add book by AJAX.
   ```
   <button type="button" class="btn btn-primary" data-bs-toggle="modal" data-bs-target="#exampleModal" style="margin-left: 1vw; margin-bottom: 3vh;">
        Add Progress by AJAX
   </button>
   ```
5. Tambahkan _form_ add progress by AJAX berikut.
   ```
   <div class="modal fade" id="exampleModal" tabindex="-1" aria-labelledby="exampleModalLabel" aria-hidden="true">
      <div class="modal-dialog">
            <div class="modal-content">
               <div class="modal-header">
                  <h1 class="modal-title fs-5" id="exampleModalLabel">Add New Progress</h1>
                  <button type="button" class="btn-close" data-bs-dismiss="modal" aria-label="Close"></button>
               </div>
               <div class="modal-body">
                  <form id="form" onsubmit="return false;">
                        {% csrf_token %}
                        <div class="mb-3">
                           <label for="subject" class="col-form-label">Subject:</label>
                           <input type="text" class="form-control" id="subject" name="subject"></input>
                        </div>
                        <div class="mb-3">
                           <label for="start_Study" class="col-form-label">Start Study:</label>
                           <input type="text" class="form-control" id="start_Study" name="start_Study"></input>
                        </div>
                        <div class="mb-3">
                           <label for="progress" class="col-form-label">Progress (%):</label>
                           <input type="number" class="form-control" id="progress" name="progress"></input>
                        </div>
                        <div class="mb-3">
                           <label for="catatan" class="col-form-label">Catatan:</label>
                           <textarea class="form-control" id="catatan" name="catatan"></textarea>
                        </div>
                  </form>
               </div>
               <div class="modal-footer">
                  <button type="button" class="btn btn-secondary" data-bs-dismiss="modal">Close</button>
                  <button type="button" class="btn btn-primary" id="button_add" data-bs-dismiss="modal">Add Progress</button>
               </div>
            </div>
      </div>
   </div>
   ```
   Dengan form ini, ketika tombol `Add Progress` pada form diklik, script pada nomor 3 akan dijalankan, sehingga akan menambahkan progress ke card dan melakukan refresh halaman.


#### Tampilan Masing-Masing Fungsi pada Aplikasi Postman
![2024-02-20](https://github.com/FasiIkom/study-tracker/assets/158117087/89a5698a-99b4-4cf6-ac8a-5a9eb602028a)
![Screenshot (31)](https://github.com/FasiIkom/study-tracker/assets/158117087/b9caa621-a278-4126-817c-9e0e502769a6)
![Screenshot (32)](https://github.com/FasiIkom/study-tracker/assets/158117087/15939858-e451-45dd-9240-036e64dec5c2)
![Screenshot (33)](https://github.com/FasiIkom/study-tracker/assets/158117087/ce5a2b9a-0caf-41a7-987e-3513e6d105e7)

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
### Apa itu Django `UserCreationForm`? Apa kelebihan dan kekurangannya?
`UserCreationForm` adalah formulir bawaan yang disediakan oleh Django yang dapat menerima input dari pengguna (dapat berupa integer, string, dan lainnya) dan menyimpannya ke dalam model. Salah satu kelebihan menggunakan `UserCreationForm` adalah developer tidak perlu lagi membuat form sendiri, karena sudah disediakan oleh Django. Kekurangannya adalah tampilannya yang terbatas karena developer tidak dapat mengkustomisasi form terlalu banyak.
### Apa perbedaan antara autentikasi dan otorisasi dalam Django, dan mengapa keduanya penting?
Autentikasi adalah proses untuk memverifikasi siapa pengguna yang sedang mengakses, sedangkan otorisasi adalah proses untuk memverifikasi apa yang dapat pengguna yang telah diautentikasi lakukan. Keduanya penting agar tidak semua user diizinkan untuk mengakses hal-hal yang tidak diizinkan untuk diakses.
### Apa itu cookies dalam aplikasi web, dan bagaimana Django menggunakan cookies untuk mengelola data sesi pengguna?
Cookies adalah file yang disimpan oleh server web di komputer pengguna saat mereka mengunjungi sebuah situs web. Jadi, ketika pengguna kembali mengunjungi situs tersebut, proses loading akan menjadi lebih cepat. Django mengelola cookies pengguna dengan cara menerima ID pengguna dari klien, lalu menyimpannya di server.
### Apakah penggunaan cookies aman secara default dalam pengembangan web, atau apakah ada risiko potensial yang harus diwaspadai?
Umumnya, penggunaan cookies aman karena cookies hanyalah sebuah data, bukan kode program, sehingga _hacker_ tidak dapat memasukkan kode program ke dalam cookies. Akan tetapi, tetap ada risiko yang harus diwaspadai, seperti diambilnya data cookies pengguna oleh orang lain.
### Jelaskan manfaat dari setiap element selector dan kapan waktu yang tepat untuk menggunakannya
Elemen selektor adalah CSS yang digunakan untuk mengubah _style_ dari semua elemen dengan tag HTML yang sama. Berguna ketika ingin mengubah semua elemen dengan tag yang sama secara konsisten pada suatu halaman.
### Jelaskan HTML5 Tag yang kamu ketahui
- <header> : Digunakan untuk membuat header dari halaman web, biasanya berisi judul
- <nav> : Digunakan untuk membuat bar navigasi dari halaman web, biasanya berisi menu yang mengarahkan ke bagian-bagian web.
- <article> : Digunakan untuk membuat artikel.
- <section> : Digunakan untuk membagi web menjadi beberapa bagian.
- <footer> : Digunakan untuk membuat footer dari halaman web, biasanya berisi hak cipta atau link ke konten.
### Jelaskan perbedaan antara margin dan padding
Keduanya sama-sama memberikan ruangan kosong di sekitar konten, perbedaannya ruangan pada _padding_ dapat diisi dengan konten lain, sedangkan _margin_ tidak.
### Jelaskan perbedaan antara framework CSS Tailwind dan Bootstrap. Kapan sebaiknya kita menggunakan Bootstrap daripada Tailwind, dan sebaliknya?
Bootstrap lebih mudah digunakan karena menggunakan gaya dan komponen yang sudah didefinisikan, sedangan tailwind, pengguna masih harus mengatur tampilan HTML mereka. Karena itu, tailwind lebih fleksibel untuk digunakan.
### Jelaskan perbedaan antara _asynchronous programming_ dengan _synchronous programming_
_asynchronous programming_ adalah salah satu cara untuk memproses program secara efektif dan efisien. Dalam proses _asynchronous programming_, program dapat menjalankan suatu tugas sambil tetap menampilkan halaman lainnya, sehingga memungkinkan user untuk dapat tetap berinteraksi dengan halaman web saat server menjalankan _request_ dari user.
### Dalam penerapan JavaScript dan AJAX, terdapat penerapan paradigma _event-driven programming_. Jelaskan maksud dari paradigma tersebut dan sebutkan salah satu contoh penerapannya pada tugas ini
_event-driven programming_ adalah serangkaian perintah yang hanya akan dijalankan ketika terjadi suatu kondisi yang telah ditentukan. Kondisi tersebut dapat berupa klik mouse, gerakan mouse, mengetikkan suatu karakter di keyboard, dan masih banyak lagi. Pada program ini, salah satu contoh _event-driven programming_ adalah pada bagian _button_, yang mana akan menjalankan perintah seperti _add new progress_ ketika tombol tersebut ditekan.
### Jelaskan penerapan _asynchronous programming_ pada AJAX
 AJAX memungkinkan halaman web untuk memperbarui data secara asinkronus dengan mengirimkan data ke _server_ di balik layar dengan menggunakan XML. Hal itu memungkinkan kita dapat memperbarui sebagian elemen data pada halaman tanpa harus me-reload halaman secara keseluruhan.
### Pada PBP kali ini, penerapan AJAX dilakukan dengan menggunakan Fetch API daripada _library_ jQuery. Bandingkanlah kedua teknologi tersebut dan tuliskan pendapat kamu teknologi manakah yang lebih baik untuk digunakan
Fetch API merupakan bawaan dari JavaScript, sedangkan jQuery merupakan sebuah _library_. Dibandingkan jQuery, Fetch API cenderung lebih modern dan lebih efisien karena tidak harus mengimpor semua fungsi melainkan hanya mengambil yang akan digunakan saja. Sedangkan, jQuery memiliki dukungan yang lebih baik kepada _browser_ lawas. Menurut pendapat saya, Fetch API cenderung lebih baik untuk digunakan karena lebih fleksibel. Meskipun begitu, pemilihan antara penggunaan Fetch API atau jQuery tetap harus mempertimbangkan hal-hal lain, seperti adanya fitur jQuery yang tidak tersedia di Fetch API (berlaku juga sebaliknya), dan hal-hal lainnya.