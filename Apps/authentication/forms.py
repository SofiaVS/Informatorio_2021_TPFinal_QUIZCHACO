from django import forms
from django.db.models.base import Model
from django.forms import fields


from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import authenticate, get_user_model


User = get_user_model()


class UsuarioLoginForm(forms.Form):
    username = forms.CharField()
    password = forms.CharField(widget=forms.PasswordInput)

    def clean(self, *args, **kwargs):
        username = self.cleaned_data.get('username')
        password = self.cleaned_data.get('password')

        if username and password:
            user = authenticate(username=username, password=password)
            if not user:
                raise forms.ValidationError("Este usuario no existe")
            if not user.check_password(password):
                raise forms.ValidationError("Password Incorrecta")
            if not user.is_active:
                raise forms.ValidationError("Este usuario no esta actívo")
        return super(UsuarioLoginForm, self).clean(*args, **kwargs)


class RegisterForm(UserCreationForm):
    email = forms.EmailField(label='Correo', required=True)
    first_name = forms.CharField(label='Nombre', required=True)
    last_name = forms.CharField(label='Apellido', required=True)
    password1 = forms.CharField(
        label='Contraseña', widget=forms.PasswordInput, required=True)
    password2 = forms.CharField(
        label='Confirmar Contraseña', widget=forms.PasswordInput, required=True)

    class Meta:
        model = User
        fields = [
            'first_name',
            'last_name',
            'username',
            'email',
            'password1',
            'password2'
        ]

        help_texts = {k: "" for k in fields}
