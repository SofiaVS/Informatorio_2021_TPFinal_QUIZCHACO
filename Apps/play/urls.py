from django.urls import path
from .views import playQuiz, reset

app_name = 'play'

urlpatterns = [
    path('', playQuiz, name='playQuiz'),
    path('reset/', reset, name='reset'),
]
