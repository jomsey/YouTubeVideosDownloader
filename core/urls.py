from django.urls import path
from . import views

urlpatterns = [
    path("",views.IndexView.as_view(),name="index"),
    path("download/<str:video_id>",views.DownloadVideoView.as_view(),name="download"),
]
