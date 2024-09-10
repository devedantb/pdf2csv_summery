import os
import json
from django.shortcuts import render, get_object_or_404
from app_pdf_csv_processing.models import DocumentData
# from csv2summery.csvai import 

# Create your views here.
def ask_and_get_insights(request, json_file_url=None):
    print(json_file_url)
    if request.method == 'POST':
        question = request.POST.get('question')
    return render(request, 'app_doc_summarization/index.html')