from django.urls import path, include

# Temporary urls for testing
urlpatterns = [
    path('download/', include('clickify.urls', namespace="clickify"))
]
