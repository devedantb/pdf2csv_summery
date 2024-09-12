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

def ask_and_get_insights(request, doc_path=None):
    # print(request.method)
    if request.method == 'POST' and doc_path!=None:
        try:
            text_json = load_json(doc_path)
            text_json = combine_documents_to_text(text_json)
            texts = text_json
        except:
            text_csv = load_csv(doc_path)
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
                'doc_path':doc_path,
                'question': question,
                'answer': re.sub(r'\*', '', result['answer'])
            }
            return render(request, 'app_doc_summarization/index.html', context=context)
    print('outside the POST')
    return render(request, 'app_doc_summarization/index.html', context={'doc_path':doc_path})