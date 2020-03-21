from django.urls import path

from information import views

urlpatterns = [
    path('person-food/<int:index>/', views.food_for_person_by_id),
]
