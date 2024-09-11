import os
import re
import json
from django.shortcuts import render, get_object_or_404
from app_pdf_csv_processing.models import DocumentData
from csv2summery.csvai import load_json, load_csv, combine_documents_to_text, getDocumentInsights, createVectorDB_retriever, llm
from langchain_core.messages import AIMessage, HumanMessage

# Create your views here.

# replace chat history with session
chat_history:list=[]

def ask_and_get_insights(request, json_file_url=None):
    # print(request.method)
    if request.method == 'POST' and json_file_url!=None:
        try:
            text_json = load_json(json_file_url)
            text_json = combine_documents_to_text(text_json)
            texts = text_json
        except:
            text_csv = load_csv(json_file_url)
            text_csv = combine_documents_to_text(text_csv)
            texts = text_csv
        # print('inside the POST')
        
        question = request.POST.get('question')
        if texts :
            retriever = createVectorDB_retriever(texts)
            result = getDocumentInsights(question,retriever,llm,chat_history=chat_history)
            chat_history.append(HumanMessage(content=question))
            chat_history.append(AIMessage(content=result["answer"]))
            context = {
                'json_file_url':json_file_url,
                'question': question,
                'answer': re.sub(r'\*', '', result['answer'])
            }
            return render(request, 'app_doc_summarization/index.html', context=context)
    print('outside the POST')
    return render(request, 'app_doc_summarization/index.html', context={'json_file_url':json_file_url})