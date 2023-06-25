from django.urls import path

from . import views
from .views import (GerarcsvTemplateView, GestaoListView, NotaFiscalCreateView,
                    Notas_FiscaisView)

urlpatterns = [
    path('notafiscal/', NotaFiscalCreateView.as_view(), name='notafiscal'),
    path('gestao/', GestaoListView.as_view(), name='gestao'),
    path('notasfiscais/', Notas_FiscaisView.as_view(), name='notasficais'),
    path('qtddecargos/', views.qtddecargos, name='qtddecargos'),
    path('notafiscal2/', views.notafiscal2, name='notafiscal2'),
    path('notafiscal3/', views.notafiscal3, name='notafiscal3'),
    path('notafiscal4/', views.notafiscal4, name='notafiscal4'),
    path('notafiscal5/', views.notafiscal5, name='notafiscal5'),
    path('notafiscal6/', views.notafiscal6, name='notafiscal6'),
    path('notafiscal7/', views.notafiscal7, name='notafiscal7'),
    path('notafiscal8/', views.notafiscal8, name='notafiscal8'),
    path('gestao/cliente/<int:cliente_id>/', views.cliente, name='cliente'),
    path('cnpj/', views.cnpj, name='cnpj'),
    path('fatoutros/', views.fatoutros, name='fatoutros'),
    path('atualizar-cnpj/', views.update_basecnpj, name='atualizar_cnpj'),
    path('importar-cnpj/', views.import_basecnpj, name='importar_basecnpj'),
    path('generate-csv/', views.generate_csv, name='generate-csv'),
    path('gerar-csv/', GerarcsvTemplateView.as_view(), name='gerar-csv'),
    path('generate-csv-for-nota/<int:pk>', views.generate_csv_for_nota, name='generate_csv_for_nota'),
    path('buscar-notas/', views.buscar_notas, name='buscar_notas'),  
    path('atualizar_notas/', views.atualizar_notas, name='atualizar_notas'),
]