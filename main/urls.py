from django.urls import path
from main.views import show_main, create_progress, show_xml, show_json, show_xml_by_id, show_json_by_id, register, login_user, logout_user, edit_progress, delete_progress, add_progress_ajax

app_name = 'main'

urlpatterns = [
    path('', show_main, name='show_main'),
    path('create-progress', create_progress, name='create_progress'),
    path('json/', show_json, name='show_json'),
    path('xml/', show_xml, name='show_xml'),
    path('xml/<int:id>/', show_xml_by_id, name='show_xml_by_id'),
    path('json/<int:id>/', show_json_by_id, name='show_json_by_id'),
    path('register/', register, name='register'),
    path('login/', login_user, name='login'),
    path('logout/', logout_user, name='logout'),
    path('edit-progress/<int:id>', edit_progress, name='edit_progress'),
    path('delete/<int:id>', delete_progress, name='delete_progress'),
    path('create-progress-ajax/', add_progress_ajax, name='add_progress_ajax'),
]