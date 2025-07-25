# Generated by Django 5.1.6 on 2025-07-08 07:34

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0005_alter_useraccount_cpf'),
    ]

    operations = [
        migrations.AddField(
            model_name='useraccount',
            name='porte',
            field=models.CharField(choices=[('PL', 'Profissional Liberal'), ('MEI', 'Mei'), ('EPP', 'Epp'), ('ME', 'Me'), ('MEDIA', 'Média'), ('GRANDE', 'Grande')], default='PL', max_length=20),
        ),
        migrations.AddField(
            model_name='useraccount',
            name='setor',
            field=models.CharField(choices=[('Setor A', 'Setor A'), ('Setor B', 'Setor B'), ('Setor C', 'Setor C')], default='Setor A', max_length=20),
        ),
    ]
