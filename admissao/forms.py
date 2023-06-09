from django import forms

from .models import Collaborator


class UploadFileForm(forms.Form):
    name = forms.CharField(max_length=200)
    file = forms.FileField()

class Admissao(forms.ModelForm):
    class Meta:
        model = Collaborator
        fields = ['name', 'cpf', 'admission_date', 'rg', 'orgao_emissor_rg', 'uf_rg', 'data_emissao_rg', 'n_ctps', 'serie', 'uf_ctps', 'data_emissao_ctps', 'endereco', 'cep', 'celular', 'email']
        requireds = ['name', 'cpf', 'admission_date', 'rg', 'orgao_emissor_rg', 'uf_rg', 'data_emissao_rg', 'n_ctps', 'serie', 'uf_ctps', 'data_emissao_ctps', 'endereco', 'cep', 'celular', 'email']
