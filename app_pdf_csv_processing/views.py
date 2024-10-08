import os
import re
import json
from django.shortcuts import render, redirect
from django.http import HttpResponseRedirect
from .forms import UploadFileForm
from django.http import FileResponse
from django.conf import settings
from pdf2csv.pdf_ops import save_uploaded_file, delete_file
from PDF_Data_Organizer.settings import BASE_DIR
from pdf2csv.pdf2csv import convert_pdf2csv
from csv2summery.csvai import llm ,load_json, load_csv, combine_documents_to_text, createVectorDB_retriever, getDocumentInsights
from csv2summery.csv2json import make_json
from .models import DocumentData

# Create your views here.
def get_summery_from_json(json_file_path, question:str=None, llm=llm):
    question = '''Please provide a brief summary of the JSON file, 
            including its main content and purpose, 
            so that someone can understand the data without opening the file. 
            '''
    text_json = load_json(json_file_path)
    text_json = combine_documents_to_text(text_json)
    retriever = createVectorDB_retriever(text_json)
    
    result = getDocumentInsights(question,retriever,llm)
    return result

def get_summery_from_csv(csv_file_name,question:str=None, llm=llm):
    question = '''Please provide a brief summary of the CSV file, 
            including its main content and purpose, 
            so that someone can understand the data without opening the file. 
            '''

    text_csv = load_csv(csv_file_name) 
    text_csv = combine_documents_to_text(text_csv)
    retriever = createVectorDB_retriever(text_csv)
    result = getDocumentInsights(question,retriever,llm)
    return result

def get_json_data(json_file_path:str):
    with open(json_file_path, 'r') as file:
        # Load the JSON data
        json_data = json.load(file)
    return json_data if json_data else None

def index(request):
    if request.method=='POST':
        pdf_file = request.FILES["files"]
        contents = pdf_file.read()
        saved_filepath = save_uploaded_file(filename=str(pdf_file), file_contents=contents)
        pdf_path = os.path.join(BASE_DIR, saved_filepath)
        csv_file_name = str(pdf_file).replace('.pdf','.csv')
        csv_file_name = f'pdf2csv/output_csv/{str(csv_file_name)}'
        csv_path = os.path.join(BASE_DIR, csv_file_name)
        
        convert_pdf2csv(pdf_path=pdf_path, csv_path=csv_path)
        os.remove(pdf_path) # removing pdf files as those are tempo
        json_file_name = str(pdf_file).replace('.pdf','.json')
        json_file_name = f'app_pdf_csv_processing/json_data/{str(json_file_name)}'
        doc_path = json_file_name
        json_file_path = os.path.join(BASE_DIR, json_file_name)

        pk = 1
        try:
            make_json(csv_path, json_file_path=json_file_path)
            result = get_summery_from_json(json_file_path)
            data = get_json_data(json_file_path)
            if data is not None:
                json_data = DocumentData(name=json_file_name, data=json.dumps(data), description=re.sub(r'\*', '', result['answer']))
                json_data.save()
                pk = json_data.id
            else:
                print(f'data is {data}')
        except:
            result = get_summery_from_csv(csv_path)
            doc_path = csv_file_name
            json_file_name = csv_file_name
        summary = re.sub(r'\*', '', result['answer'])

        return render(request, 'app_pdf_csv_processing/output.html', {'csv_file_url': csv_file_name, 'summary':summary, 'doc_path':doc_path})
    return render(request, 'app_pdf_csv_processing/index.html')

def download_csv(request, csv_file_url:str):
    # Check if the file exists
    if not os.path.exists(csv_file_url):
        return HttpResponse('File not found.', status=404)

    # Serve the file
    response = FileResponse(open(csv_file_url, 'rb'), as_attachment=True, content_type='text/csv')
    response['Content-Disposition'] = f'attachment; filename="{os.path.basename(csv_file_url)}"'
    return response

