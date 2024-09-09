import os

def save_uploaded_file(file_contents:str, filename:str, UPLOAD_DIR='pdf2csv/inp_pdf')->str:
    filepath = os.path.join(UPLOAD_DIR, filename)
    with open(filepath, "wb") as f:
        f.write(file_contents)
    return filepath

def delete_file(filepath:str)->bool:
    try:
        os.remove(filepath)
        return True
    except FileNotFoundError:
        return False