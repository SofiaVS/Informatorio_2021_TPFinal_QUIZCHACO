from django.urls import path
from .views import resultado_pregunta

app_name = 'response'

urlpatterns = [
    path('<int:pregunta_respondida_pk>/', resultado_pregunta, name='resultado'),
]
