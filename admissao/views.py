import os

from django.conf import settings
from django.http import FileResponse, HttpResponseRedirect, JsonResponse
from django.shortcuts import render
from django.urls import reverse_lazy
from django.views.generic.edit import CreateView
from docx import Document

from .forms import Admissao, UploadFileForm
from .models import Collaborator, ContractTemplate

# Create your views here.




def generate_contract(template, collaborator):
    # Load the Word document
    doc = Document(template.file.path)

    # Prepare the replacement dictionary combining values from all models
    replacements = {}
    replacements.update(collaborator.get_field_values())
    if collaborator.cargo:
        replacements.update(collaborator.cargo.get_field_values())
    if collaborator.departamento_turno:
        replacements.update(collaborator.departamento_turno.get_field_values())

    # Loop through each paragraph
    for paragraph in doc.paragraphs:
        # Replace the keys in the entire paragraph text, not just the runs
        inline = paragraph.runs
        for key, value in replacements.items():
            if key in paragraph.text:
                text = paragraph.text.replace(key, value)
                for i in range(len(inline)):
                    if key in inline[i].text:
                        text = inline[i].text.replace(key, value)
                        inline[i].text = text

    # Make sure the contracts directory exists
    contract_directory = os.path.join(settings.MEDIA_ROOT, 'contracts')
    os.makedirs(contract_directory, exist_ok=True)

    # Save the new Word document
    new_contract_filename = os.path.join(contract_directory, f'{collaborator.name}_{template.name}.docx')
    doc.save(new_contract_filename)

    return new_contract_filename



def select_contract(request):
    if request.method == 'POST':
        collaborator_id = request.POST.get('collaborator')
        template_id = request.POST.get('template')

        collaborator = Collaborator.objects.get(id=collaborator_id)
        template = ContractTemplate.objects.get(id=template_id)

        contract_filename = generate_contract(template, collaborator)

        return FileResponse(open(contract_filename, 'rb'), as_attachment=True, filename=contract_filename)

    collaborators = Collaborator.objects.all()
    templates = ContractTemplate.objects.all()

    return render(request, 'select_contract.html', {'collaborators': collaborators, 'templates': templates})


def upload_template(request):
    if request.method == 'POST':
        form = UploadFileForm(request.POST, request.FILES)
        if form.is_valid():
            new_template = ContractTemplate(name=form.cleaned_data['name'], file=request.FILES['file'])
            new_template.save()
            return HttpResponseRedirect('/upload_template')  # Redirect to a page showing success.
    else:
        form = UploadFileForm()
    return render(request, 'upload.html', {'form': form})

class AdmissaoCreateView(CreateView):
    model = Collaborator
    form_class = Admissao
    template_name = 'formulario_adm.html'  # substitua com o seu template
    success_url = reverse_lazy('admissao')  # substitua com a URL que você quer redirecionar após o sucesso

    def form_valid(self, form):
        form.instance.created_by = self.request.user
        return super().form_valid(form)