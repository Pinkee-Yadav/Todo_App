from django.urls import path
from . import views


urlpatterns = [
path('', views.index, name='index'),
path('register/', views.register_view, name='register'),
path('login/', views.login_view, name='login'),
path('logout/', views.logout_view, name='logout'),
path('task/add/', views.add_task, name='add_task'),
path('task/<int:pk>/edit/', views.edit_task, name='edit_task'),
path('task/<int:pk>/delete/', views.delete_task, name='delete_task'),
path('task/<int:pk>/toggle/', views.toggle_complete, name='toggle_complete'),
]
