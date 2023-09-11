from django.urls import path

from . import views

urlpatterns = [
    path('', views.index, name='insert_index'),
    path('upload/', views.upload, name='upload'),
]
