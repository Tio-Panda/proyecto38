from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name="index"),
    path('pruebas', views.pruebas, name="pruebas"),
    path('añadir-negocio', views.añadir_negocio, name="añadir_negocio"),
    path('mis-negocios', views.mis_negocios, name="mis_negocios"),
    path('mis-negocios/<int:id_negocio>', views.negocio, name="negocio"),
    path('actualizar/<str:metodo>', views.actualizar_transbank, name="actualizar"),
    path('separar-por-negocio', views.separar_por_negocio, name="separar"),
]