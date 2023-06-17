import csv
import re
from decimal import Decimal

from django.contrib import messages
from django.core.paginator import PageNotAnInteger, Paginator
from django.http import Http404, HttpResponse
# from core.main import make_recipe - Importação para testar as coisas.
from django.shortcuts import render
from django.utils import timezone
from django.views.generic import CreateView, DetailView, ListView

from .forms import BaseCNPJModelForm, NotasModelForm
from .models import BaseCNPJ, Notas
from .utils import import_basecnpj_from_excel, update_basecnpj_from_excel


def generate_csv(request):
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="notas.csv"'

    writer = csv.writer(response, delimiter=';')
    today = timezone.now().strftime("%Y-%m-%d")
    test_marker = 'T' if 'test' in request.GET else ''
    first_row = ['H', today, today, test_marker, '18504752000155']
    writer.writerow(first_row)

    def generate_description(nota):
        descricao = ""
        if nota.porcentagem_ans is not None and nota.total_valor_outros is None:
            total_a_faturar_nota = round(nota.total_a_faturar - (nota.total_a_faturar * nota.porcentagem_ans) , 4)

        elif nota.porcentagem_ans is None and nota.total_valor_outros is not None:
            total_a_faturar_nota = round(nota.total_valor_outros, 4)

        else:
            total_a_faturar_nota = round(nota.total_a_faturar, 4) 

        base_pis = total_a_faturar_nota * Decimal("0.0065")
        base_confins = total_a_faturar_nota * Decimal("0.03")
        base_inss = total_a_faturar_nota * Decimal("0.11")
        base_ir = total_a_faturar_nota * Decimal("0.048")
        base_cssl = total_a_faturar_nota * Decimal("0.01")
        base_iss = total_a_faturar_nota * nota.cnpj_da_nota.iss
        total_liquido_descricao = round(total_a_faturar_nota - (base_pis + base_confins + base_inss + base_ir + base_cssl + base_iss) , 4)



        if nota.tipo_de_faturamento == 'FATURAMENTO HORAS' and nota.cnpj_da_nota.tipo_de_cliente == 'LOG' and nota.porcentagem_ans is None:
            descricao = f"PRESTAÇÃO DE SERVIÇOS DE APOIO A OPERAÇÃO DE ARMAZENAGEM E LOGISTICA|\n\nCONTRATO: {nota.baseinfocontratos.contrato} - COMPETÊNCIA: {nota.competencia_nota}|\n\n"
            for baseinfocontratos_field, quantidade_hora_field in [('baseinfocontratos', 'quantidade_hora'), ('baseinfocontratos2', 'quantidade_hora2'), ('baseinfocontratos3', 'quantidade_hora3'), ('baseinfocontratos4', 'quantidade_hora4'), ('baseinfocontratos5', 'quantidade_hora5'), ('baseinfocontratos6', 'quantidade_hora6'), ('baseinfocontratos7', 'quantidade_hora7'), ('baseinfocontratos8', 'quantidade_hora8')]:  # adicione aqui todos os pares baseinfocontratos/quantidade_hora
                baseinfocontratos = getattr(nota, baseinfocontratos_field)
                quantidade_hora = getattr(nota, quantidade_hora_field)
                if baseinfocontratos and quantidade_hora:
                    total_bruto_cargo = round(baseinfocontratos.valor_hora * Decimal(str(quantidade_hora)), 4)
                    total_bruto_cargo = str(total_bruto_cargo).replace('.', ',')  # substitui o ponto por vírgula
                    descricao += f"CARGO: {baseinfocontratos.cargo} - QTD HS: {quantidade_hora}- VALOR HORA: R${baseinfocontratos.valor_hora} TOTAL BRUTO CARGO: R$ {total_bruto_cargo}|\n\n"
            descricao += f"||TOTAL A FATURAR: R$ {format(total_a_faturar_nota, '.4f').replace('.', ',')}|\n\n BASE PARA RETENÇÕES:|\n\nRETENÇÃO CONFORME LEI 10833/03 - PIS: 0,0065: R$ {format(base_pis, '.4f').replace('.', ',')}|\n\nRETENÇÃO CONFORME LEI 10833/03 - CONFINS: 0,03: R$ {format(base_confins, '.4f').replace('.', ',')}|\n\n INSS RETENÇÃO: 0,11: R$ {format(base_inss, '.4f').replace('.', ',')}|\n\n I.R. RETENÇÃO: 0,048: R$ {format(base_ir, '.4f').replace('.', ',')}|\n\n RETENÇÃO CONFORME LEI 10833/03 - CSLL: 0,01: R$ {format(base_cssl, '.4f').replace('.', ',')}|\n\n RETENÇÃO CONFORME LEI 116/03 - ISS: {format(base_iss, '.4f').replace('.', ',')}|\n\n TOTAL LIQUIDO A RECEBER: R$ {format(total_liquido_descricao, '.4f').replace('.', ',')}|"


        if nota.tipo_de_faturamento == 'FATURAMENTO HORAS' and nota.cnpj_da_nota.tipo_de_cliente == 'MOT' and nota.porcentagem_ans is None:
            descricao = f"PRESTAÇÃO DE SERVIÇOS DE APOIO A OPERAÇÃO DE ARMAZENAGEM E LOGISTICA|\n\nCONTRATO: {nota.baseinfocontratos.contrato} - COMPETÊNCIA: {nota.competencia_nota}|\n\n"
            for baseinfocontratos_field, quantidade_hora_field in [('baseinfocontratos', 'quantidade_hora'), ('baseinfocontratos2', 'quantidade_hora2'), ('baseinfocontratos3', 'quantidade_hora3'), ('baseinfocontratos4', 'quantidade_hora4'), ('baseinfocontratos5', 'quantidade_hora5'), ('baseinfocontratos6', 'quantidade_hora6'), ('baseinfocontratos7', 'quantidade_hora7'), ('baseinfocontratos8', 'quantidade_hora8')]:  # adicione aqui todos os pares baseinfocontratos/quantidade_hora
                baseinfocontratos = getattr(nota, baseinfocontratos_field)
                quantidade_hora = getattr(nota, quantidade_hora_field)
                if baseinfocontratos and quantidade_hora:
                    total_bruto_cargo = round(baseinfocontratos.valor_hora * Decimal(str(quantidade_hora)), 4)
                    total_bruto_cargo = str(total_bruto_cargo).replace('.', ',')  # substitui o ponto por vírgula
                    descricao += f"CARGO: {baseinfocontratos.cargo} - QTD HS: {quantidade_hora}- VALOR HORA: R${baseinfocontratos.valor_hora} TOTAL BRUTO CARGO: R$ {total_bruto_cargo}|\n\n"
            descricao += f"||TOTAL A FATURAR: R$ {format(total_a_faturar_nota, '.4f').replace('.', ',')}|\n\n BASE PARA RETENÇÕES:|\n\nRETENÇÃO CONFORME LEI 10833/03 - PIS: 0,0065: R$ {format(base_pis, '.4f').replace('.', ',')}|\n\nRETENÇÃO CONFORME LEI 10833/03 - CONFINS: 0,03: R$ {format(base_confins, '.4f').replace('.', ',')}|\n\n INSS RETENÇÃO: 0,11: R$ {format(base_inss, '.4f').replace('.', ',')}|\n\n I.R. RETENÇÃO: 0,048: R$ {format(base_ir, '.4f').replace('.', ',')}|\n\n RETENÇÃO CONFORME LEI 10833/03 - CSLL: 0,01: R$ {format(base_cssl, '.4f').replace('.', ',')}|\n\n RETENÇÃO CONFORME LEI 116/03 - ISS: {format(base_iss, '.4f').replace('.', ',')}|\n\n TOTAL LIQUIDO A RECEBER: R$ {format(total_liquido_descricao, '.4f').replace('.', ',')}|"


        if nota.tipo_de_faturamento == 'FATURAMENTO HORAS' and nota.cnpj_da_nota.tipo_de_cliente == 'DISTRIBUIÇÃO' and nota.porcentagem_ans is None:
            descricao = f"PRESTAÇÃO DE SERVIÇOS CONTINUADOS DE APOIO AS UNIDADE DE DISTRUIBUIÇÃO, UNIDADE: {nota.cnpj_da_nota.unidade} MCU: {nota.cnpj_da_nota.mcu}|\n\nCONTRATO: {nota.baseinfocontratos.contrato} - COMPETÊNCIA: {nota.competencia_nota}|\n\n"
            for baseinfocontratos_field, quantidade_hora_field in [('baseinfocontratos', 'quantidade_hora'), ('baseinfocontratos2', 'quantidade_hora2'), ('baseinfocontratos3', 'quantidade_hora3'), ('baseinfocontratos4', 'quantidade_hora4'), ('baseinfocontratos5', 'quantidade_hora5'), ('baseinfocontratos6', 'quantidade_hora6'), ('baseinfocontratos7', 'quantidade_hora7'), ('baseinfocontratos8', 'quantidade_hora8')]:  # adicione aqui todos os pares baseinfocontratos/quantidade_hora
                baseinfocontratos = getattr(nota, baseinfocontratos_field)
                quantidade_hora = getattr(nota, quantidade_hora_field)
                if baseinfocontratos and quantidade_hora:
                    total_bruto_cargo = round(baseinfocontratos.valor_hora * Decimal(str(quantidade_hora)), 4)
                    total_bruto_cargo = str(total_bruto_cargo).replace('.', ',')  # substitui o ponto por vírgula
                    descricao += f"CARGO: {baseinfocontratos.cargo} - QTD HS: {quantidade_hora}- VALOR HORA: R${baseinfocontratos.valor_hora} TOTAL BRUTO CARGO: R$ {total_bruto_cargo}|\n\n"
            descricao += f"||TOTAL A FATURAR: R$ {format(total_a_faturar_nota, '.4f').replace('.', ',')}|\n\n BASE PARA RETENÇÕES:|\n\nRETENÇÃO CONFORME LEI 10833/03 - PIS: 0,0065: R$ {format(base_pis, '.4f').replace('.', ',')}|\n\nRETENÇÃO CONFORME LEI 10833/03 - CONFINS: 0,03: R$ {format(base_confins, '.4f').replace('.', ',')}|\n\n INSS RETENÇÃO: 0,11: R$ {format(base_inss, '.4f').replace('.', ',')}|\n\n I.R. RETENÇÃO: 0,048: R$ {format(base_ir, '.4f').replace('.', ',')}|\n\n RETENÇÃO CONFORME LEI 10833/03 - CSLL: 0,01: R$ {format(base_cssl, '.4f').replace('.', ',')}|\n\n RETENÇÃO CONFORME LEI 116/03 - ISS: {format(base_iss, '.4f').replace('.', ',')}|\n\n TOTAL LIQUIDO A RECEBER: R$ {format(total_liquido_descricao, '.4f').replace('.', ',')}|"


        #################################### COM ANS ######################################################



        if nota.tipo_de_faturamento == 'FATURAMENTO HORAS' and nota.cnpj_da_nota.tipo_de_cliente == 'LOG' and nota.porcentagem_ans is not None:
            descricao = f"PRESTAÇÃO DE SERVIÇOS DE APOIO A OPERAÇÃO DE ARMAZENAGEM E LOGISTICA|\n\nCONTRATO: {nota.baseinfocontratos.contrato} - COMPETÊNCIA: {nota.competencia_nota}|\n\n TODOS OS ITENS DESCRITOS NA NF SOFRERAM DESCONTO DE {nota.porcentagem_ans} % PELA PONTUAÇÃO DO ANS NA COMPETÊNCIA DE {nota.competencia_nota_ans.competencia}.|"
            for baseinfocontratos_field, quantidade_hora_field in [('baseinfocontratos', 'quantidade_hora'), ('baseinfocontratos2', 'quantidade_hora2'), ('baseinfocontratos3', 'quantidade_hora3'), ('baseinfocontratos4', 'quantidade_hora4'), ('baseinfocontratos5', 'quantidade_hora5'), ('baseinfocontratos6', 'quantidade_hora6'), ('baseinfocontratos7', 'quantidade_hora7'), ('baseinfocontratos8', 'quantidade_hora8')]:  # adicione aqui todos os pares baseinfocontratos/quantidade_hora
                baseinfocontratos = getattr(nota, baseinfocontratos_field)
                quantidade_hora = getattr(nota, quantidade_hora_field)
                if baseinfocontratos and quantidade_hora:
                    total_bruto_cargo = round(baseinfocontratos.valor_hora * Decimal(str(quantidade_hora)), 4)
                    total_bruto_cargo_ans = round(total_bruto_cargo - (total_bruto_cargo * Decimal(str(nota.porcentagem_ans))), 4)
                    total_bruto_cargo_ans = str(total_bruto_cargo_ans).replace('.', ',')  # substitui o ponto por vírgula
                    descricao += f"CARGO: {baseinfocontratos.cargo} - QTD HS: {quantidade_hora}- VALOR HORA: R${baseinfocontratos.valor_hora} TOTAL BRUTO CARGO COM DESCONTO: R$ {total_bruto_cargo_ans}|\n\n"
            descricao += f"||TOTAL A FATURAR: R$ {format(total_a_faturar_nota, '.4f').replace('.', ',')}|\n\n BASE PARA RETENÇÕES:|\n\nRETENÇÃO CONFORME LEI 10833/03 - PIS: 0,0065: R$ {format(base_pis, '.4f').replace('.', ',')}|\n\nRETENÇÃO CONFORME LEI 10833/03 - CONFINS: 0,03: R$ {format(base_confins, '.4f').replace('.', ',')}|\n\n INSS RETENÇÃO: 0,11: R$ {format(base_inss, '.4f').replace('.', ',')}|\n\n I.R. RETENÇÃO: 0,048: R$ {format(base_ir, '.4f').replace('.', ',')}|\n\n RETENÇÃO CONFORME LEI 10833/03 - CSLL: 0,01: R$ {format(base_cssl, '.4f').replace('.', ',')}|\n\n RETENÇÃO CONFORME LEI 116/03 - ISS: {format(base_iss, '.4f').replace('.', ',')}|\n\n TOTAL LIQUIDO A RECEBER: R$ {format(total_liquido_descricao, '.4f').replace('.', ',')}|"


        #################################### REPACTUAÇÃO######################################################



        if nota.tipo_de_faturamento == 'FATURAMENTO REPACTUAÇÃO E REQUILIBRIO' and nota.porcentagem_ans is None:
            descricao = f"CONTRATO: {nota.contrato_texto_livre} |\n\n | {nota.texto_livre}"
            
            descricao += f"||TOTAL A FATURAR: R$ {format(total_a_faturar_nota, '.4f').replace('.', ',')}|\n\n BASE PARA RETENÇÕES:|\n\nRETENÇÃO CONFORME LEI 10833/03 - PIS: 0,0065: R$ {format(base_pis, '.4f').replace('.', ',')}|\n\nRETENÇÃO CONFORME LEI 10833/03 - CONFINS: 0,03: R$ {format(base_confins, '.4f').replace('.', ',')}|\n\n INSS RETENÇÃO: 0,11: R$ {format(base_inss, '.4f').replace('.', ',')}|\n\n I.R. RETENÇÃO: 0,048: R$ {format(base_ir, '.4f').replace('.', ',')}|\n\n RETENÇÃO CONFORME LEI 10833/03 - CSLL: 0,01: R$ {format(base_cssl, '.4f').replace('.', ',')}|\n\n RETENÇÃO CONFORME LEI 116/03 - ISS: {format(base_iss, '.4f').replace('.', ',')}|\n\n TOTAL LIQUIDO A RECEBER: R$ {format(total_liquido_descricao, '.4f').replace('.', ',')}|"


        #################################### PRIVADOS######################################################



        if nota.tipo_de_faturamento == 'FATURAMENTO OUTROS' and nota.porcentagem_ans is None:
            descricao = f"{nota.texto_livre}"
            
            descricao += f"||TOTAL A FATURAR: R$ {format(total_a_faturar_nota, '.4f').replace('.', ',')}|\n\n BASE PARA RETENÇÕES:|\n\nRETENÇÃO CONFORME LEI 10833/03 - PIS: 0,0065: R$ {format(base_pis, '.4f').replace('.', ',')}|\n\nRETENÇÃO CONFORME LEI 10833/03 - CONFINS: 0,03: R$ {format(base_confins, '.4f').replace('.', ',')}|\n\n INSS RETENÇÃO: 0,11: R$ {format(base_inss, '.4f').replace('.', ',')}|\n\n I.R. RETENÇÃO: 0,048: R$ {format(base_ir, '.4f').replace('.', ',')}|\n\n RETENÇÃO CONFORME LEI 10833/03 - CSLL: 0,01: R$ {format(base_cssl, '.4f').replace('.', ',')}|\n\n RETENÇÃO CONFORME LEI 116/03 - ISS: {format(base_iss, '.4f').replace('.', ',')}|\n\n TOTAL LIQUIDO A RECEBER: R$ {format(total_liquido_descricao, '.4f').replace('.', ',')}|"





        # aqui, você pode adicionar os outros casos 'MOT' e 'DISTRIBUIÇÃO' de maneira similar
        return descricao

    field_mappings = {
        'D': lambda nota: 'D',
        'sequencial': lambda nota: nota.id,
        'id': lambda nota: nota.id,
        'data_emissao': lambda nota: today,
        'N': lambda nota: 'N',
        'field_total': lambda nota: nota.total_quantidade_de_horas,
        'cnpj_tipo_de_servico': lambda nota: getattr(nota.cnpj_da_nota, 'tipo_de_servico', ''),
        'S': lambda nota: 'S',
        'sempre_em_branco': lambda nota: '',
        'cnpj_cnpj': lambda nota: re.sub(r'\D', '', getattr(nota.cnpj_da_nota, 'cnpj', '')),
        'cnpj_razao': lambda nota: getattr(nota.cnpj_da_nota, 'razao', ''),
        'cnpj_avenida_rua': lambda nota: getattr(nota.cnpj_da_nota, 'avenida_rua', ''),
        'cnpj_endereco': lambda nota: getattr(nota.cnpj_da_nota, 'endereco', ''),
        'cnpj_numero': lambda nota: getattr(nota.cnpj_da_nota, 'numero', ''),
        'cnpj_complemento': lambda nota: getattr(nota.cnpj_da_nota, 'complemento', ''),
        'cnpj_bairro': lambda nota: getattr(nota.cnpj_da_nota, 'bairro', ''),
        'cnpj_municipio': lambda nota: getattr(nota.cnpj_da_nota, 'municipio', ''),
        'cnpj_uf': lambda nota: getattr(nota.cnpj_da_nota, 'uf', ''),
        'cnpj_cep': lambda nota: getattr(nota.cnpj_da_nota, 'cep', ''),
        'email': lambda nota: 'alex.sobreira@go2b.com.br',    
        'id_2': lambda nota: nota.id,
        'descricao': generate_description,
        '0': lambda nota: '0',
    }
    sequential_number = 1  # iniciando o número sequencial para a segunda coluna

    for nota in Notas.objects.all():
        row = []
        for field, get_value in field_mappings.items():
            if field == 'sequencial':  # quando encontramos o campo 'sequencial', substituímos pelo número sequencial
                valor = sequential_number
                sequential_number += 1  # incrementa o número sequencial
            else:
                valor = get_value(nota)  # obtemos o valor usando a função no mapeamento
            row.append(valor)
        writer.writerow(row)

    return response









def gerarcsv_template(request):

    return render(request, 'gerarcsv.html')



class GestaoListView(ListView):
    model = Notas
    template_name = 'gestao.html'
    paginate_by = 10

    def get(self, request, *args, **kwargs):
        self.object_list = self.get_queryset()
        return super().get(request, *args, **kwargs)
    
    def get_queryset(self):
        return super().get_queryset().order_by('data_de_criacao')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        paginator = Paginator(self.object_list, self.paginate_by)
        page_number = self.request.GET.get('page')
        page_obj = paginator.get_page(page_number)
        context = super().get_context_data(**kwargs)
        context['page_obj'] = page_obj

        return context






def notafiscalindividual(request, id):
    notas = Notas.objects.filter(id=id).order_by('-id')
    return render(request, 'pages/recipe-view.html', context={
        'nota_gestao': notas,
        'pag_de_detalhe': True,
    })

def cliente(request, cliente_id):
    notas = Notas.objects.filter(cnpj_da_nota__id=cliente_id).order_by('-id')

    if not notas:
        return HttpResponse(content='Not found', status=404)
    return render(request, 'cliente.html', context={
        'nota_gestao': notas,
        'title_cliente': f'{notas.first().cnpj_da_nota.nome_cliente} | Ametista'
    })




















def qtddecargos(request):
    return render(request, 'qtddecargos.html')





class NotaFiscalCreateView(CreateView):
    model = Notas
    form_class = NotasModelForm
    template_name = 'notafiscal.html'
    success_url = '/notafiscal/'

    def form_valid(self, form):
        messages.success(self.request, 'Nota salva com sucesso.')
        return super().form_valid(form)
    
    

    def form_invalid(self, form):
        messages.error(self.request, 'Erro ao salvar o formulário, por favor verifique as informações preenchidas.')
        return super().form_invalid(form)




# 2 Cargos

def notafiscal2(request):
    if str(request.method) == 'POST':
        form = NotasModelForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            
            messages.success(request, 'Formulario salvo com sucesso')
            form = NotasModelForm()
        else:
            messages.error(request, 'Erro ao salvar o formulario')
            
    else:
        form = NotasModelForm()
    context = {
        'form': form
    }
    return render(request, 'notafiscal2.html', context)

# 3 Cargos

def notafiscal3(request):
    if str(request.method) == 'POST':
        form = NotasModelForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            
            messages.success(request, 'Formulario salvo com sucesso')
            form = NotasModelForm()
        else:
            messages.error(request, 'Erro ao salvar o formulario')
            
    else:
        form = NotasModelForm()
    context = {
        'form': form
    }
    return render(request, 'notafiscal3.html', context)


# 4 Cargos

def notafiscal4(request):
    if str(request.method) == 'POST':
        form = NotasModelForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            
            messages.success(request, 'Formulario salvo com sucesso')
            form = NotasModelForm()
        else:
            messages.error(request, 'Erro ao salvar o formulario')
            
    else:
        form = NotasModelForm()
    context = {
        'form': form
    }
    return render(request, 'notafiscal4.html', context)

# 5 Cargos

def notafiscal5(request):
    if str(request.method) == 'POST':
        form = NotasModelForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            
            messages.success(request, 'Formulario salvo com sucesso')
            form = NotasModelForm()
        else:
            messages.error(request, 'Erro ao salvar o formulario')
            
    else:
        form = NotasModelForm()
    context = {
        'form': form
    }
    return render(request, 'notafiscal5.html', context)

# 6 Cargos

def notafiscal6(request):
    if str(request.method) == 'POST':
        form = NotasModelForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            
            messages.success(request, 'Formulario salvo com sucesso')
            form = NotasModelForm()
        else:
            messages.error(request, 'Erro ao salvar o formulario')
            
    else:
        form = NotasModelForm()
    context = {
        'form': form
    }
    return render(request, 'notafiscal6.html', context)


# 7 Cargos

def notafiscal7(request):
    if str(request.method) == 'POST':
        form = NotasModelForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            
            messages.success(request, 'Formulario salvo com sucesso')
            form = NotasModelForm()
        else:
            messages.error(request, 'Erro ao salvar o formulario')
            
    else:
        form = NotasModelForm()
    context = {
        'form': form
    }
    return render(request, 'notafiscal7.html', context)

# 8 Cargos

def notafiscal8(request):
    if str(request.method) == 'POST':
        form = NotasModelForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            
            messages.success(request, 'Formulario salvo com sucesso')
            form = NotasModelForm()
        else:
            messages.error(request, 'Erro ao salvar o formulario')
            
    else:
        form = NotasModelForm()
    context = {
        'form': form
    }
    return render(request, 'notafiscal8.html', context)


def cnpj(request):
    if str(request.method) == 'POST':
        form = BaseCNPJModelForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            
            messages.success(request, 'Formulario salvo com sucesso')
            form = BaseCNPJModelForm()
        else:
            messages.error(request, 'Erro ao salvar o formulario')
            
    else:
        form = BaseCNPJModelForm()
    context = {
        'form': form
    }
    return render(request, 'cnpj.html', context)



def fatoutros(request):
    if str(request.method) == 'POST':
        form = NotasModelForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            
            messages.success(request, 'Formulario salvo com sucesso')
            form = NotasModelForm()
        else:
            messages.error(request, 'Erro ao salvar o formulario')
            
    else:
        form = NotasModelForm()
    context = {
        'form': form
    }
    return render(request, 'fatoutros.html', context)








def update_basecnpj(request):
    if request.method == 'POST':
        excel_file = request.FILES['excel_file']
        update_basecnpj_from_excel(excel_file)
        return render(request, 'atualizar_cnpj.html', {'success': True})
    return render(request, 'atualizar_cnpj.html')

def import_basecnpj(request):
    if request.method == 'POST':
        excel_file = request.FILES['excel_file']
        import_basecnpj_from_excel(excel_file)
        return render(request, 'import_basecnpj.html', {'success': True})
    return render(request, 'import_basecnpj.html')