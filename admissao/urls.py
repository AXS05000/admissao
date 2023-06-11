from django.urls import path

from . import views
from .views import (AdmissaoCreateView, AdmissaoRHCreateView, BaseList,
                    DepartamentoList)

urlpatterns = [
    path('gerar_contrato/', views.select_contract, name='select_contract'),
    path('upload_template/', views.upload_template, name='upload_template'),
    path('admissao/', AdmissaoCreateView.as_view(), name='admissao'),
    path('admissao_rh/', AdmissaoRHCreateView.as_view(), name='admissao_rh'),
    path('api/departamentos/', DepartamentoList.as_view(), name='api-departamentos'),
    path('api/bases/', BaseList.as_view(), name='api-bases'),
]