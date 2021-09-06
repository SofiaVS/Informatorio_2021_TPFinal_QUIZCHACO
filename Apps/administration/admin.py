
from django.contrib import admin


# Register your models here.
from Apps.genericos.models import Pregunta, ElegirRespuesta, PreguntasRespondidas, QuizUsuario, Category
from .forms import ElegirInLineFormSet

# mejoramos como se ve en sección admin


class ElegirRespuestaInline(admin.TabularInline):
    model = ElegirRespuesta
    can_delete = False
    max_num = ElegirRespuesta.MAX_RESPONSE
    min_num = ElegirRespuesta.MAX_RESPONSE
    formset = ElegirInLineFormSet


class PreguntaAdmin(admin.ModelAdmin):
    model = Pregunta
    inlines = (ElegirRespuestaInline,)
    list_display = ['texto', ]
    search_fields = ['texto', 'preguntas__texto']  # dos niveles arriba


class PreguntasRespondidasAdmin(admin.ModelAdmin):
    list_display = ['pregunta', 'respuesta', 'correcta', 'puntaje_obtenido']
    list_per_page = 15

    class Metal:
        model = PreguntasRespondidas


class QuizUsuarioAdmin(admin.ModelAdmin):

    list_display = ['usuario', 'puntaje_total']

    class Metal:
        model = QuizUsuario


# registramos en secciones admin
admin.site.register(PreguntasRespondidas, PreguntasRespondidasAdmin)
admin.site.register(Pregunta, PreguntaAdmin)
admin.site.register(ElegirRespuesta)
admin.site.register(QuizUsuario, QuizUsuarioAdmin)
admin.site.register(Category)
