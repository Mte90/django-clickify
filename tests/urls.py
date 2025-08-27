from django.urls import path, reverse
from clickify.views import track_download

# Temporary urls for testing
urlpatterns = [
    path('download/<path:file_path>', track_download, name='track_download')
]
