from django.urls import path
from . import views

urlpatterns = [
    path('', views.event_list, name='event_list'),
    path('signup/', views.student_signup, name='signup'),
    path('login/', views.student_login, name='login'),
    path('logout/', views.student_logout, name='logout'),
    path('register/<int:event_id>/', views.register_event, name='register_event'),
    path('my-registrations/', views.my_registrations, name='my_registrations'),
]