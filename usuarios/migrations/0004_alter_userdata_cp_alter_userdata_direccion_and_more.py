# Generated by Django 5.0.4 on 2024-05-16 23:00

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('usuarios', '0003_usuarioxinst'),
    ]

    operations = [
        migrations.AlterField(
            model_name='userdata',
            name='cp',
            field=models.PositiveIntegerField(default=''),
        ),
        migrations.AlterField(
            model_name='userdata',
            name='direccion',
            field=models.CharField(default='', max_length=100),
        ),
        migrations.AlterField(
            model_name='userdata',
            name='poblacion',
            field=models.CharField(default='', max_length=50),
        ),
        migrations.AlterField(
            model_name='userdata',
            name='provincia',
            field=models.CharField(default='', max_length=30),
        ),
        migrations.AlterField(
            model_name='userdata',
            name='telefono',
            field=models.PositiveIntegerField(default=''),
        ),
    ]