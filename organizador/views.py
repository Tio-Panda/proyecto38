from django.shortcuts import render, redirect
from login.models import Rutas
from .models import Negocios
from .forms import NegociosForm
from .functions import *

def index(request):
    return render(request, 'index.html')

def pruebas(request):
    if request.method == 'POST':
        archivo = request.FILES['archivo']
        print(archivo.name)

        import pandas as pd

        data = pd.read_csv(archivo, header = 0, sep = ",")
        print(data.head())
        print(data.describe())       

    return render(request, 'pruebas.html')

# ----- Negocios ------ #

def añadir_negocio(request):
    if request.method == 'POST':
        form = NegociosForm(request.POST)
        if form.is_valid():
            nuevo_negocio = form.save(commit=False)
            nuevo_negocio.dueño = request.user
            nuevo_negocio.transbank = crear_archivo_csv(request.user, nuevo_negocio.nombre, 'transbank')
            nuevo_negocio.efectivo = crear_archivo_csv(request.user, nuevo_negocio.nombre, 'efectivo')
            nuevo_negocio.save()

            return redirect('mis_negocios')

    else:
        form = NegociosForm()

    context = {'form' : form}    
    return render(request, 'añadir_negocio.html', context)

def mis_negocios(request):
    negocios = Negocios.objects.filter(dueño=request.user)
    context = {'negocios' : negocios}
    return render(request, 'mis_negocios.html', context)

def negocio(request, id_negocio):
    negocio = Negocios.objects.get(id=id_negocio)

    if request.method == 'POST':
        seleccion = request.POST
        fecha_inicio = seleccion['fecha_inicio']
        fecha_final = seleccion['fecha_final']
        aux = list(seleccion.keys())
        intervalo = aux[3]
        print(intervalo)
        print(fecha_inicio)
        print(fecha_final)
        
        k = mostrar_info(negocio.transbank, fecha_inicio, fecha_final, intervalo)

        print(k)
        
    
    context = {'negocio' : negocio, 'fecha' : k['fecha'], 'neto' : k['neto'], 'iva' : k['iva'], 'total' : k['total'], 'volumen' : k['volumen']}
    return render(request, 'negocio.html', context)

def actualizar_transbank(request, metodo):
    rutas = Rutas.objects.get(usuario=request.user)

    if request.method == 'POST':
        archivos = request.FILES.getlist('archivos')
        ruta_master = rutas.master + "/transbank.csv"
        guardar_archivos_cache(archivos, request.user.username)
        fusionar_csv(ruta_master, rutas.cache)
        return redirect('separar')

    context = {'negocio' : ""}
    return render(request, 'subir_archivos.html', context)

def separar_por_negocio(request):
    rutas = Rutas.objects.get(usuario=request.user)
    negocios = Negocios.objects.filter(dueño=request.user)

    ruta_master = rutas.master + "/transbank.csv"   
    nombres = separar_csv_por_negocio(ruta_master)

    if request.method == 'POST':
        seleccion = request.POST

        for negocio in negocios:
            ruta_negocio = negocio.transbank
            nombre_selecto = seleccion[negocio.nombre]
            if not nombre_selecto == "null":
                distribuir_csv_por_negocio(ruta_master, ruta_negocio, nombre_selecto)

        return redirect('mis_negocios')
        

    context = {'negocios' : negocios, 'nombres': nombres}
    return render(request, 'separar_por_negocio.html', context)

