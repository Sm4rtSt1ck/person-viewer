from django.urls import path
from . import views


urlpatterns = [
    path('', views.index, name='index'),
    path('random/', views.random_person, name='random'),
    path('<int:user_id>/', views.person_detail, name='person_detail'),
]
