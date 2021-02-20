from django.contrib.auth.forms import UserCreationForm
from django import forms
from .models import CustomUser as User


class CadastroForm(UserCreationForm):
    """SubClasse de UserCreationForm que já possui o atributo user_name."""

    email = forms.EmailField(label='Email')
    name = forms.CharField(label='Name')

    class Meta():
        model = User
        fields = {"username", "name", "email"}

    def save(self, commit=False):
        user = super(CadastroForm, self).save(commit=False)
        fullname = self.cleaned_data["name"].split(None, 1)
        if len(fullname) > 1:
            first_name, last_name = fullname
            user.first_name = first_name
            user.last_name = last_name
        else:
            user.first_name = fullname[0]
        user.email = self.cleaned_data["email"]
        user.is_email_activated = False
        if commit:
            user.save()
        return user


class ConfirmaEmailForm(forms.Form):
    codigo = forms.CharField(label='codigo', max_length=200)
