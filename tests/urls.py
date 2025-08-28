from django.urls import path, include

# Temporary urls for testing
urlpatterns = [
    path('track/', include('clickify.urls', namespace="clickify")),
    path('api/track/', include('clickify.drf_urls', namespace="clickify-drf"))
]
