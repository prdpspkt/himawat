from django.urls import path
from . import views

app_name = 'services'

urlpatterns = [
    # Service Categories
    path('', views.category_list, name='category_list'),
    path('category/<slug:slug>/', views.category_detail, name='category_detail'),

    # Individual Services
    path('service/<slug:slug>/', views.detail, name='detail'),
]
