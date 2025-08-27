from django.urls import path
from .views import track_download

app_name = 'clickify'

urlpatterns = [
    path('<path:file_path>', track_download, name='track_download'),
]
