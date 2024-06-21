"""
URL configuration for tcc project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.urls import path, include
from . import views
from django.contrib import admin
from django.contrib.auth import logout

urlpatterns = [
    path('admin/',admin.site.urls),
    path('',views.index, name="index"),
    path('login/',views.irlogin, name="irlogin"),
    path('login/',views.logar, name="logar"),
    path('home/',views.home, name="home"),
    path('novouser/',views.novouser, name="novouser"),
    path('cadastrar/',views.cadastrar, name="cadastrar"),
    path('caduser/',views.caduser, name="caduser"),
    path('loguser/',views.loguser, name="loguser"),
    path('logout/',views.logout_view, name="logout"),
    path('roadmap/',views.roadmap, name="roadmap"),
    path('pesquisadores/', views.pesquisadores, name='pesquisadores'),
    path('salvar_pesquisador/', views.salvar_pesquisador, name="salvar_pesquisador"),
    path('editar_pesquisador/', views.editar_pesquisador, name="editar_pesquisador"),
    path('deletar_pesquisador/<int:id>', views.deletar_pesquisador, name="deletar_pesquisador"),
    path('pesquisas/', views.pesquisas, name="pesquisas"),
    path('salvar_pesquisa/', views.salvar_pesquisa, name="salvar_pesquisa"),
    path('erro/', views.erro, name="erro"),

]
