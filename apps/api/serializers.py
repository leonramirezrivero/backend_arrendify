from rest_framework import serializers
from ..home.models import Inquilino

from ..home.models import *
from ..authentication.models import *
from ..home.models import DocumentosInquilino

class DISerializer(serializers.ModelSerializer):
    inquilinos_nombre = serializers.CharField(source='inquilino.nombre', read_only=True)
    inquilinos_apellido = serializers.CharField(source='inquilino.apellido', read_only=True)
    inquilinos_apellido1 = serializers.CharField(source='inquilino.apellido1', read_only=True)
    class Meta:
        model = DocumentosInquilino
        fields = '__all__'
        
class DFSerializer(serializers.ModelSerializer):
    fiador_nombre = serializers.CharField(source='fiador.n_fiador', read_only=True)
    fiador_apellido = serializers.CharField(source='inquilino.apellido', read_only=True)
    fiador_apellido1 = serializers.CharField(source='inquilino.apellido1', read_only=True)
    class Meta:
        model = DocumentosFiador
        fields = '__all__'

class Fiador_obligadoSerializer(serializers.ModelSerializer):

    inquilino_nombre = serializers.CharField(source='inquilino.nombre', read_only=True)
    inquilino_apellido = serializers.CharField(source='inquilino.apellido', read_only=True)
    inquilino_apellido1 = serializers.CharField(source='inquilino.apellido1', read_only=True)
    archivos = DFSerializer(many=True, read_only=True)

    
    class Meta:
        model = Fiador_obligado
        fields = '__all__'
# Serializar para mandar excluivamente datos sintetizador del fiador al inquilino
class FOS(serializers.ModelSerializer):
    class Meta:
        model = Fiador_obligado
        fields = ('id','fiador_obligado','n_fiador','a_fiador','a2_fiador','nombre_comercial')         
   
class InquilinoSerializers(serializers.ModelSerializer):
    # aval = Fiador_obligadoSerializer(many=True, read_only=True)
    aval = FOS(many=True, read_only=True)
    archivos = DISerializer(many=True, read_only=True)
    
    class Meta:
        model = Inquilino
        fields = '__all__'

# Serializar para mandar excluivamente datos sintetizador del inquilino hacia fiador
class InquilinoSerializersFiador(serializers.ModelSerializer):
    class Meta:
        model = Inquilino
        fields = ('id', 'nombre','apellido','apellido1')
        

class ArrendadorConCamposEstablecidosSerializer(serializers.ModelSerializer):
    custom_field = serializers.SerializerMethodField()
    class Meta:
        model = Arrendador
        fields = ('id', 'nombre','apellido','apellido1', 'custom_field', 'arrendador_validacion')
    def get_custom_field(self, obj):
        if not obj.nombre:
            return obj.n_inmobiliaria


class ImagenInmuebleSerializer(serializers.ModelSerializer):
    # imagenes = serializers.FileField(required=False)
    # imagenes = serializers.ListField(child=serializers.ImageField())
    # imagenes = serializers.ListField(child=serializers.ImageField(), required=False)
    class Meta:
        model = ImagenInmueble
        fields = '__all__'

class InmueblesMobiliarioSerializer(serializers.ModelSerializer):
    class Meta:
        model = InmueblesInmobiliario
        fields = '__all__'

class InmueblesSerializer(serializers.ModelSerializer):
    # imagen_inmueble_inner = ImagenInmuebleSerializer( many=True , read_only=True)
    # arrendador = ArrendadorConCamposEstablecidosSerializer()
    # author = ImagenInmuebleSerializer(many=True, read_only=True)
    arrendador_nombre = serializers.CharField(source='arrendador.nombre', read_only=True)
    arrendador_apellido_paterno = serializers.CharField(source='arrendador.apellido', read_only=True)
    arrendador_apellido_materno = serializers.CharField(source='arrendador.apellido1', read_only=True)
    inmuebles = InmueblesMobiliarioSerializer(many=True, read_only=True)
    class Meta:
        model = Inmuebles
        fields = '__all__'

    def create(self, validated_data):
        try:
            return Inmuebles.objects.create(**validated_data)
        except Exception as e:
            raise serializers.ValidationError(str(e))
        
class DocumentosArrendadorSerializer(serializers.ModelSerializer):
    # arrendador = serializers.PrimaryKeyRelatedField(queryset=Arrendador.objects.all(),allow_null=True)
    # arrendador = serializers.PrimaryKeyRelatedField(queryset=Author.objects.all())
    # arrendador = ArrendadorConCamposEstablecidosSerializer(read_only=True)
    class Meta:
        model = DocumentosArrendador
        fields = '__all__'

class DocumentosArrendadorSerializer22(serializers.ModelSerializer):
    # arrendador = serializers.PrimaryKeyRelatedField(queryset=Arrendador.objects.all(),allow_null=True)
    # arrendador = serializers.PrimaryKeyRelatedField(queryset=Author.objects.all())
    # arrendador = ArrendadorConCamposEstablecidosSerializer(read_only=True)
    class Meta:
        model = DocumentosArrendador
        fields = '__all__'

class ValidacionArrendadorSerializer(serializers.ModelSerializer):
    class Meta:
        model = ValidacionArrendador
        fields = '__all__'
        
class ArrendadorDocumentosSerializer(serializers.ModelSerializer):
    arrendador = DocumentosArrendadorSerializer22(many=True, read_only=True)
    arrendador_validacion = ValidacionArrendadorSerializer(many=True, read_only=True)
    class Meta:
        model = Arrendador
        fields = ('id', 'nombre','apellido','apellido1', 'arrendador', 'n_inmobiliaria', 'pmoi', 'slug', 'estatus_arrendador', 'created','arrendador_validacion')


class ArrendadorSerializer(serializers.ModelSerializer):
    arrendador = DocumentosArrendadorSerializer22(many=True, read_only=True)
    class Meta:
        model = Arrendador
        fields = '__all__'

class HistorialDocumentosArrendadorSerializer(serializers.ModelSerializer):
    class Meta:
        model = HistorialDocumentosArrendador
        fields = '__all__'



class DocumentosArrendadorPruebaSerializer(serializers.ModelSerializer):
    historial_documentos_arrendador = HistorialDocumentosArrendadorSerializer(many=True, read_only=True)
    arrendador = ArrendadorConCamposEstablecidosSerializer(read_only=True)
    class Meta:
        model = DocumentosArrendador
        fields = '__all__'


class HistorialDocumentosInquilinoSerializer(serializers.ModelSerializer):
    class Meta:
        model = HistorialDocumentosInquilinos
        fields = '__all__'

class DocumentosInquilinosSerializer(serializers.ModelSerializer):
    historial_documentos_inquilinos = HistorialDocumentosInquilinoSerializer(many=True, read_only = True)

    class Meta:
        model = DocumentosInquilino
        fields = '__all__'

class DocumentosInquilinoSerializer(serializers.ModelSerializer):
    class Meta:
        model = DocumentosInquilino
        fields = '__all__'




class ArrendadorPruebaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Arrendador
        fields = '__all__'


