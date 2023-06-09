from django.shortcuts import render
from rest_framework.response import Response
from rest_framework.views import APIView
from .serializers import *
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.renderers import JSONRenderer
import io
from rest_framework.parsers import JSONParser
from rest_framework.exceptions import ValidationError
from django.shortcuts import get_object_or_404

from ..home.models import *
from rest_framework import status

from rest_framework import viewsets

from rest_framework.authentication import TokenAuthentication,SessionAuthentication
from rest_framework.permissions import IsAuthenticated
from apps.authentication.authentication_mixins import Authentication

from rest_framework.decorators import action
from django.core.paginator import Paginator
import json
# Create your views here.

import json
import shutil
# Para autenticacion
import os


class inquilino_registro(APIView):
    authentication_classes = [TokenAuthentication, SessionAuthentication]
    permission_classes = [IsAuthenticated]
    
    def post(self, request, format=None):
        user_session = request.user

       # request.data.user = user_session
        print("request inquilino", request.data)
        serializer3 = InquilinoSerializers(data=request.data)
        if serializer3.is_valid():
            print("valido")
            nombre = serializer3.validated_data['nombre']
        
            if len(nombre) > 0:
                print(nombre)
                serializer3.save(user = user_session)
                return Response(serializer3.data, status=status.HTTP_201_CREATED)
            else:
                print("Nombre no valido")
                return Response("Nombre vacio", status=status.HTTP_400_BAD_REQUEST)
        else:
            print("no valido")
            return Response(serializer3.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET'])
def inquilinos_list_all(request):
    """
    List all code snippets, or create a new snippet.
    """
    user_session = request.user
    if request.method == 'GET':
        if user_session.is_staff:
            snippets = Inquilino.objects.all()
            serializer = InquilinoSerializers(snippets, many=True)
            return Response(serializer.data)
        else:
            snippets = Inquilino.objects.all().filter(user_id = user_session)
            serializer = InquilinoSerializers(snippets, many=True)
            return Response(serializer.data)

@api_view(['POST'])
# @renderer_classes([JSONRenderer])
def editar_inquilino(request):
    print("Yo soy request", request.data)
    id = request.data.get('id')
    print("Valor de la id", id)
    inquilino = Inquilino.objects.get(id=id)
    print("Inquilinos: ", inquilino)
    user_serializer = InquilinoSerializers(inquilino, data=request.data)

    if user_serializer.is_valid():
        user_serializer.save()
        print("Guardo Inquilino")
        return Response(user_serializer.data, status=status.HTTP_200_OK)
    print("No guardo Inquilino xD")
    return Response(user_serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class inquilinos_delete(APIView):

    def post(self, request, format=None):
        print("Si llega a eliminar", request.data)
        id = request.data.get('id')
        print("Valor de la id", id)
        post = Inquilino.objects.get(id=id)
        post.delete()
        print("Post", post)
        return Response(status=status.HTTP_204_NO_CONTENT)


class InquilinoFiadorObligadoViewSet(viewsets.ModelViewSet):
    authentication_classes = [TokenAuthentication, SessionAuthentication]
    permission_classes = [IsAuthenticated]
    queryset = Inquilino.objects.all()
    serializer_class = InquilinoSerializersFiador
    http_method_names = ['get']

    def list(self, request, *args, **kwargs):
        user_session = request.user
        if user_session.is_authenticated:
            print(user_session.id)
            fiador_obligado = Inquilino.objects.all().filter(user_id = user_session.id )
            serializer = self.get_serializer(fiador_obligado, many=True)
            return Response(serializer.data)
        else:
            return Response(status=status.HTTP_403_FORBIDDEN)

# class DocumentosInquilino(Authentication,viewsets.ModelViewSet): Con autenticacion integrada
class DocumentosInquilino(viewsets.ModelViewSet):
    authentication_classes = [TokenAuthentication, SessionAuthentication]
    permission_classes = [IsAuthenticated]
    queryset = DocumentosInquilino.objects.all()
    serializer_class = DocumentosInquilinosSerializer
    # ser_2 = DocumentosInquilinoSerializer
    
    def list(self, request, *args, **kwargs):
        content = {
            'user': str(request.user),
            'auth': str(request.auth),
        }
        queryset = self.filter_queryset(self.get_queryset())
        InquilinoSerializers = self.get_serializer(queryset, many=True)
       
        return Response(InquilinoSerializers.data ,status=status.HTTP_200_OK)
    
    def create (self, request, *args, **kwargs):
        user_session = str(request.user.id)
        print(user_session)
        try: 
            data = request.data
            print("primer print",data)
            data = {
                    "Ine": request.FILES.get('Ine', None),
                    "Comp_dom": request.FILES.get('Comp_dom', None),
                    "Rfc": request.FILES.get('Rfc', None),
                    "Ingresos": request.FILES.get('Ingresos', None),
                    "Extras": request.FILES.get('Extras', None),
                    "Recomendacion_laboral": request.FILES.get('Recomendacion_laboral', None),
                    "inquilino":request.data['inquilino'],
                    "user":user_session
                }
            print("segundo print",data)
            if data:
                documentos_serializer = self.get_serializer(data=data)
                documentos_serializer.is_valid(raise_exception=True)
                documentos_serializer.save()
                return Response(documentos_serializer.data, status=status.HTTP_201_CREATED)
            else:
                return Response({'error': 'No file provided'}, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)
        

    def destroy(self, request, pk=None, *args, **kwargs):
        # try:
        documentos_inquilinos = self.get_object()
        documento_inquilino_serializer = self.serializer_class(documentos_inquilinos)
        print("Soy ine", documento_inquilino_serializer.data['ine'])
        print("1")
        if documentos_inquilinos:
            ine = documento_inquilino_serializer.data['ine']
            print("Soy ine 2", ine)
            comp_dom= documento_inquilino_serializer.data['comp_dom']
            rfc= documento_inquilino_serializer.data['escrituras_titulo']
            print("Soy RFC", rfc)
            ruta_ine = 'apps/static'+ ine
            print("Ruta ine", ruta_ine)
            ruta_comprobante_domicilio = 'apps/static'+ comp_dom
            ruta_rfc = 'apps/static'+ rfc
            print("Ruta com", ruta_comprobante_domicilio)
            print("Ruta RFC", ruta_rfc)
            os.remove(ruta_ine)
            os.remove(ruta_comprobante_domicilio)
            os.remove(ruta_rfc)
            # self.perform_destroy(documentos_arrendador)  #Tambien se puede eliminar asi
            documentos_inquilinos.delete()
            return Response({'message': 'Archivo eliminado correctamente'}, status=204)
        else:
            return Response({'message': 'Error al eliminar archivo'}, status=400)
        # except Exception as e:
        #     return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)
        
        
    def retrieve(self, request, pk=None):
        try:
            # documentos = self.queryset #Toma los datos de Inmuebles.objects.all() que esta al inicio de la clase viewset
            # inquilino = documentos.filter(id=pk)
            # serializer_inquilino = DISerializer(inquilino, many=True)
            # print(serializer_inquilino.data)
            # # ine = serializer_inquilino.data[0]['ine']
            # # print(ine)
            # # documentos_arrendador = self.get_object()
            # # print(documentos_arrendador)
            # return Response(serializer_inquilino.data)
            instance = self.get_object()
            serializer_inquilino = self.get_serializer(instance)
            return Response(serializer_inquilino.data)
        
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)
    
    # @action(detail=False, methods=['put'], url_path='actualizar_archivos_individual')
    # def actualizar_archivos_individual(self, request, pk=None, *args, **kwargs):
    #     instance = self.get_object()
    #     print(instance)
    #     data = {}
    #     fields = ['Ine', 'Comp_dom', 'Rfc']

    #     for field in fields:
    #         print("si hay campos",field)
            
    #         if field in request.FILES:
    #             print("si hay campos 2",field)
    #             data[field] = request.FILES[field]
    #             print(data[field])

    #     data['user'] = request.user.id

    #     serializer = self.get_serializer(instance, data=data, partial=True)
    #     if serializer.is_valid(raise_exception=True):
    #         serializer.save()
    #         return Response(serializer.data)
    #     else:
    #         return Response(serializer.errors)
    
    # def update(self, request, *args, **kwargs):
    #     instance = self.get_object()
    #     serializer = self.get_serializer(instance, data=request.data, partial=True)
    #     serializer.is_valid(raise_exception=True)
    #     print(request.data)
        
    #     # Verificar si se proporciona un nuevo archivo adjunto
    #     if 'Ine' in request.data:
    #         print("soy ine")
    #         Ine = request.data['Ine']
    #         instance.Ine = Ine  # Actualizar el archivo adjunto sin eliminar el anterior
            
    #     if 'Comp_dom' in request.data:
    #         Comp_dom = request.data['Comp_dom']
    #         instance.Comp_dom = Comp_dom  # Actualizar el archivo adjunto sin eliminar el anterior
            
    #     if 'Rfc' in request.data:
    #         Rfc = request.data['Rfc']
    #         instance.Rfc = Rfc  # Actualizar el archivo adjunto sin eliminar el anterior
        
    #     if 'Extras' in request.data:
    #         Extras = request.data['Extras']
    #         instance.Extras = Extras  # Actualizar el archivo adjunto sin eliminar el anterior
        
    #     if 'Ingresos' in request.data:
    #         Ingresos = request.data['Ingresos']
    #         instance.Ingresos = Ingresos  # Actualizar el archivo adjunto sin eliminar el anterior
        
    #     if 'Recomendacion_laboral' in request.data:
    #         print("si entre")
    #         Recomendacion_laboral = request.data['Recomendacion_laboral']
    #         instance.Recomendacion_laboral = Recomendacion_laboral  # Actualizar el archivo adjunto sin eliminar el anterior
        
    #     serializer.update(instance, serializer.validated_data)
    #     print(serializer.data['Ine'])# Actualizar el archivo adjunto sin eliminar el anterior
    #     return Response(serializer.data)
    
    def update(self, request, *args, **kwargs):
        try:
            instancia_anterior = self.get_object()  # Obtén la instancia anterior
            data = {field: request.FILES[field] for field in ['Ine', 'Comp_dom', 'Rfc', 'Ingresos', 'Extras', 'Recomendacion_laboral'] if field in request.FILES}
                                                        #    Ine  Comp_dom Rfc Buro Recomendacion_laboral
            data['user'] = request.user.id
            data['inquilino_id'] = request.data.get('inquilino')
            print("Request data", request.data)
            user_id = request.user.id
            print("Soy user id inquilino", user_id)
            serializer = self.get_serializer(instancia_anterior, data=data, partial=True)
            if HistorialDocumentosInquilinos.objects.filter(previo_Ingresos__isnull=False, historial_documentos=request.data.get('inquilino')).count() < 4:
                if serializer.is_valid(raise_exception=True):
                    print("Hola")
                    for field in ['Ingresos']:
                        print("Entrando a el for")
                        if field in data and getattr(instancia_anterior, field) != serializer.validated_data.get(field): #getattr  permite obtener el valor de un atributo indicando su nombre como una cadena
                            self.guardar_historial(getattr(instancia_anterior, field), serializer.validated_data.get(field), 'previo_' + field)
                            print("Si entro a editar")
                    serializer.save()
                    return Response(serializer.data)
                else:
                    return Response(serializer.errors)
            else:
                return Response({"error": "No se permiten más de 3 modificaciones de archivos."})
        except Exception as e:
            return Response({'Error': 'Error al actualizar'})
    
    # def guardar_historial(self, archivo_anterior, archivo_actual, campo_previo, user_id):
    #     if archivo_anterior:
    #         # Crear una nueva instancia de HistorialDocumentosArrendador
    #         historial = HistorialDocumentosInquilinos.objects.create(
    #             historial_documentos = self.get_object(),
    #             previo_Ingresos = archivo_anterior if campo_previo == 'previo_Ingresos' else None,
    #             user_id = user_id,
    #         )
    def guardar_historial(self, archivo_anterior, archivo_actual, campo_previo):
        if archivo_actual != archivo_anterior:
            # Eliminar el archivo anterior
            if archivo_anterior:
                os.remove(archivo_anterior.path)

            if campo_previo == 'previo_Ingresos':
                # Crear una nueva instancia de HistorialDocumentosArrendador
                historial = HistorialDocumentosArrendador.objects.create(
                    historial_documentos = self.get_object(),
                    previo_Ingresos = archivo_anterior if campo_previo == 'previo_Ingresos' else None,
                )

# Vista para arrendador ------------------------------------------------------------------------------------------------------------------------------------------------?

class ArrendadorCamposUnicosViewSet(viewsets.ModelViewSet):
    queryset = Arrendador.objects.all()
    serializer_class = ArrendadorConCamposEstablecidosSerializer
    http_method_names = ['get']

    def list(self, request, *args, **kwargs):
        try:    
            queryset = self.filter_queryset(self.get_queryset())
            arrendador_serializer = self.get_serializer(queryset, many=True)
            return Response(arrendador_serializer.data ,status=status.HTTP_201_CREATED)
        except Exception as e:
            return Response(e, status=status.HTTP_400_BAD_REQUEST)
        

class ArrendadorViewSet(viewsets.ModelViewSet):
    lookup_field = 'slug'
    queryset = Arrendador.objects.all()
    serializer_class = ArrendadorSerializer

    def list(self, request):
        try:
            queryset = self.filter_queryset(self.get_queryset())
            arrendador_serializer = self.get_serializer(queryset, many=True)
            return Response(arrendador_serializer.data ,status=status.HTTP_201_CREATED)
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)
        
    def update(self, request, *args, **kwargs):
        try:
            instance = self.get_object()
            serializer = self.get_serializer(instance, data=request.data, partial=True)
            serializer.is_valid(raise_exception=True)
            self.perform_update(serializer)
            print("edito arrendador ")
            return Response(serializer.data, status=status.HTTP_200_OK)
        except ValidationError as e:
            return Response({'errors': e.detail}, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)

    def create(self, request, *args, **kwargs):
        try:
            print("Llegando a create arrendador")
            request.data['user'] = request.user.id
            arrendador_serializer = self.get_serializer(data=request.data) # Usa el serializer_class
            if arrendador_serializer.is_valid(raise_exception=True):
                arrendador_serializer.save()
                print("Guardado arrendador")
                arrendador = arrendador_serializer.instance

                validacion_arrendador = ValidacionArrendador(arrendador_validacion=arrendador)
                validacion_arrendador.user_id = request.user.id
                validacion_arrendador.save()

                return Response({'arrendador': arrendador_serializer.data, 'validacion_arrendador': validacion_arrendador.id}, status=status.HTTP_201_CREATED)
            else:
                print("Error al crear arrendador")
                return Response({'errors': arrendador_serializer.errors})
        except ValidationError as e:
            return Response({'errors': e.detail}, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)
        
    def retrieve(self, request, slug=None, *args, **kwargs):
        try:
            print("Entrando a retrieve")
            modelos = self.queryset #Toma los datos de Inmuebles.objects.all() que esta al inicio de la clase viewset
            arrendador = modelos.filter(slug=slug)
            if arrendador:
                arrendador_serializer = self.serializer_class(arrendador, many=True)
                return Response(arrendador_serializer.data, status=status.HTTP_200_OK)
            else:
                return Response({'message': 'No hay persona con esos datos'}, status = status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)
        
    def destroy (self,request, *args, **kwargs):
        try:
            print("Esta entrando a eliminar")
            arrendador = self.get_object()
            if arrendador:
                arrendador.delete()
                return Response({'message': 'Arrendador eliminado'}, status=204)
            return Response({'message': 'Error al eliminar'}, status=400)
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)

# ---------------------------------- Vistas para Inmuebeles ---------------------------------- #


class inmueblesViewSet(viewsets.ModelViewSet):
    # authentication_classes = [TokenAuthentication, SessionAuthentication]
    # permission_classes = [IsAuthenticated]
    lookup_field = 'slug'
    queryset = Inmuebles.objects.all()
    serializer_class = InmueblesSerializer
    queryset_imagenes = ImagenInmueble.objects.all()
    serializer_class_imagen = ImagenInmuebleSerializer

    
    # def get_queryset(self):
    #     # user_id = self.request.user.id
    #     # queryset = Inmuebles.objects.filter(user_id=user_id)
    #     # return queryset
        # return self.queryset.filter(user_id=self.request.user.id)

    # def get_queryset(self):
    #     user_session = self.request.user
    #     if user_session.is_staff:
    #         data_serializer = self.serializer_class(self.queryset, many=True)
    #         return Response(data_serializer.data)
    #     else:            
    #         user_id = self.request.user.id
    #         return Inmuebles.objects.filter(user_id=user_id)
    # def get_queryset(self):
        # return self.queryset.filter(user_id=self.request.user.id)
        # user_id = self.request.user.id
        # return Inmuebles.objects.filter(user_id=user_id)

    def create (self, request, *args, **kwargs):
        data = request.data
        data['user'] = request.user.id
        try:
            print("Esta llegando a create")
            print("id user es:",request.user.id)
            data = request.data
            # print(data)
            data['user'] = request.user.id
            # request.data['user'] = request.user.id
            img = request.FILES.get('imagenes', None)
            if img:
                image_data = data.pop('imagenes')
            print("2")
            data = request.data.copy()  # Crear una copia mutable de request.data
            if data.get('reglamento_interno') == 'undefined':
                del data['reglamento_interno']
            
            if data.get('mobiliario') == 'undefined':
                del data['mobiliario']
                
            inmueble_serializer = self.get_serializer(data=data) #Usa el serializer_class 
            if inmueble_serializer.is_valid(raise_exception=True):
                inmueble = inmueble_serializer.save()
                print("1")
            else:
                return(inmueble_serializer.errors)
            data2 = {
                "imagenes": request.FILES.get('imagenes', None),
                "inmueble": inmueble.id
            }
            imagen_serializer = ImagenInmuebleSerializer(data=data2)
            imagen_serializer.is_valid(raise_exception=True)
            imagen_serializer.save()
            return Response({'inmuebles': inmueble_serializer.data, 'imagen': imagen_serializer.data},
                            status=status.HTTP_201_CREATED)
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)
    
    def destroy(self, request, slug=None, *args, **kwargs):
        try:
            print("Esta entrando a eliminar Inmueble")
            inmueble = get_object_or_404(Inmuebles.objects.all(), slug=slug)
            print("Soy inmueble", inmueble)
            if inmueble:
                inmueble.delete()
                print("Elimino correctamente")
                return Response({'message': 'Inmueble eliminado correctamente'}, status=204)
            return Response({'message': 'Error al eliminar inmueble'}, status=400)
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)
        
    def retrieve(self, request, slug=None, *args, **kwargs):
        try:
            print("Entrando a retrieve")
            modelos = self.queryset #Toma los datos de Inmuebles.objects.all() que esta al inicio de la clase viewset
            inmueble = modelos.filter(slug=slug)
            serializer_inmueble = InmueblesSerializer(inmueble, many=True)
            id = serializer_inmueble.data[0]['id']
            imagenes = self.queryset_imagenes.filter(inmueble_id=id)
            serializer_img = ImagenInmuebleSerializer(imagenes, many=True)
            total_imagenes = imagenes.count()
            context = {"inmueble": serializer_inmueble.data,
                    "fotos_inmueble": serializer_img.data}  # create dictionary with values
            dta = {}
            dta['inmueble'] = serializer_inmueble.data
            dta['fotos'] = serializer_img.data
            dta['total_imagenes'] = total_imagenes
            # data = {'data': context}
            # return render(request, 'home/edit_inmueble.html', {'data': dta})
            return Response({'inmuebles': serializer_inmueble.data, 'imagen': serializer_img.data, 'total_imagenes':total_imagenes},
                            status=status.HTTP_201_CREATED)
        except Exception as e:
            return Response({'Error': str(e)}, status=status.HTTP_400_BAD_REQUEST)
    
        
    def update(self, request, *args, **kwargs):
        # print("Esta entrando a update Inmueble")
        try: 
            data_string = request.data.get('eliminar_imagenes')
            data2 = json.loads(data_string)
            id_inmeble = request.data.get('id')
            print(request.data)
            if len(data2) != 0:
                for key , value in data2.items():
                    print("Valor de las id a eliminar", value)
                    imagenes = self.queryset_imagenes.filter(inmueble_id=id_inmeble)
                    if imagenes.count() > 1:
                        imagen = self.queryset_imagenes.filter(id=value)
                        img_ser = self.serializer_class_imagen(imagen, many=True)
                        ur = img_ser.data[0]['imagenes']
                        print("Soy la url" ,ur)
                        imagen.delete() 
                        c = 'apps/static' + ur
                        os.remove(c)
            print("Actualizar datos Inmueble")
            # id = request.data.get('id')
            data = request.data
            print("Soy nuevamente data", data)
            if request.FILES.get('imagenes', None) is not None:
                image_data = data.pop('imagenes')
            eli_img = request.data.get('id')
            print("Soy id imagen", eli_img)
            # print(modelos)
            # inmueble = self.get_object()
            id_inmueble = request.data.get('id')
            inmueble = self.queryset.get(id = id_inmueble)
            print("Soy inmueble", inmueble)
            print("5")
            # inmueble_serializer = InmueblesSerializer(inmueble, data = data, many=True)
            data = request.data.copy()  # Crear una copia mutable de request.data

            if data.get('reglamento_interno') == 'undefined':
                del data['reglamento_interno']
            
            if data.get('mobiliario') == 'undefined':
                del data['mobiliario']

            # if request.FILES.get('reglamento_interno', None) is None:
            #     data.pop('reglamento_interno')
            # if request.FILES.get('mobiliario', None) is None:
            #     data.pop('mobiliario')
            print("Soy request.data sin archivos", data)
            inmueble_serializer = self.get_serializer(inmueble, data=data, partial=kwargs.pop('partial', False))
            print("6")

            if inmueble_serializer.is_valid(raise_exception=True):
                print("7")
                self.perform_update(inmueble_serializer)
                print("Edito datos Inmuebles")
                print("4")
                print("El valor de la id es:", id)
                print(request.data.get('id'))
                if request.FILES.get('imagenes', None) is not None:
                    data2 = {
                        "imagenes": request.FILES.get('imagenes', None),
                        "inmueble": request.data.get('id')
                    }
                    print("5")
                    imagen_serializer = ImagenInmuebleSerializer(data=data2)
                    print("6")
                    imagen_serializer.is_valid(raise_exception=True)
                    imagen_serializer.save()
                    return Response({'Inmueble': inmueble_serializer.data, 'Imagen': imagen_serializer.data},
                            status=status.HTTP_201_CREATED)
            return Response({'author': inmueble_serializer.data})
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)
        

    @action(detail=False, methods=['put'], url_path='actualizar_status')
    def actualizar_status(self, request, pk=None, *args, **kwargs):
        instance = self.get_object()
        data = request.data.copy()
        data['user'] = request.user.id

        serializer = self.get_serializer(instance, data=data, partial=True)
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            return Response(serializer.data)
        else:
            return Response(serializer.errors)

# ---------------------------------- Fiador Obligado ---------------------------------- #

class Fiador_obligadoViewSet(viewsets.ModelViewSet):
    authentication_classes = [TokenAuthentication, SessionAuthentication]
    permission_classes = [IsAuthenticated]
    queryset = Fiador_obligado.objects.all()
    serializer_class = Fiador_obligadoSerializer
    lookup_field = 'slug'
     
    def list(self, request, *args, **kwargs):
        user_session = request.user       
        try:
           if user_session.is_staff:
                print("Esta entrando a listar fiador_obligado fil")
                fiadores_obligados =  Fiador_obligado.objects.all()
                serializer = self.get_serializer(fiadores_obligados, many=True)
                return Response(serializer.data)
           else:
                print("Esta entrando a listar fiador_obligado fil")
                fiadores_obligados =  Fiador_obligado.objects.all().filter(user_id = user_session)
                serializer = self.get_serializer(fiadores_obligados, many=True)
           
           return Response(serializer.data, status= status.HTTP_200_OK)
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)
        
    def create(self, request, *args, **kwargs):
        user_session = request.user
        try:
            print("Llegando a create fiador-obligado")
            print(request.data)
            fiador_obligado_serializer = self.serializer_class(data=request.data) #Usa el serializer_class
            print(fiador_obligado_serializer)
            if fiador_obligado_serializer.is_valid(raise_exception=True):
                fiador_obligado_serializer.save( user = user_session)
                print("Guardado fiador obligado")
                return Response({'fiador_obligado': fiador_obligado_serializer.data}, status=status.HTTP_201_CREATED)
            else:
                print("Error en validacion")
                return Response({'errors': fiador_obligado_serializer.errors})
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)
        
    def update(self, request, *args, **kwargs):
        try:
            print("Esta entrando a actualizar fiador_obligado")
            partial = kwargs.pop('partial', False)
            print("partials",partial)
            print(request.data)
            instance = self.get_object()
            print("instance",instance)
            serializer = self.get_serializer(instance, data=request.data, partial=partial)
            print(serializer)
            if serializer.is_valid(raise_exception=True):
                self.perform_update(serializer)
                print("edito fiador obligado")
                # return redirect('myapp:my-url')
                return Response(serializer.data, status=status.HTTP_200_OK)
            else:
                return Response({'errors': serializer.errors})
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)
        
    def retrieve(self, request, slug=None, *args, **kwargs):
        user_session = request.user
        try:
            print("Entrando a retrieve")
            modelos = Fiador_obligado.objects.all().filter(user_id = user_session) #Toma los datos de Inmuebles.objects.all() que esta al inicio de la clase viewset
            fiador_obligado = modelos.filter(slug=slug)
            if fiador_obligado:
                serializer_fiador_obligado = Fiador_obligadoSerializer(fiador_obligado, many=True)
                return Response(serializer_fiador_obligado.data, status=status.HTTP_200_OK)
            else:
                return Response({'message': 'No hay persona fisica con esos datos'}, status = status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)
        
    def destroy (self,request, *args, **kwargs):
        try:
            fiador_obligado = self.get_object()
            if fiador_obligado:
                fiador_obligado.delete()
                return Response({'message': 'Fiador obligado eliminado'}, status=204)
            return Response({'message': 'Error al eliminar'}, status=400)
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)

# ---------------------------------- Fiador Obligado ---------------------------------- #
class DocumentosArrendadorViewSet(viewsets.ModelViewSet):
    queryset = DocumentosArrendador.objects.all()
    serializer_class = DocumentosArrendadorSerializer
    
    def list(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset())
        arrendador_serializer = self.get_serializer(queryset, many=True)
        return Response(arrendador_serializer.data ,status=status.HTTP_201_CREATED)
    
    def create (self, request, *args,**kwargs):
        try: 
            data = request.data
            print(data)
            print("Id_arrendador",  request.data.get('arrendador'))
            data = {}
            fields = ['ine', 'comp_dom', 'predial', 'escrituras_titulo','mobiliario', 'reglamento_interno']
            for field in fields:
                if field in request.FILES:
                    data[field] = request.FILES[field]

            data['user'] = request.user.id
            data['arrendador'] = request.data.get('arrendador')
            print("soy data", data)
            if data:
                documentos_serializer = self.get_serializer(data=data)
                documentos_serializer.is_valid(raise_exception=True)
                documentos_serializer.save()
                return Response(documentos_serializer.data, status=status.HTTP_201_CREATED)
            else:
                return Response({'error': 'No file provided'}, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)
        
    @action(detail=False, methods=['delete'], url_path='destroy_individual_archivos')
    def destroy_individual_archivos(self, request,pk=None, *args, **kwargs):
        instance = self.get_object()  # Recuperar el objeto basado en la id proporcionada
        campo = request.data.get('nombre_campo')  # Obtener el nombre del campo a eliminar

        if campo:  # Verificar si se proporcionó un nombre de campo
            if hasattr(instance, campo):  # Verificar si el campo existe en el objeto
                setattr(instance, campo, None)  # Establecer el valor del campo como None o según lo desees
                instance.save()  # Guardar el objeto modificado
                return Response(status=status.HTTP_200_OK)
        else:
            return Response({'Mensaje:': 'No hay nada que eliminar'})
        return Response({'Mensaje': 'Error al eliminar'}, status=status.HTTP_400_BAD_REQUEST)

    @action(detail=False, methods=['put'], url_path='actualizar_archivos_individual')
    def actualizar_archivos_individual(self, request, pk=None, *args, **kwargs):
        instance = self.get_object()
        data = {}
        fields = ['ine', 'comp_dom', 'predial', 'escrituras_titulo']

        for field in fields:
            if field in request.FILES:
                data[field] = request.FILES[field]

        data['user'] = request.user.id

        serializer = self.get_serializer(instance, data=data, partial=True)
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            return Response(serializer.data)
        else:
            return Response(serializer.errors)

    def destroy(self, request, pk=None, *args, **kwargs):
        # try:
        documentos_arrendador = self.get_object()
        documento_arrendador_serializer = self.serializer_class(documentos_arrendador)
        print("Soy ine", documento_arrendador_serializer.data['ine'])
        print("1")
        if documentos_arrendador:
            ine = documento_arrendador_serializer.data['ine']
            print("Soy ine 2", ine)
            comp_dom= documento_arrendador_serializer.data['comp_dom']
            rfc= documento_arrendador_serializer.data['escrituras_titulo']
            print("Soy RFC", rfc)
            ruta_ine = 'apps/static'+ ine
            print("Ruta ine", ruta_ine)
            ruta_comprobante_domicilio = 'apps/static'+ comp_dom
            ruta_rfc = 'apps/static'+ rfc
            print("Ruta com", ruta_comprobante_domicilio)
            print("Ruta RFC", ruta_rfc)
            os.remove(ruta_ine)
            os.remove(ruta_comprobante_domicilio)
            os.remove(ruta_rfc)
            # self.perform_destroy(documentos_arrendador)  #Tambien se puede eliminar asi
            documentos_arrendador.delete()
            return Response({'message': 'Archivo eliminado correctamente'}, status=204)
        else:
            return Response({'message': 'Error al eliminar archivo'}, status=400)
        # except Exception as e:
        #     return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)

    def retrieve(self, request, pk=None):
        try:
            documentos = self.queryset #Toma los datos de Inmuebles.objects.all() que esta al inicio de la clase viewset
            inmueble = documentos.filter(id=pk)
            serializer_inmueble = DocumentosArrendadorSerializer(inmueble, many=True)
            print(serializer_inmueble.data)
            ine = serializer_inmueble.data[0]['ine']
            print(ine)
            
            # documentos_arrendador = self.get_object()
            # print(documentos_arrendador)
            return Response(serializer_inmueble.data)
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)
        
    
    def update(self, request, *args, **kwargs):
        print("Soy data", request.data)
        instance = self.get_object()
        data = {}
        fields = ['ine', 'comp_dom', 'predial', 'escrituras_titulo']
        for field in fields:
            if field in request.FILES:
                data[field] = request.FILES[field]

        data['user'] = request.user.id
        data['arrendador'] = request.data.get('arrendador')

        serializer = self.get_serializer(instance, data=data, partial=True)
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            return Response(serializer.data)
        else:
            return Response(serializer.errors)
        
class Listar_Documentos_ViewSet(viewsets.ModelViewSet):
    # authentication_classes = [TokenAuthentication, SessionAuthentication]
    queryset = Arrendador.objects.all()
    serializer_class = ArrendadorDocumentosSerializer
    # documentos_class = DocumentosArrendadorSerializer
        
    # def get_queryset(self):
    #     user_session = self.request.user
    #     if user_session.is_staff:
    #         data_serializer = self.serializer_class(self.queryset, many=True)
    #         return Response(data_serializer.data)
    #     else:            
    #         user_id = self.request.user.id
    #         return Arrendador.objects.filter(user=user_id)

    def retrieve(self, request, *args, **kwargs):
        print("Esta lleggando a retrieve")
        instance = self.get_object()
        serializer_inquilino = self.get_serializer(instance)
        return Response(serializer_inquilino.data)
    
    def update(self, request, *args, **kwargs):
        try:
            instance = self.get_object()
            # Obtener el valor de validacion_escrituras y comentarios del modelo hijo
            validacion_escrituras = request.data.get('validacion_escrituras')
            comentarios = request.data.get('comentarios')
            # Actualizar el campo estatus_arrendador en el modelo principal
            instance.estatus_arrendador = validacion_escrituras
            # Guardar la instancia actualizada del modelo principal
            instance.save()
            
            # Actualizar los campos del modelo hijo
            arrendador_validacion = instance.arrendador_validacion.first()
            arrendador_validacion.validacion_escrituras = validacion_escrituras
            arrendador_validacion.comentarios = comentarios
            arrendador_validacion.save()
            
            serializer = self.get_serializer(instance, data=request.data, partial=True)
            serializer.is_valid(raise_exception=True)
            self.perform_update(serializer)
            
            print("edito arrendador ")
            return Response(serializer.data, status=status.HTTP_200_OK)
        except ValidationError as e:
            return Response({'errors': e.detail}, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)
    

class HistorialDocumentosArrendadorViewSet(viewsets.ModelViewSet):
    queryset = DocumentosArrendador.objects.all()
    serializer_class = DocumentosArrendadorPruebaSerializer

    def update(self, request, *args, **kwargs):
        print("Soy request data", request.data)
        try:
            instancia_anterior = self.get_object()  # Obtén la instancia anterior
            data = {field: request.FILES[field] for field in ['ine', 'comp_dom', 'predial', 'escrituras_titulo'] if field in request.FILES}

            data['user'] = request.user.id
            data['arrendador'] = request.data.get('arrendador')

            serializer = self.get_serializer(instancia_anterior, data=data, partial=True)
            # Comprueba si existen menos de 4 registros en la tabla HistorialDocumentosArrendador 
            # donde el campo previo_escrituras_titulo no sea nulo (isnull=False) y el campo historial_documentos sea igual al valor proporcionado en request.data.get('arrendador').
            if HistorialDocumentosArrendador.objects.filter(previo_predial__isnull=False, historial_documentos=request.data.get('arrendador')).count() < 4:
                if serializer.is_valid(raise_exception=True):
                    print("Hola")
                    for field in ['ine', 'comp_dom', 'predial', 'escrituras_titulo']:
                        print(field)
                        if field in data and getattr(instancia_anterior, field) != serializer.validated_data.get(field): #getattr  permite obtener el valor de un atributo indicando su nombre como una cadena
                            self.guardar_historial(getattr(instancia_anterior, field), serializer.validated_data.get(field), 'previo_' + field)
                    serializer.save()
                    print("Se guardo")
                    return Response(serializer.data)
                else:
                    return Response(serializer.errors)
            else:
                return Response({"error": "No se permiten más de 3 archivos previo_escrituras_titulo."})
        except Exception as e:
            return Response({'Error': 'Error al actualizar'})
    
    def guardar_historial(self, archivo_anterior, archivo_actual, campo_previo):
        if archivo_actual != archivo_anterior:
            # Eliminar el archivo anterior

            if campo_previo == 'previo_predial':
                # Crear una nueva instancia de HistorialDocumentosArrendador
                historial = HistorialDocumentosArrendador.objects.create(
                    historial_documentos=self.get_object(),
                    previo_ine=None,
                    previo_comp_dom=None,
                    previo_predial=archivo_anterior,
                    previo_escrituras_titulo=None,
                )

            if archivo_anterior and campo_previo != 'previo_predial':
                os.remove(archivo_anterior.path)
# class HistorialDocumentosInquilinoViewSet(viewsets.ModelViewSet):
#     queryset = Inquilino.objects.all()
#     serializer_class = DocumentosInquilinoSerializer

    # def update(self, request, *args, **kwargs):
    #     try:
    #         instancia_anterior = self.get_object()  # Obtén la instancia anterior
    #         data = {field: request.FILES[field] for field in ['ine', 'comp_dom', 'predial', 'escrituras_titulo', 'reglamento_interno', 'mobiliario'] if field in request.FILES}

    #         data['user'] = request.user.id
    #         data['arrendador'] = request.data.get('arrendador')

    #         serializer = self.get_serializer(instancia_anterior, data=data, partial=True)
    #         # print("Cantidad previo escrituras ", HistorialDocumentosArrendador.objects.filter(previo_escrituras_titulo__isnull=False, historial_documentos=request.data.get('arrendador')).count())
    #         # print("instancia_anterior.ine", instancia_anterior.ine)
    #         if HistorialDocumentosArrendador.objects.filter(previo_escrituras_titulo__isnull=False, historial_documentos=request.data.get('arrendador')).count() < 4:
    #             if serializer.is_valid(raise_exception=True):
    #                 print("Hola")
    #                 for field in ['ine', 'comp_dom', 'predial', 'escrituras_titulo']:
    #                     if field in data and getattr(instancia_anterior, field) != serializer.validated_data.get(field): #getattr  permite obtener el valor de un atributo indicando su nombre como una cadena
    #                         self.guardar_historial(getattr(instancia_anterior, field), serializer.validated_data.get(field), 'previo_' + field)
    #                 serializer.save()
    #                 return Response(serializer.data)
    #             else:
    #                 return Response(serializer.errors)
    #         else:
    #             return Response({"error": "No se permiten más de 3 archivos previo_escrituras_titulo."})
    #     except Exception as e:
    #         return Response({'Error': 'Error al actualizar'})
    
    # def guardar_historial(self, archivo_anterior, archivo_actual, campo_previo):
    #     if archivo_anterior:
    #         # Crear una nueva instancia de HistorialDocumentosArrendador
    #         historial = HistorialDocumentosArrendador.objects.create(
    #             historial_documentos = self.get_object(),
    #             previo_ine = archivo_anterior if campo_previo == 'previo_ine' else None,
    #             previo_comp_dom = archivo_anterior if campo_previo == 'previo_comp_dom' else None,
    #             previo_predial = archivo_anterior if campo_previo == 'previo_predial' else None,
    #             previo_escrituras_titulo = archivo_anterior if campo_previo == 'previo_escrituras_titulo' else None,
    #         )


# dOCUMENTOS FIADOR
class DocumentosFoo(viewsets.ModelViewSet):
    authentication_classes = [TokenAuthentication, SessionAuthentication]
    permission_classes = [IsAuthenticated]
    queryset = DocumentosFiador.objects.all()
    serializer_class = DFSerializer
   
    
    def list(self, request, *args, **kwargs):
        content = {
            'user': str(request.user),
            'auth': str(request.auth),
        }
        queryset = self.filter_queryset(self.get_queryset())
        FiadorSerializers = self.get_serializer(queryset, many=True)
       
        return Response(FiadorSerializers.data ,status=status.HTTP_200_OK)
    
    def create (self, request, *args,**kwargs):
        user_session = request.user.id
        print(user_session)
        try: 
            data = request.data
            print("primer print",data)
            data = {
                    "Ine": request.FILES.get('Ine', None),
                    "Comp_dom": request.FILES.get('Comp_dom', None),
                    "Escrituras": request.FILES.get('Escrituras', None),
                    "Estado_cuenta": request.FILES.get('Estado_cuenta', None),
                    "Fiador":request.data['Fiador'],
                    "user":user_session
                }
            print("segundo print",data)
            if data:
                documentos_serializer = self.get_serializer(data=data)
                documentos_serializer.is_valid(raise_exception=True)
                documentos_serializer.save()
                return Response(documentos_serializer.data, status=status.HTTP_201_CREATED)
            else:
                return Response({'error': 'No file provided'}, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)
        

    def destroy(self, request, pk=None, *args, **kwargs):
        # try:
        documentos_fiador = self.get_object()
        documento_fiador_serializer = self.serializer_class(documentos_fiador)
        print("Soy ine", documento_fiador_serializer.data['ine'])
        print("1")
        if documentos_fiador:
            ine = documento_fiador_serializer.data['ine']
            print("Soy ine 2", ine)
            comp_dom= documento_fiador_serializer.data['comp_dom']
            rfc= documento_fiador_serializer.data['escrituras_titulo']
            print("Soy RFC", rfc)
            ruta_ine = 'apps/static'+ ine
            print("Ruta ine", ruta_ine)
            ruta_comprobante_domicilio = 'apps/static'+ comp_dom
            ruta_rfc = 'apps/static'+ rfc
            print("Ruta com", ruta_comprobante_domicilio)
            print("Ruta RFC", ruta_rfc)
            os.remove(ruta_ine)
            os.remove(ruta_comprobante_domicilio)
            os.remove(ruta_rfc)
            # self.perform_destroy(documentos_arrendador)  #Tambien se puede eliminar asi
            documentos_fiador.delete()
            return Response({'message': 'Archivo eliminado correctamente'}, status=status.HTTP_200_OK)
        else:
            return Response({'message': 'Error al eliminar archivo'}, status=status.HTTP_400_BAD_REQUEST)
        # except Exception as e:
        #     return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)
        
        
    def retrieve(self, request, pk=None):
        try:
            documentos = self.queryset #Toma los datos de Inmuebles.objects.all() que esta al inicio de la clase viewset
            fiador = documentos.filter(id=pk)
            serializer_fiador = DFSerializer(fiador, many=True)
            print(serializer_fiador.data)
            ine = serializer_fiador.data[0]['Ine']
            print(ine)
            # documentos_arrendador = self.get_object()
            # print(documentos_arrendador)
            return Response(serializer_fiador.data)
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)
    
    # @action(detail=False, methods=['put'], url_path='actualizar_archivos_individual')
    # def actualizar_archivos_individual(self, request, pk=None, *args, **kwargs):
    #     instance = self.get_object()
    #     print(instance)
    #     data = {}
    #     fields = ['Ine', 'Comp_dom', 'Rfc']

    #     for field in fields:
    #         print("si hay campos",field)
            
    #         if field in request.FILES:
    #             print("si hay campos 2",field)
    #             data[field] = request.FILES[field]
    #             print(data[field])

    #     data['user'] = request.user.id

    #     serializer = self.get_serializer(instance, data=data, partial=True)
    #     if serializer.is_valid(raise_exception=True):
    #         serializer.save()
    #         return Response(serializer.data)
    #     else:
    #         return Response(serializer.errors)
    
    def update(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        print(request.data)
        
        # Verificar si se proporciona un nuevo archivo adjunto
        if 'Ine' in request.data:
            print("soy ine")
            Ine = request.data['Ine']
            os.remove(instance.Ine.path)
            instance.Ine = Ine  # Actualizar el archivo adjunto sin eliminar el anterior
            
        if 'Comp_dom' in request.data:
            Comp_dom = request.data['Comp_dom']
            os.remove(instance.Comp_dom.path)
            instance.Comp_dom = Comp_dom  # Actualizar el archivo adjunto sin eliminar el anterior
            
        if 'Estado_cuenta' in request.data:
            Estado_cuenta = request.data['Estado_cuenta']
            instance.Estado_cuenta = Estado_cuenta  # Actualizar el archivo adjunto sin eliminar el anterior
        
        if 'Escrituras' in request.data:
            Escrituras = request.data['Escrituras']
            os.remove(instance.Escrituras.path)
            instance.Escrituras = Escrituras  # Actualizar el archivo adjunto sin eliminar el anterior
        
        serializer.update(instance, serializer.validated_data)
        print(serializer.data['Ine'])# Actualizar el archivo adjunto sin eliminar el anterior
        return Response(serializer.data)
    

class MobiliarioCantidad(viewsets.ModelViewSet):
    authentication_classes = [TokenAuthentication, SessionAuthentication]
    queryset = InmueblesInmobiliario.objects.all()
    serializer_class = InmueblesMobiliarioSerializer

    def create(self, request, *args, **kwargs):
        data = request.data.copy()  # Crear una copia mutable de request.data
        data['user'] = request.user.id
        
        # Eliminar los campos vacíos del diccionario 'data'
        data = {key: value for key, value in data.items() if value != ''}
        
        mobiliario = self.get_serializer(data=data)
        mobiliario.is_valid(raise_exception=True)
        mobiliario.save()

        return Response(mobiliario.data, status=status.HTTP_201_CREATED)













