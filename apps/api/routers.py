from rest_framework.routers import DefaultRouter
from ..api.views import *

# router = routers.SimpleRouter()
# router.register(r'users', ListarLibrosSet, basename='user')
# urlpatterns += router.urls

router = DefaultRouter()
router.register(r'inquilino_fiador_obligado', InquilinoFiadorObligadoViewSet, basename='inquilino_fiador_obligado')
router.register(r'arrendadores_campos_establecidos', ArrendadorCamposUnicosViewSet, basename='arrendadores_campos_establecidos')
router.register(r'fiadores_obligados', Fiador_obligadoViewSet, basename='fiadores_obligados')

router.register(r'documentos_reg', DocumentosInquilino, basename='documentos_reg')

router.register(r'inquilino_fiador_obligado', InquilinoFiadorObligadoViewSet, basename='inquilino_fiador_obligado')
router.register(r'arrendadores_campos_establecidos', ArrendadorCamposUnicosViewSet, basename='arrendadores_campos_establecidos')
router.register(r'Arrendador_Api', ArrendadorViewSet, basename='Arrendador_Api')

# Fiadores obligados
router.register(r'fiadores_obligados', Fiador_obligadoViewSet, basename='fiadores_obligados')
# Documentos arrendador
router.register(r'documentos_arrendador', DocumentosArrendadorViewSet, basename='documentos_arrendador')
# Inmuebles
router.register(r'inmuebles_viewset', inmueblesViewSet, basename='inmuebles54')
# Listar documentos
router.register(r'listar_documentos', Listar_Documentos_ViewSet, basename='PruebaListar'),
# Historial documentos arrendador
router.register(r'HistorialDocumentosArrendadorViewSet', HistorialDocumentosArrendadorViewSet, basename='HistorialDocumentosArrendadorViewSet'),

# router.register(r'HistorialDocumentosInquilinoViewSet', HistorialDocumentosInquilinoViewSet, basename='HistorialDocumentosInquilinoViewSet')
router.register(r'documentos_foo', DocumentosFoo, basename='base_foo')

router.register(r'MobiliarioCantidad', MobiliarioCantidad, basename='MobiliarioCantidad')


# router.register(r'i_a', Inmuebles_a, basename='a_a')


# router.register(r'ListarInmuieblesImagenesArrendador', ListarInmuieblesImagenesArrendador, basename='ListarInmuieblesImagenesArrendador')

# Cambiar a v1/

# myobjects_list = ArrendadorViewSet.as_view({
#     'get': 'list',
#     'get': 'retrieve'
# })