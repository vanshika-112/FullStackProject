from django.urls import path
from .views import test_api, upload_csv
from .views import LastFiveDatasetsView

urlpatterns = [
    path('test/', test_api),
    path('upload/', upload_csv),
    path("datasets/last-five/", LastFiveDatasetsView.as_view()),
]