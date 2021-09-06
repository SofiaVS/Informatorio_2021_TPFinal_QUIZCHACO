
from django import forms
from Apps.genericos.models import Pregunta


class ElegirInLineFormSet(forms.BaseInlineFormSet):
    def clean(self):
        super(ElegirInLineFormSet, self).clean()

        respuesta_correcta = 0
        for formulario in self.forms:
            if not formulario.is_valid():
                return
            # Controlamos cuantos estan marcados como True
            if formulario.cleaned_data and formulario.cleaned_data.get('correcta') is True:
                respuesta_correcta += 1

        try:
            # verificamos que la cantidad sea igual a lo establecido en el modelo
            assert respuesta_correcta == Pregunta.RESPUESTAS_PERMITIDAS
        except AssertionError:
            raise forms.ValidationError('Solo una sola respuesta es permitida')
