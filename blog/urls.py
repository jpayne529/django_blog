from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('item/<slug:slug>/', views.item, name='item'),
    path('tag/<str:tag>/', views.tagsearch, name='tag'),
]
