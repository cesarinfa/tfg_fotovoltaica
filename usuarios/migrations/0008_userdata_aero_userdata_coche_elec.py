# Generated by Django 5.0.6 on 2024-07-03 20:13

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('usuarios', '0007_alter_usuarioxinst_unique_together'),
    ]

    operations = [
        migrations.AddField(
            model_name='userdata',
            name='aero',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='userdata',
            name='coche_elec',
            field=models.BooleanField(default=False),
        ),
    ]