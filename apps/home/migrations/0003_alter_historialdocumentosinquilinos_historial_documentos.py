# Generated by Django 3.2.6 on 2023-06-01 18:01

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0002_alter_inquilino_calle_empleo'),
    ]

    operations = [
        migrations.AlterField(
            model_name='historialdocumentosinquilinos',
            name='historial_documentos',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='historial_d_inquilinos', to='home.documentosinquilino'),
        ),
    ]
