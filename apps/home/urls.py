# -*- encoding: utf-8 -*-
"""
Copyright (c) 2019 - present AppSeed.us
"""
from . import views
from django.urls import path, re_path, include
from apps.home import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    # The home page
    path('', views.index, name='home'),
    path("archivos", views.subirArch, name = "subirArch"),
    path("fiador", views.reg_fiador, name = "fiador"),
    
    #Rutas Inquilino
    path('registro_inquilino/', views.reg_inq, name='reg_inq'),   
    path('inquilinos/', views.inquilinos, name='inquilinos'),
    path('detalles_inquilino/<str:id>', views.ver_inquilino, name='Detalles_Inquilino'), 
    path('editar_inq/<str:id>', views.editar_inq, name='editar_inq'),
    path('eliminar_inq/<str:id>', views.eliminar_inq, name='eliminar_inq'),
    
    # #Rutas Arrendador
    # path('registro_arr/', views.reg_arr, name='reg_arr'),   
    # path('arrendadores/', views.arrendadores, name='arrendadores'),
    # path('detalles_arr/<str:id>', views.ver_arrendador, name='Det_arr'), 
    # path('editar_arr/<str:id>', views.editar_arr, name='editar_arr'),
    # path('eliminar_arr/<str:id>', views.eliminar_arr, name='eliminar_arr'),


    # Rutas arrendador API
    # path('usuarios/', include('apps.api.urls')),
    
    #Rutas Inmuebles
    # path('reg_inmueble', views.reg_inmueble, name='createin'),
    # path('inmuebles/', views.listarInmueble, name='listarInmueble'),
    # path('editarin/<slug:slug>', views.editarInmueble, name='editarin'),
    # path('removerin/<id>', views.removerInmueble, name='removerin'),
    path('vistain/<slug:slug>', views.verInmueble, name='verin'),
    
   
    # Matches any html file
    re_path(r'^.*\.*', views.pages, name='pages'),
    # path("", include("apps.home.urls")), 

]
if settings.DEBUG: 
    urlpatterns += static(
        settings.MEDIA_URL, 
        document_root = settings.MEDIA_ROOT
    )