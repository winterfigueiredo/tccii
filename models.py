from django.db import models
import datetime
from .choices import *
from django.contrib.auth.models import User
from dateutil.relativedelta import relativedelta



# Create your models here.
class Pesquisador(models.Model):
    usuario = models.ForeignKey(User, on_delete=models.CASCADE) 
    nome_pesq =  models.TextField()
    ceo = models.BooleanField(default=True)
    startup = models.TextField(default="")
    email = models.EmailField(default="")

    class Meta:
        ordering = ['nome_pesq']
        
       
    def __str__(self):
        return self.nome_pesq

class Pesquisa(models.Model):
    usuario = models.ForeignKey(User, on_delete=models.CASCADE) 
    pesquisador = models.ManyToManyField(Pesquisador)  # Relacionamento entre Pesquisa e Pesquisador
    titulo = models.TextField()
    data_inicio = models.DateField(default=datetime.datetime.now)
    duracao = models.IntegerField(default=10)
    num_pesquisadores = models.IntegerField()
    orcamento = models.DecimalField(max_digits=10, decimal_places=2)
    etapa = models.CharField(max_length=4, choices=ETAPA)

   
    class Meta:
        ordering = ['titulo']

    @property
    def prazofinal(self):
        # Calcula a data de prazo final somando a duração em meses à data de início
        return self.data_inicio + relativedelta(months=self.duracao)
    @property
    def data_formatada(self): 
        return self.data_inicio.strftime('%d/%m/%Y')
    
    @property
    def data_input(self): 
        return self.data_inicio.strftime('%YYYY/%MM/%DD')
    
    @property
    def diasfaltantes(self):
        # Calcula quantos dias faltam até o prazo final
        hoje = datetime.date.today()
        prazo_final = self.prazofinal
        if hoje > prazo_final:
            return 0
        else:
            return (prazo_final - hoje).days

   
    
        
    def __str__(self):
        return f"{self.titulo}- {self.pesquisador.usuario}"
    
    
class PesquisadorPesquisa(models.Model):
    pesquisador = models.ForeignKey(Pesquisador, on_delete=models.CASCADE)
    pesquisa = models.ForeignKey(Pesquisa, on_delete=models.CASCADE)

    def __str__(self):
        return f'{self.pesquisador.nome} - {self.pesquisa.titulo}'