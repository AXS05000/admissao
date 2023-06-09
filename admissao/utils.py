from docx import Document


def generate_contract(template, collaborator):
    # Load the Word document
    doc = Document(template.file.path)

    # Loop through each paragraph
    for paragraph in doc.paragraphs:
        # Replace the keys in the text
        for run in paragraph.runs:
            if run.text.find('{nome}') != -1:
                run.text = run.text.replace('{nome}', collaborator.name)
            if run.text.find('{cpf}') != -1:
                run.text = run.text.replace('{cpf}', collaborator.cpf)
            if run.text.find('{admissão}') != -1:
                run.text = run.text.replace('{admissão}', str(collaborator.admission_date))
            if run.text.find('{rg}') != -1:
                run.text = run.text.replace('{rg}', collaborator.rg)
        # Do the same for other replacements...

    # Save the new Word document
    new_contract_filename = f'contracts/{collaborator.name}_{template.name}.docx'
    doc.save(new_contract_filename)

    return new_contract_filename
