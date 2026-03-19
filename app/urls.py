from django.urls import path
from . import views

app_name = 'app'

urlpatterns = [
    path('', views.index, name='index'),
    path('test/', views.test, name='test'),
    path('picrotate/', views.picrotate, name='picrotate'),
    path('get-bookmarks/', views.get_bookmarks, name='get_bookmarks'),
    path('bookmarks/', views.bookmark, name='bookmark'),
    path('bookmarks/<int:pk>/visit/', views.bookmark_visit, name='bookmark_visit'),
]