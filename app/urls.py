from django.urls import path, include
from rest_framework.routers import DefaultRouter
from . import views

app_name = 'app'

router = DefaultRouter()
router.register('api/bookmarks', views.BookmarkViewSet, basename='api-bookmark')
router.register('api/tags', views.TagViewSet, basename='api-tag')

urlpatterns = [
    path('', views.index, name='index'),
    path('test/', views.test, name='test'),
    path('picrotate/', views.picrotate, name='picrotate'),
    path('get-bookmarks/', views.get_bookmarks, name='get_bookmarks'),
    path('bookmarks/', views.bookmark, name='bookmark'),
    path('bookmarks/<int:pk>/visit/', views.bookmark_visit, name='bookmark_visit'),
    path('', include(router.urls)),
]
