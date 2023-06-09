# -*- encoding: utf-8 -*-
"""
Copyright (c) 2019 - present AppSeed.us
"""

from multiprocessing import context
from django import template
from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import UserPassesTestMixin, LoginRequiredMixin
from django.http import HttpResponse, HttpResponseRedirect, HttpResponseBadRequest, JsonResponse, Http404
from django.template import loader
from django.urls import reverse
from requests import get
from .models import Inmuebles, Inquilino, Arrendador, ImagenInmueble, DocumentosInquilino, Fiador_obligado
from django.shortcuts import redirect, render, get_object_or_404
from .forms import InquilinosForm, InmueblesForm, ArrendadorForm, ImagenInmuelbeForm, FiadorForm
from . import models
from time import sleep
import os
from django.core.paginator import Paginator


def index(request):
    context = {'segment': 'index'}
    html_template = loader.get_template('home/index.html')
    return HttpResponse(html_template.render(context, request))


@login_required(login_url="/login/")
def subirArch(request):
    if request.method == "POST":
        # Fetching the form data
        ine = request.FILES["ine"]
        user = request.user
        comp_dom = request.FILES["comp_dom"]
        rfc = request.FILES["rfc"]

        # Saving the information in the database
        document = DocumentosInquilino(
            Ine=ine,
            Comp_dom=comp_dom,
            Rfc=rfc,
            user=user,
        )
        document.save()
        print(f'Archivo subido correctamente')

    documents = DocumentosInquilino.objects.all().filter(user_id=request.user)

    return render(request, "home/archivos.html", context={"files": documents})


# MODULO Inquilino #________________________________
def reg_inq(request):
    if request.method == 'POST':
        form_inq = InquilinosForm(request.POST or None)
        if form_inq.is_valid():
            print("Es valido continuar")
            form_inq = form_inq.save(commit=False)
            form_inq.user = request.user
            print(form_inq.user)
            # user = form_inq.save()
            print(form_inq)
            form_inq.save()
            sleep(3)
            print("GUARDADO CON EXITO")
            # print(user)
            return redirect('/inquilinos/')
        else:
            print("No valido")
            print(form_inq.errors)
            form_inq = InquilinosForm()
    return render(request, 'home/inquilinos.html', {'form_inq': form_inq})


def inquilinos(request):
    if request.user.is_authenticated:
        inquilinos = Inquilino.objects.all().filter(user_id=request.user)
        print(inquilinos)
        return render(request, 'home/inquilinos.html', {'inquilinos': inquilinos})
    else:
        return render(request, 'home/page-403.html')


def ver_inquilino(request, id):
    inquilino = Inquilino.objects.get(id=id)
    # personas_f=get_object_or_404(p_fisica, pk=id)
    if inquilino.user == request.user:
        print(inquilino)
        return render(request, 'home/detalles-inquilino.html', {'inquilino': inquilino})
    else:
        return render(request, 'home/page-500.html')


def editar_inq(request, id):
    # fetch the object related to passed id
    inquilinos = Inquilino.objects.all().filter(user_id=request.user)
    print(inquilinos)
    inquilino = Inquilino.objects.get(id=id)
    if inquilino.user == request.user:
        form_inq = InquilinosForm(request.POST or None, instance=inquilino)
        if form_inq.is_valid():
            form_inq = form_inq.save(commit=False)
            print(form_inq)
            form_inq.user = request.user
            print(form_inq.user)
            # user = form_inq.save()
            # obter el valor de cualquir campo en el template
            # print(request.POST['tel_empleo'])
            form_inq.save()
            sleep(3)
            print("ACTUALIZADO CON EXITO")
            # print(user)
            return redirect('/inquilinos/')
        else:
            print(" No valido")
            print(form_inq.errors)

        context = {'inquilino': inquilino, 'inquilinos': inquilinos}
        return render(request, "home/edit_inq.html", context)
    else:
        return render(request, 'home/page-500.html')


def eliminar_inq(request, id):
    inquilino = Inquilino.objects.get(id=id)
    inquilino.delete()

    return redirect('/inquilinos/')
# MODULO Fiador  #________________________________
def reg_fiador(request):
    form_fiador = FiadorForm()
 
    base = Inquilino.objects.all().filter(user_id = request.user)
    #base = Fiador_obligado.objects.all()
    print(base)
    if request.method == 'POST':
        form_fiador = FiadorForm(request.POST or None)
        if form_fiador.is_valid():
            print("Es valido continuar")
            form_fiador = form_fiador.save(commit=False)
            form_fiador.user = request.user
          
            print(form_fiador.user)
            print(form_fiador)
            form_fiador.save()
            sleep(3)
            print("GUARDADO CON EXITO")
            # print(user)
            return redirect('/fiador')
        else:
            print("No valido")
            print(form_fiador.errors)
            form_fiador = InquilinosForm()
    return render(request, 'home/MSFO.html', {'form_fiador': form_fiador, 'base': base})



# MODULO Arrendador  #________________________________
# def arrendadores(request):
#     if request.user.is_authenticated:
#         arrendadores = Arrendador.objects.all().filter(user_id=request.user)
#         print(arrendadores)
#         return render(request, 'home/arrendador.html', {'arrendadores': arrendadores})
#     else:
#         return render(request, 'home/page-403.html')


# def reg_arr(request):
#     if request.method == 'POST':
#         form_arr = ArrendadorForm(request.POST or None)
#         if form_arr.is_valid():
#             print("Es valido continuar")
#             form_arr = form_arr.save(commit=False)
#             form_arr.user = request.user
#             print(form_arr.user)
#             # user = form_arr.save()
#             print(form_arr)
#             form_arr.save()
#             sleep(3)
#             print("GUARDADO CON EXITO")
#             # print(user)
#             return redirect('/arrendadores/')
#         else:
#             print("No valido")
#             print(form_arr.errors)
#             form_arr = ArrendadorForm()
#     return render(request, 'home/arrendador.html', {'form_arr': form_arr})


# def ver_arrendador(request, id):
#     arrendador = Arrendador.objects.get(id=id)
#     # personas_f=get_object_or_404(p_fisica, pk=id)
#     if arrendador.user == request.user:
#         print(arrendador)
#         return render(request, 'home/detalles-arrendador.html', {'arrendador': arrendador})
#     else:
#         return render(request, 'home/page-403.html')


# def editar_arr(request, id):
#     # fetch the object related to passed id
#     arrendadores = Arrendador.objects.all().filter(user_id=request.user)
#     print(arrendadores)
#     arrendador = Arrendador.objects.get(id=id)
#     if arrendador.user == request.user:
#         form_arr = ArrendadorForm(request.POST or None, instance=arrendador)
#         if form_arr.is_valid():
#             form_arr = form_arr.save(commit=False)
#             print(form_arr)
#             form_arr.user = request.user
#             print(form_arr.user)
#             # user = form_inq.save()
#             # obter el valor de cualquir campo en el template
#             # print(request.POST['tel_empleo'])
#             form_arr.save()
#             sleep(3)
#             print("ACTUALIZADO CON EXITO")
#             # print(user)
#             return redirect('/arrendadores/')
#         else:
#             print(" No valido")
#             print(form_arr.errors)

#         context = {'arrendador': arrendador, 'arrendadores': arrendadores}
#         return render(request, "home/edit_arr.html", context)
#     else:
#         return render(request, 'home/page-500.html')


# def eliminar_arr(request, id):
#     arrendador = Arrendador.objects.get(id=id)
#     arrendador.delete()

#     return redirect('/arrendadores/')


# Modulo Inmuebles#________________________________

def reg_inmueble(request):
    user = request.user
    inmuebles = Inmuebles.objects.filter(user=request.user, alias_inmueble=request.POST['alias_inmueble'])
    print("query de inmuebles",inmuebles)
    print(inmuebles.first())
    print("soy request de alias",request.POST['alias_inmueble'])
   
   
    if inmuebles:
        print("NO carnal, ese Alias de inmueble ya inmueble ya existe")
        alias_inmueble = request.POST['alias_inmueble'] + "" + str(inmuebles.count())
        print("nuevo nombre",alias_inmueble)
         
    if request.method == 'POST':
        form = InmueblesForm(request.POST)
        fotos_form = ImagenInmuelbeForm(request.POST, request.FILES)
        images = request.FILES.getlist('imagenes')  # field name in model
        img = len(images)
        print(img)
        if img <= 5:
            if form.is_valid() and fotos_form.is_valid():
                print("valido")
                inmueble_instance = form.save(commit=False)
                inmueble_instance.user = user
                if inmuebles:
                    inmueble_instance.alias_inmueble = alias_inmueble
                inmueble_instance.save()
                for f in images:
                    foto_instance = ImagenInmueble(imagenes=f, inmueble=inmueble_instance)
                    print(foto_instance)
                    foto_instance.user = user
                    foto_instance.save()
                sleep(1)
                return redirect('/inmuebles/')
            else:
                print("No valido")
                print(form.errors)
                form = InquilinosForm()
                fotos_form = ImagenInmuelbeForm()
        else:
            return render(request, 'home/page-007.html')

    return render(request, 'home/page-007.html', {'form': form, 'fotos_form': fotos_form})


def listarInmueble(request):
    inmuebles = Inmuebles.objects.all().filter(user_id=request.user)
    print(inmuebles)
    lookup_field = 'slug'
    # registros = request.POST.get('no_registros',5)
    records_per_page = request.GET.get('records_per_page', 5)
    records_per_page = int(records_per_page)
    page = request.GET.get('page', 1)

    print("registros", records_per_page)
    print("page", page)
    try:
        # paginator = Paginator(inmuebles, registros) # Show 25 contacts per page.
        paginator = Paginator(inmuebles, records_per_page)
        page_obj = paginator.get_page(page)
        print("yo soy page obj", page_obj)

    except:
        raise Http404
    return render(request, 'home/inmuebles.html',
                  {'page_obj': page_obj, 'records_per_page': records_per_page, 'paginator': paginator})


def verInmueble(request, slug):
    verinmueble = Inmuebles.objects.filter(user_id=request.user).get(slug=slug)
    print(verinmueble)
    print("yo soy", verinmueble.id)
    return render(request, 'home/detalles-inmueble.html', {'verinmueble': verinmueble})


def editarInmueble(request, slug):
    # consulta slug
    print("Esta en editar")
    verinmueble = Inmuebles.objects.filter(user_id=request.user).get(slug=slug)
    # asignar id desde la consulta slug
    id = verinmueble.id
    # consulta tabla
    inmuebles = Inmuebles.objects.all().filter(user_id=request.user)
    # consulta objeto a editar
    objin = Inmuebles.objects.get(id=id)
    print("Paso a 5")
    imagen = get_object_or_404(ImagenInmueble, pk=11)
    print("Paso a 6")
    fotos_old = ImagenInmueble.objects.all().filter(inmueble_id=11)
    print("Paso a 7")
    # print(fotos_old.__getitem__(4).imagenes)
    print("contador de fotos old", fotos_old.count())
    print("imagen imagenes", imagen.imagenes)
    if request.method == 'POST':
        form = InmueblesForm(request.POST or None, instance=objin)
        fotos_form = ImagenInmuelbeForm(request.POST, request.FILES, instance=imagen)

        if fotos_old.count() <= 5:
            if form.is_valid() and fotos_form.is_valid():
                print("valido")
                inmueble_instance = form.save(commit=False)
                inmueble_instance.user = request.user
                inmueble_instance.save()
                ids_eliminar = request.POST.getlist('eliminar[]')
                print("ids a eliminar", ids_eliminar)
                imagenes_eliminar = ImagenInmueble.objects.filter(id__in=ids_eliminar)
                print("imagenes a eliminar", imagenes_eliminar)
                if imagenes_eliminar != 0:
                    for imagen in imagenes_eliminar:
                        imagen.delete()
                        os.remove(imagen.imagenes.path)
                        print("se elimino correctamente la imagen", imagen)

                images = request.FILES.getlist('imagenes')  # field name in model
                img = len(images)
                print("imagens a cargar:", img)
                contador = fotos_old.count()
                print("contadador 2: =", contador)
                contador2 = 5 - contador
                if contador != 5 or contador2 != 0:
                    if img <= contador2:
                        for f in images:
                            foto_instance = ImagenInmueble(imagenes=f, inmueble=inmueble_instance)
                            print(foto_instance)
                            foto_instance.user = request.user
                            foto_instance.save()

                    else:
                        return render(request, 'home/page-007.html')
                sleep(2)
                return redirect('/inmuebles/')
            else:
                print("No valido")
                print(form.errors)
                form = InquilinosForm()
                fotos_form = ImagenInmuelbeForm()
        else:
            messages.error(request, 'Se ha producido un error. Por favor solo subir 5 Fotos como MAXIMO ')

    context = {'objin': objin, 'inmuebles': inmuebles, 'verinmueble': verinmueble}

    return render(request, "home/edit_inmueble.html", context)


def removerInmueble(request, id):
    objin = Inmuebles.objects.get(id=id)
    objin.delete()

    return HttpResponseRedirect(reverse('listarInmueble'))



def pages(request):
    context = {}
    # All resource paths end in .html.
    # Pick out the html file name from the url. And load that template.
    try:

        load_template = request.path.split('/')[-1]
        if load_template == 'admin':
            return HttpResponseRedirect(reverse('admin:index'))
        context['segment'] = load_template

        html_template = loader.get_template('home/' + load_template)
        return HttpResponse(html_template.render(context, request))

    except template.TemplateDoesNotExist:

        html_template = loader.get_template('home/page-404.html')
        return HttpResponse(html_template.render(context, request))

    except:
        html_template = loader.get_template('home/page-500.html')
        return HttpResponse(html_template.render(context, request))
