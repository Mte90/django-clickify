from django.urls import path, include

# Temporary urls for testing
urlpatterns = [
    path('download/', include('clickify.urls', namespace="clickify")),
    path('download/api/', include('clickify.drf_urls', namespace="clickify-drf"))
]
