# Generated by Django 4.1.9 on 2023-06-16 15:19

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('admissao', '0003_alter_base_salario_alter_base_salario_mes'),
    ]

    operations = [
        migrations.AlterField(
            model_name='collaborator',
            name='orgao_emissor_rg',
            field=models.CharField(choices=[('SSP', 'Secretaria de Segurança Pública'), ('PM', 'Polícia Militar'), ('PC', 'Polícia Civil'), ('FGTS', 'Fundo de Garantia do Tempo de Serviço'), ('IFP', 'Instituto Félix Pacheco'), ('IPF', 'Instituto Pereira Faustino'), ('IMESP', 'Instituto de Identificação Ricardo Gumbleton Daunt'), ('ITI', 'Instituto de Identificação Tobias de Aguiar'), ('DETRAN', 'Departamento de Trânsito'), ('CTPS', 'Carteira de Trabalho e Previdência Social'), ('FIDENE', 'Fundação de Integração e Desenvolvimento do Ensino do Noroeste do Estado'), ('ME', 'Ministério do Exército'), ('MEX', 'Ministério do Exército'), ('MTE', 'Ministério do Trabalho e Emprego'), ('PF', 'Polícia Federal'), ('POM', 'Polícia Militar'), ('SD/SG', 'Serviço Discreto / Secretaria Geral'), ('SNJ', 'Secretaria Nacional de Justiça'), ('SSPDS', 'Secretaria de Segurança Pública e Defesa da Sociedade'), ('STF', 'Supremo Tribunal Federal'), ('STM', 'Superior Tribunal Militar')], max_length=150),
        ),
    ]
