from django.contrib import admin

from .models import Base, Cargo, ClienteGI, Collaborator, ContractTemplate

admin.site.register(ContractTemplate)

admin.site.register(Collaborator)

admin.site.register(Base)

admin.site.register(Cargo)

admin.site.register(ClienteGI)
