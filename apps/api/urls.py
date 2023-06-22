
"""
Copyright (c) 2019 - present AppSeed.us
"""
from . import views
from django.urls import path 
from ..api.routers import *
from django.urls import include
urlpatterns = [
    path('v1/inquilino_registro/', views.inquilino_registro.as_view()), 
    path('v1/inquilinos_delete/', views.inquilinos_delete.as_view()),
    path('v1/inq_list/', views.inquilinos_list_all),
    path('v1/editar_inquilino/', views.editar_inquilino),

   # path('tus/<int:pk>/', views.DocumentosInquilino.as_view({'put': 'actualizar'}), name='update'),
   #path('documentos_edit/<int:pk>/', views.DocumentosInquilino.as_view({'put': 'actualizar_archivos_individual'}), name='actualizar_archivos_individual'),
    path('actualizar_status/<str:slug>/', views.inmueblesViewSet.as_view({'put': 'actualizar_status'}), name='actualizar_status'),
    path('listar_documentos/buscar/', Listar_Documentos_ViewSet.as_view({'get': 'buscar'}), name='buscar-documentos'),
    # path('inmuebles/datos_inmueble/<str:slug>/', InmueblesViewSet.as_view({'get': 'datos_inmueble'}), name='datos_inmueble'),
    # -*- encoding: utf-8 -*-
    
    
    path('', include(router.urls)),
]

# urlpatterns += router.urls