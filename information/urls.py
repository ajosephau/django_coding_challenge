from django.urls import path

from information import views

urlpatterns = [
    path('company/<int:index>/', views.company_by_index),
    path('mutual-friends-alive-brown-eyes/<int:person_one_index>/<int:person_two_index>/', views.mutual_friends_alive_with_brown_eyes),
    path('person-food/<int:index>/', views.food_for_person_by_index),
]
