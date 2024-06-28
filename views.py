from django.shortcuts import render, redirect, HttpResponse, get_object_or_404
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.contrib import messages
from django.db.models import Sum
from django.utils import timezone
from . import models

# Create your views here.

def index(request):
    # usuarios = Usuario.objects.all()
     return render(request, "landing_page.html")



@login_required
def home(request):
    usuario = request.user
    pesquisas = models.Pesquisa.objects.filter(usuario=usuario)
    pesqPlanejamento = models.Pesquisa.objects.filter(usuario=usuario, etapa="Planejamento")
    pesqElaboracao = models.Pesquisa.objects.filter(usuario=usuario, etapa="Elaboração")
    pesqExecucao = models.Pesquisa.objects.filter(usuario=usuario, etapa="Execução")
    pesqFinalizado = models.Pesquisa.objects.filter(usuario=usuario, etapa="Finalizado")
    npesquisas = pesquisas.count
    pesquisadores = models.Pesquisador.objects.filter(usuario=usuario)
    npesquisadores = pesquisadores.count
    if npesquisas==0 :
        somacusto = 0
    else:
        somacusto = pesquisas.aggregate(Sum('orcamento'))['orcamento__sum'] 
    data_atual = timezone.now()

    return render(request, "home.html", {
        'pesquisas': pesquisas,
        'npesquisas': npesquisas,
        'pesquisadores': pesquisadores,
        'npesquisadores': npesquisadores,
        'usuario': usuario,
        'somacusto': somacusto,
        'data_atual': data_atual,
        'pesqplanejamento': pesqPlanejamento,
        'pesqelaboracao': pesqElaboracao,
        'pesqexecucao': pesqExecucao,
        'pesqfinalizacao': pesqFinalizado,
        }
        )


def irlogin(request):
     return render(request, "login.html")

def novouser(request):
     return render(request, "cadastro_user.html")

def erro(request):
    return render (request,"erro.html")


def cadastrar(request):
     if request.method == 'POST':
          nome = request.POST.get('nome')
          email = request.POST.get('email')
          senha = request.POST.get('senha')
          nome_startup= request.POST.get('nomestartup')
          usuario = models.Usuario.objects.create(nome=nome, email=email, senha=senha,nome_startup = nome_startup)
          #criar validação para não deixar repetir o usuário
          if nome and email and senha and nome_startup:
            usuario.save()
            return render(request, "home.html", {"usuario": usuario})
          else:
            return render(request, 'login.html')
          
# Está cadastrando por caduser
def caduser(request):
     if request.method == 'POST':
        nome = request.POST.get('nome')
        email = request.POST.get('email')
        senha = request.POST.get('senha')
        startup = request.POST.get('nomestartup')
        #criar validação para não deixar repetir o usuário
        if nome and email and senha:
            usuario = User.objects.create_user(username=nome, email=email, password=senha, last_name = startup)
            usuario.save()
        user = authenticate(request, username=nome, password=senha)
        if user is not None:
                login(request, user)
                return redirect(home)
        else:
            return render(request, 'login.html')


def logar(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        senha = request.POST.get('senha')
        if email and senha:
            usuario = models.Usuario.objects.get(email=email)
            return render(request,"home.html",  usuario)
        else:
            return render("login.html")    
        
def loguser(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        senha = request.POST.get('senha')
        user = authenticate(username = email, password=senha)
        if user is not None:
            login(request, user)
            # return render(request, "home.html", {"usuario": user})
            return redirect(home)
            
        else:
            messages.error(request, 'Email ou senha incorretos.')
            return render(request, "login.html")

def logout_view(request):
    logout(request)
    return render(request, "landing_page.html")

# @login_required          
def mostrarroadmap(request):
    return render(request,"roadmap.html")


def novoproj(request):
    return render(request, "cadastro_projeto.html")

@login_required
def pesquisadores(request):
    usuario = request.user
    pesquisadores = models.Pesquisador.objects.filter(usuario=usuario)
    data_atual = timezone.now()
    return render(request, 'pesquisadores.html', {'pesquisadores': pesquisadores, 'data_atual': data_atual})


@login_required
def pesquisas(request):
    usuario = request.user
    pesquisadores = models.Pesquisador.objects.filter(usuario=usuario)
    pesquisas = models.Pesquisa.objects.filter(usuario=usuario)
    somacusto = pesquisas.aggregate(Sum("orcamento")) 
    data_atual = timezone.now()

    return render(request, "pesquisa.html", {'pesquisas': pesquisas,'pesquisadores': pesquisadores, 'somacusto':somacusto, 'data_atual': data_atual})

@login_required
def roadmap(request):
    usuario = request.user
    pesquisas = models.Pesquisa.objects.filter(usuario=usuario)
    return render(request, "roadmap.html", {'pesquisas': pesquisas})


@login_required
def salvar_pesquisador(request):
    nome_pesq = request.POST.get('nomePesq') 
    emailpesq = request.POST.get('emailPesq') 
    usuario = request.user
    # pesq_id = usuario.id
    if request.method == 'POST':
        novopesq = models.Pesquisador.objects.create(nome_pesq = nome_pesq, usuario_id = usuario.id, email = emailpesq)
        novopesq.save()
        return redirect(pesquisadores)
    return redirect(pesquisadores)
    

@login_required
def salvar_pesquisa(request):   
    titulo = request.POST.get('titulo')
    datainicio = request.POST.get('datainicio')
    duracao = request.POST.get('duracao')
    orcamento = request.POST.get('orcamento')
    etapa = request.POST.get('etapa')
    usuario = request.user
    pesquisadores = request.POST.getlist('pesquisadores')
    npesqui = len(pesquisadores)

    if request.method=='POST':
        novapesquisa = models.Pesquisa.objects.create(
            usuario = usuario,
            titulo = titulo,
            data_inicio = datainicio,
            duracao = duracao,
            num_pesquisadores = npesqui,
            orcamento = orcamento,
            etapa = etapa
        )
        novapesquisa.save()       
        novapesquisa.pesquisador.set(pesquisadores)
        return redirect(pesquisas)
    else:
        return redirect(erro)
    

def editar_pesquisa(request, id):
    usuario = request.user
    pesquisa = models.Pesquisa.objects.get(id=id)
    pesquisadores = models.Pesquisador.objects.filter(usuario=usuario)
    return render(request, 'editar_pesquisa.html', {'pesquisa': pesquisa,'pesquisadores': pesquisadores})
    
def atualizar_pesquisa(request,id):
    titulo = request.POST.get('titulo')
    datainicio = request.POST.get('datainicio')
    duracao = request.POST.get('duracao')
    orcamento = float(request.POST.get('orcamento').replace(",", "."))
    etapa = request.POST.get('etapa')
    usuario = request.user
    pesquisadores = request.POST.getlist('pesquisadores')
    npesqui = len(pesquisadores) 
    pesquisa = models.Pesquisa.objects.get(id=id)
    pesquisa.titulo= titulo
    pesquisa.data_inicio= datainicio
    pesquisa.duracao= duracao
    pesquisa.orcamento = orcamento
    pesquisa.etapa=etapa
    pesquisa.pesquisador.set(pesquisadores)
    pesquisa.save()
    return redirect(pesquisas)



@login_required
def deletar_pesquisa(request,id):
    pesquisa = models.Pesquisa.objects.filter(id=id)
    pesquisa.delete()
    return redirect(pesquisas)




@login_required
def atualizar_pesquisador(request, id):
    nome_pesq = request.POST.get('nomePesq') 
    emailpesq = request.POST.get('emailPesq') 
    # usuario = request.user
    pesquisador = models.Pesquisador.objects.get(id=id)
    pesquisador.nome_pesq = nome_pesq
    pesquisador.email = emailpesq
    pesquisador.save()
    return redirect(pesquisadores)
   
def editar_pesquisador(request, id):
    pesquisador = models.Pesquisador.objects.get(id=id)
    return render(request, 'editar_pesquisador.html', {'pesquisador': pesquisador})
    
@login_required
def deletar_pesquisador(request, id):
    pesquisador = models.Pesquisador.objects.filter(id=id)
    pesquisador.delete()
    return redirect(pesquisadores)

    
