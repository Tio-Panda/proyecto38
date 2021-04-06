from django import forms
from .models import Negocios

class NegociosForm(forms.ModelForm):

    class Meta:
        model = Negocios
        fields = ['nombre']


