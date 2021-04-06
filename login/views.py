from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from .forms import UserRegisterForm
from .models import *
from .functions import *

def signin(request):
    if request.method == 'POST':
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data['username']

            usuario = User.objects.get(username=username)
            master = crear_carpeta(username, "master")
            cache = crear_carpeta(username, "cache")
            crear_archivo_csv(username, "master", "transbank")
            crear_archivo_csv(username, "master", "efectivo")
            rutas = Rutas(usuario=usuario, master=master, cache=cache)
            rutas.save()

            return redirect('index')
    else:
        form = UserRegisterForm()

    context = { 'form' : form }
    return render(request, 'signin.html', context)

def login(request):
    return render(request, 'login.html')
