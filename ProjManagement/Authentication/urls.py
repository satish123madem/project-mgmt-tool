
from django.urls import path

from . import views

urlpatterns = [
    path('login/', views.Auth.as_view()),
    path('register/', views.Register.as_view()),
    path('register/<bulk>/', views.Register.as_view()),
    path('user-detail/', views.User.as_view()),
    path('user-detail/<args>/', views.User.as_view()),    

]
