from django.urls import path

from . import views
from .views import AdmissaoCreateView

urlpatterns = [
    path('gerar_contrato/', views.select_contract, name='select_contract'),
    path('upload_template/', views.upload_template, name='upload_template'),
    path('admissao/', AdmissaoCreateView.as_view(), name='admissao'),
   
]