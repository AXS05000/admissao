from django.db import models


class ContractTemplate(models.Model):
    name = models.CharField(max_length=200)
    file = models.FileField(upload_to='contract_templates/')

    def __str__(self):
        return f'{self.name}'
    
class ClienteGI(models.Model):
    nome = models.CharField(max_length=250)
    cod_cliente = models.IntegerField()
    responsavel_filial = models.CharField(max_length=250)
    telefone_filial = models.CharField(max_length=60)
       
    def __str__(self):
        return f'{self.nome}'
    
    def get_field_values(self):
        return {
            '{nome_cliente}': self.nome,
            '{cod_cliente}': str(self.cod_cliente),
            '{responsavel_filial}': str(self.responsavel_filial),
            '{telefone_filial}': self.telefone_filial,
        }
    
class Cargo(models.Model):
    nome = models.CharField(max_length=250)
    cbo = models.CharField(max_length=250)


    def __str__(self):
        return f'{self.nome}'
    
    def get_field_values(self):
        return {
            '{nome_cargo}': self.nome,
            '{cbo}': self.cbo,
        }

class Base(models.Model):
    cargo = models.ForeignKey(
        Cargo, on_delete=models.SET_NULL, null=True, blank=True
    )
    cliente = models.ForeignKey(
        ClienteGI, on_delete=models.SET_NULL, null=True, blank=True
    )
    salario = models.DecimalField(
        'Salario', max_digits=18, decimal_places=2)
    salario_mes = models.DecimalField(
        'Salario Mês', max_digits=18, decimal_places=2)
    vt = models.DecimalField(
        'VT', max_digits=18, decimal_places=2)
    vr = models.DecimalField(
        'VR', max_digits=18, decimal_places=2)
    cesta = models.DecimalField(
        'CESTA', max_digits=18, decimal_places=2)
    sindicato = models.CharField(max_length=250)

       
    def __str__(self):
        return f'{self.cargo} - {self.cliente} - {self.salario_mes}'
    
    def get_field_values(self):
        return {
            '{nome_cargo}': self.cargo.nome if self.cargo else '',
            '{nome_cliente}': self.cliente.nome if self.cliente else '',
            '{salario}': str(self.salario),
            '{salario_mes}': str(self.salario_mes),
            '{vt}': str(self.vt),
            '{vr}': str(self.vr),
            '{cesta}': str(self.cesta),
            '{sindicato}': self.sindicato,
        }
    

class Collaborator(models.Model):
    name = models.CharField(max_length=200)
    cpf = models.CharField(max_length=14)
    admission_date = models.DateField()
    rg = models.CharField(max_length=20)
    orgao_emissor_rg = models.CharField(max_length=30)
    uf_rg = models.CharField(max_length=2)
    data_emissao_rg = models.DateField()
    n_ctps = models.CharField(max_length=30)
    serie = models.CharField(max_length=30)
    uf_ctps = models.CharField(max_length=2)
    data_emissao_ctps = models.DateField()
    endereco = models.CharField(max_length=250)
    cep = models.CharField(max_length=30)
    celular = models.CharField(max_length=11)
    email = models.CharField(max_length=250)
    cargo = models.ForeignKey(
        Base, on_delete=models.SET_NULL, null=True, blank=True
    )
       
    def __str__(self):
        return f'{self.name}'
    
    def get_field_values(self):
        return {
            '{nome}': self.name,
            '{cpf}': self.cpf,
            '{admissão}': str(self.admission_date),
            '{rg}': self.rg,
            '{orgao_emissor_rg}': self.orgao_emissor_rg,
            '{uf_rg}': self.uf_rg,
            '{data_emissao_rg}': self.data_emissao_rg,
            '{n_ctps}': self.n_ctps,
            '{serie}': self.serie,
            '{uf_ctps}': self.uf_ctps,
            '{data_emissao_ctps}': self.data_emissao_ctps,
            '{endereco}': self.endereco,
            '{cep}': self.cep,
            '{celular}': self.celular,
            '{email}': self.email,
        }
    