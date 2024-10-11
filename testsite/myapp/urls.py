from django.urls import path
from .views import my_view, register, my_results_view, MyLoginView
from django.contrib.auth.views import LoginView
from django.contrib.auth.views import LogoutView

urlpatterns = [
    path('login/', LoginView.as_view(template_name='login.html'), name='login'),  # Ścieżka do logowania
    path('register/', register, name='register'),
    path('', my_view, name='my-view'),
    path('results', my_results_view, name="results-view"),
]
