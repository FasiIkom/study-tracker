# Penjelasan step-by-step Pembuatan Aplikasi study-tracker
## Membuat Proyek Django Baru
# Bagan Aplikasi Django

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
