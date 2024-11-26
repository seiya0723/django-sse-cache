from django.urls import path
from . import views

app_name    = "bbs"
urlpatterns = [
    path('', views.index, name="index"),

    path('topic_stream/', views.topic_stream, name="topic_stream"),

]

