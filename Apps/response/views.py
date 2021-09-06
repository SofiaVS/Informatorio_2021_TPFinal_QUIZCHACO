from django.shortcuts import render, get_object_or_404
from Apps.genericos.models import PreguntasRespondidas
# Create your views here.


def resultado_pregunta(request, pregunta_respondida_pk):
    respondida = get_object_or_404(
        PreguntasRespondidas, pk=pregunta_respondida_pk)
    context = {
        'respondida': respondida,
        'titulo': "Quiz Chaco - Respuesta"
    }
    return render(request, 'response/response.html', context)
