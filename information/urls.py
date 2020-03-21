from django.urls import path

from information import views

urlpatterns = [
    path('company/<int:index>/', views.company_by_index),
    path('person-food/<int:index>/', views.food_for_person_by_index),
]
