from django.shortcuts import render, redirect
from django.http import HttpResponseRedirect
from .forms import UploadFileForm
from django.http import FileResponse
from django.conf import settings
from pdf2csv.pdf_ops import save_uploaded_file, delete_file
import os
from PDF_Data_Organizer.settings import BASE_DIR
from pdf2csv.pdf2csv import convert_pdf2csv


# Create your views here.
def index(request):
    if request.method=='POST':
        pdf_file = request.FILES["files"]
        # print(str(pdf_file))
        contents = pdf_file.read()
        # print(type(filename))
        saved_filepath = save_uploaded_file(filename=str(pdf_file), file_contents=contents)
        # print(os.path.join(BASE_DIR, saved_filepath))
        pdf_path = os.path.join(BASE_DIR, saved_filepath)
        # print(pdf_path)
        # print(BASE_DIR)
        csv_file_name = str(pdf_file).replace('.pdf','.csv')
        csv_file_name = f'pdf2csv/output_csv/{str(csv_file_name)}'
        csv_path = os.path.join(BASE_DIR, csv_file_name)
        convert_pdf2csv(pdf_path=pdf_path, csv_path=csv_path)
        print(os.remove(pdf_path))
        print(f'CSV PATH >>>>> {csv_path}')

        summery = 'Lorem ipsum, dolor sit amet consectetur adipisicing elit. Explicabo nostrum alias nulla quidem dolor pariatur assumenda architecto, numquam nobis, voluptates veniam delectus debitis perferendis quod minus rerum suscipit deleniti quisquam!'

        return render(request, 'app_pdf_csv_processing/output.html', {'csv_file_url': csv_file_name, 'summery':summery})
    return render(request, 'app_pdf_csv_processing/index.html')

def get_csv_and_summery(request, csv_file_url:str):
    # Check if the file exists
    if not os.path.exists(csv_file_url):
        return HttpResponse('File not found.', status=404)

    # Serve the file
    response = FileResponse(open(csv_file_url, 'rb'), as_attachment=True, content_type='text/csv')
    response['Content-Disposition'] = f'attachment; filename="{os.path.basename(csv_file_url)}"'
    return response

