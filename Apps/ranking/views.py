from django.shortcuts import render
from Apps.genericos.models import QuizUsuario
from django.core.paginator import Paginator

# Create your views here.


def ranking(request):
    # definimos que solo se mostraran los diez primeros de la lista
    contact_list = QuizUsuario.objects.order_by('-puntaje_total')[:10]
    # mostramos 10 usuarios por paginación
    paginator = Paginator(contact_list, 15)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    context = {
        'page_obj': page_obj,
        'titulo': "Quiz Chaco - Ranking"
    }

    return render(request, 'ranking/ranking.html', context)
