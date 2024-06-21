from django import forms 
from .models import Pesquisa, Pesquisador

class PesquisaForm(forms.ModelForm):
    class Meta:
        model = Pesquisa
        fields = ['pesquisador', 'titulo','data_inicio','duracao','num_pesquisadores','orcamento','etapa']

class PesquisadorForm(forms.ModelForm):
    class Meta:
        model = Pesquisador
        exclude = ['usuario']