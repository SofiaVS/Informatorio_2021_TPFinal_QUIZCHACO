from django.db import models

from Apps.core.models import TimeModel
from Apps.usuarios.models import Usuario

import random
# Modelo pregunta


class Category(models.Model):
    texto = models.TextField(verbose_name='Nombre de la categoría')

    def __str__(self):
        return self.texto


class Pregunta(models.Model):
    RESPUESTAS_PERMITIDAS = 1
    texto = models.TextField(verbose_name='Texto de la pregunta')
    max_puntaje = models.DecimalField(
        verbose_name='Máximo Puntaje', default=3, decimal_places=2, max_digits=6)
    categoria = models.ForeignKey(
        Category, related_name='category', on_delete=models.CASCADE, null=True)

    def __str__(self):
        return self.texto

# Relación Pregunta con posibles respuestas


class ElegirRespuesta(models.Model):
    MAX_RESPONSE = 3  # número para definir el número de respuestas posibles
    pregunta = models.ForeignKey(
        Pregunta, related_name='opciones', on_delete=models.CASCADE)
    correcta = models.BooleanField(
        verbose_name='¿Es esta la respuesta correcta?', default=False, null=False)
    texto = models.TextField(verbose_name='Texto de la respuesta')

    def __str__(self):
        return self.texto


class QuizUsuario(models.Model):
    # Usuario que esta realizando el Quiz
    usuario = models.OneToOneField(Usuario, on_delete=models.CASCADE)
    puntaje_total = models.DecimalField(
        verbose_name='Puntaje Total', default=0, decimal_places=2, max_digits=10)

    def create_intent(self, pregunta):
        intento = PreguntasRespondidas(pregunta=pregunta, quizUser=self)
        intento.save()

    def get_new_question(self):
        # guardamos las pk de preguntas respondidas
        respondidas = PreguntasRespondidas.objects.filter(quizUser=self).values_list(
            'pregunta__pk', flat=True)  # nos devuelve un queryset de tuplas
        # excluimos pk de las preguntas respondidas
        preguntas_restantes = Pregunta.objects.exclude(pk__in=respondidas)
        if not preguntas_restantes.exists():
            return None
        # devolvemos de forma random las preguntas restantes
        return random.choice(preguntas_restantes)

    def validate_intent(self, pregunta_respondida, respuesta_seleccionada):
        if pregunta_respondida.pregunta_id != respuesta_seleccionada.pregunta_id:
            return
        pregunta_respondida.respuesta_seleccionada = respuesta_seleccionada
        if respuesta_seleccionada.correcta is True:
            pregunta_respondida.correcta = True
            pregunta_respondida.puntaje_obtenido = respuesta_seleccionada.pregunta.max_puntaje
            pregunta_respondida.respuesta = respuesta_seleccionada
        else:
            pregunta_respondida.respuesta = respuesta_seleccionada
        pregunta_respondida.save()
        self.update_score()

    def update_score(self):
        puntaje_actualizado = self.intentos.filter(correcta=True).aggregate(
            models.Sum('puntaje_obtenido'))['puntaje_obtenido__sum']
        # fix de error arrojado cuando erramos la primera respuesta. Evitamos que no se guarde None
        if not puntaje_actualizado == None:
            self.puntaje_total = puntaje_actualizado
            self.save()

    def get_incomplete_question(self):
        preguntas_sin_responder = PreguntasRespondidas.objects.filter(
            quizUser=self, respuesta_id__isnull=True)
        return preguntas_sin_responder

    # delete current user's game
    def reset_game(self):
        self.delete()


class PreguntasRespondidas(models.Model):
    quizUser = models.ForeignKey(
        QuizUsuario, on_delete=models.CASCADE, related_name='intentos')
    pregunta = models.ForeignKey(Pregunta, on_delete=models.CASCADE)
    respuesta = models.ForeignKey(
        ElegirRespuesta, on_delete=models.CASCADE, null=True)
    correcta = models.BooleanField(
        verbose_name='¿Es esta la respuesta correcta?', default=False, null=False)
    puntaje_obtenido = models.DecimalField(
        verbose_name='Puntaje obtenido', default=0, decimal_places=2, max_digits=6)
