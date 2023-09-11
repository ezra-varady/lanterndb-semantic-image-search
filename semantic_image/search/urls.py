from django.urls import path

from . import views

urlpatterns = [
    path('', views.index, name='search_index'),
    path('image/<int:image_id>/', views.get_image, name='get_image'),
    path('query/', views.get_topn, name='get_topn'),
]
