from django.urls import path
from .views import my_view
from .views import my_results_view

urlpatterns = [
    path('', my_view, name='my-view'),
    path('results', my_results_view, name="results-view")
]
