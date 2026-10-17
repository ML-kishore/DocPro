from django.urls import path
from . import views

urlpatterns = [
    path('upload/',views.upload_file,name='upload_file'),
    path('files/',views.view_files,name='view_files'),
    path('update/<int:id>/',views.update_file,name='update_file'),
    path('delete/<int:id>/',views.delete_files,name='delete_file'),
]
