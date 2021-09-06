from django.shortcuts import render


def Home(request):

    context = {
        'titulo': 'Quiz Chaco - Inicio'
    }

    return render(request, 'index.html', context)


def About(request):
    context = {
        'titulo': 'Quiz Chaco - Acerca de'
    }
    return render(request, 'about.html', context)
