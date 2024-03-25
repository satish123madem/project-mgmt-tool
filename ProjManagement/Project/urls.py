
from django.urls import path

from . import views

urlpatterns = [
    path('project/', views.Project.as_view()),
    path('project/<int:id>/', views.Project.as_view()),
    path('team/', views.Team.as_view()),
    path('team/<int:id>/', views.Team.as_view()),
    path('team/<int:id>/<str:action>/', views.Team.as_view()),
    path('task/', views.Task.as_view()),   
    path('task/<int:id>/', views.Task.as_view()),    

]