# Generated by Django 3.2.6 on 2023-06-20 22:43

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0020_alter_paquetes_table'),
    ]

    operations = [
        migrations.CreateModel(
            name='Agentify',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('nombre', models.CharField(blank=True, max_length=50, null=True)),
                ('apellido_materno', models.CharField(blank=True, max_length=30, null=True)),
                ('apellido_paterno', models.CharField(blank=True, max_length=30, null=True)),
                ('correo', models.CharField(blank=True, max_length=30, null=True)),
                ('empresa_labora', models.CharField(blank=True, default='Arrendify', max_length=30, null=True)),
                ('numero_celular', models.CharField(blank=True, max_length=30, null=True)),
                ('puesto', models.CharField(blank=True, max_length=30, null=True)),
                ('esquema_comisiones', models.CharField(blank=True, max_length=30, null=True)),
                ('ventas', models.CharField(blank=True, max_length=30, null=True)),
            ],
            options={
                'db_table': 'agentify',
            },
        ),
        migrations.CreateModel(
            name='Cotizacion',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('nombre_cotizacion', models.CharField(blank=True, max_length=30, null=True)),
                ('cliente', models.CharField(blank=True, max_length=30, null=True)),
                ('monto', models.CharField(blank=True, max_length=30, null=True)),
                ('monto_impuesto', models.CharField(blank=True, default=16, max_length=30, null=True)),
                ('monto_total', models.CharField(blank=True, max_length=50, null=True)),
                ('comision', models.CharField(blank=True, max_length=50, null=True)),
                ('costos_extra', models.CharField(blank=True, max_length=50, null=True)),
                ('observaciones', models.CharField(blank=True, max_length=50, null=True)),
                ('años_cobertura', models.PositiveIntegerField(blank=True, default=1, null=True)),
                ('duracion_contrato', models.CharField(blank=True, max_length=50, null=True)),
                ('tipo_poliza', models.CharField(blank=True, max_length=50, null=True)),
                ('fecha_cotizacion', models.DateField(auto_now_add=True)),
                ('fecha_vigencia', models.DateField(null=True)),
                ('cliente_inquilino', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='cliente_inquilino', to='home.inquilino')),
                ('cotizacion_inmueble', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='cotizacion_inmueble', to='home.arrendador')),
            ],
            options={
                'db_table': 'cotizacion',
            },
        ),
    ]
