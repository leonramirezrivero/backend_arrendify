# Generated by Django 3.2.6 on 2023-06-14 22:48

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0015_remove_datosarrendamiento_fecha_1'),
    ]

    operations = [
        migrations.RenameField(
            model_name='datosarrendamiento',
            old_name='vigencia',
            new_name='duracion',
        ),
        migrations.RemoveField(
            model_name='datosarrendamiento',
            name='fecha_solicitud',
        ),
        migrations.RemoveField(
            model_name='datosarrendamiento',
            name='inquilino',
        ),
        migrations.RemoveField(
            model_name='datosarrendamiento',
            name='nombre_arrendador',
        ),
        migrations.RemoveField(
            model_name='datosarrendamiento',
            name='nombre_inmueble_a_ocupar',
        ),
        migrations.RemoveField(
            model_name='datosarrendamiento',
            name='user',
        ),
        migrations.AddField(
            model_name='datosarrendamiento',
            name='fecha_1',
            field=models.CharField(blank=True, max_length=30, null=True),
        ),
        migrations.AddField(
            model_name='datosarrendamiento',
            name='mantenimiento',
            field=models.CharField(blank=True, max_length=30, null=True),
        ),
        migrations.AddField(
            model_name='datosarrendamiento',
            name='renta',
            field=models.CharField(blank=True, max_length=30, null=True),
        ),
        migrations.AddField(
            model_name='datosarrendamiento',
            name='tipo_persona',
            field=models.CharField(blank=True, max_length=30, null=True),
        ),
        migrations.AddField(
            model_name='datosarrendamiento',
            name='uso_inmueble',
            field=models.CharField(blank=True, max_length=30, null=True),
        ),
        migrations.AlterField(
            model_name='datosarrendamiento',
            name='lugar_firma',
            field=models.CharField(blank=True, max_length=30, null=True),
        ),
        migrations.AlterField(
            model_name='datosarrendamiento',
            name='observaciones',
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
    ]
