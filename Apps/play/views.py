from django.core.exceptions import ObjectDoesNotExist

from django.http.response import Http404
from django.shortcuts import redirect, render
from Apps.genericos.models import QuizUsuario
from django.contrib.auth.decorators import login_required

# Create your views here.


@login_required
def playQuiz(request):
    QuizUser, created = QuizUsuario.objects.get_or_create(usuario=request.user)

    if request.method == 'POST':
        pregunta_pk = request.POST.get('pregunta_pk')
        pregunta_respondida = QuizUser.intentos.select_related(
            'pregunta').get(pregunta__pk=pregunta_pk)
        respuesta_pk = request.POST.get('respuesta_pk')

        try:
            opcion_selecionada = pregunta_respondida.pregunta.opciones.get(
                pk=respuesta_pk)
        except ObjectDoesNotExist:
            raise Http404

        QuizUser.validate_intent(pregunta_respondida, opcion_selecionada)
        return redirect('response:resultado', pregunta_respondida.pk)

    else:
        # En lo siguiente verificamos que no exista un intento sin
        # haberse seleccionado una respuesta, por ejemplo en la situación
        # en que un usuario cierra la aplicación sin responder
        # traemos todos los registros de preguntas en null
        questions = QuizUser.get_incomplete_question()
        if questions:  # verificamos que existan
            questions.delete()  # lo eliminamos

        pregunta = QuizUser.get_new_question()
        if pregunta is not None:
            QuizUser.create_intent(pregunta)

        context = {
            'pregunta': pregunta,
            'titulo': "Quiz Chaco - Jugar",
        }

    return render(request, 'play/play.html', context)


@login_required
def reset(request):
    QuizUser, created = QuizUsuario.objects.get_or_create(usuario=request.user)
    QuizUser.reset_game()
    return redirect('play:playQuiz')
