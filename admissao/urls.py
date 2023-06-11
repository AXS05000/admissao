from django.urls import path

from . import views
from .views import (AdmissaoCreateView, AdmissaoRHCreateView, BaseList,
                    DepartamentoList, TurnoList)

urlpatterns = [
    path('gerar_contrato/', views.select_contract, name='select_contract'),
    path('upload_template/', views.upload_template, name='upload_template'),
    path('admissao/', AdmissaoCreateView.as_view(), name='admissao'),
    path('admissao_rh/', AdmissaoRHCreateView.as_view(), name='admissao_rh'),
    path('api/departamentos/', DepartamentoList.as_view(), name='api-departamentos'),
    path('api/bases/', BaseList.as_view(), name='api-bases'),
    path('api/turnos/', TurnoList.as_view(), name='api-turnos'),
    path('search_collaborator/', views.CollaboratorSearchView.as_view(), name='search_collaborator'),
    path('collaborator/<int:pk>/', views.CollaboratorDetailView.as_view(), name='collaborator_detail'),
    path('colaborador/<int:pk>/', views.CollaboratorDetailView.as_view(), name='collaborator_detail'),
    path('editar/<int:pk>/', views.CollaboratorUpdateView.as_view(), name='edit_collaborator'),

]