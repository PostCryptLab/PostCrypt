from django.urls import path
from .views import home, register, my_results_view, courses_view, view_document
from django.contrib.auth.views import LoginView, LogoutView
from django.contrib.auth.views import LogoutView

urlpatterns = [
    path('login/', LoginView.as_view(template_name='login.html'), name='login'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('register/', register, name='register'),
    path('dashboard/', courses_view, name='dashboard'),
    path('', home, name='home'),
    path('results', my_results_view, name="results-view"),
    path('documents/<int:document_id>/', view_document, name='view_document'),
]
