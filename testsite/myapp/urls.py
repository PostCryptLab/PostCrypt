from django.urls import path
from .views import my_view, register, my_results_view, courses_view, MyLoginView
from django.contrib.auth.views import LoginView, LogoutView
from django.contrib.auth.views import LogoutView

urlpatterns = [
    path('login/', LoginView.as_view(template_name='login.html'), name='login'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('register/', register, name='register'),
    path('dashboard/', courses_view, name='dashboard'),
    path('', my_view, name='my-view'),
    path('results', my_results_view, name="results-view"),
]
