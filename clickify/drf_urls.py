from django.urls import path
from .drf_views import TrackDownloadAPIView

app_name = "clickify-drf"

urlpatterns = [
    path('<slug:slug>/', TrackDownloadAPIView.as_view(), name='track_download_api'),
]
