# Generated by Django 4.1.9 on 2023-06-16 16:11

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('admissao', '0006_alter_collaborator_cep_alter_collaborator_cpf_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='collaborator',
            name='celular',
            field=models.CharField(max_length=14),
        ),
        migrations.AlterField(
            model_name='collaborator',
            name='cep',
            field=models.CharField(max_length=9),
        ),
        migrations.AlterField(
            model_name='collaborator',
            name='cpf',
            field=models.CharField(max_length=13),
        ),
    ]