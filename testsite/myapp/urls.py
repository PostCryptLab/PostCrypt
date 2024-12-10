from django.urls import path
from . import views
from django.contrib.auth.views import LoginView, LogoutView
from django.contrib.auth.views import LogoutView

urlpatterns = [
    path('create_lab/', views.create_lab, name='create_lab'),
    path('login/', LoginView.as_view(template_name='login.html'), name='login'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('register/', views.register, name='register'),
    path('dashboard/', views.courses_view, name='dashboard'),
    path('', views.home, name='home'),
    path('results', views.my_results_view, name="results-view"),
    path('documents/<int:document_id>/', views.view_document, name='view_document'),

]
