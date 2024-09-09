# source >> https://nbviewer.org/github/chezou/tabula-py/blob/master/examples/tabula_example.ipynb
import tabula


# help(tabula.read_pdf)
def convert_pdf2csv(pdf_path:str, csv_path:str, output_format="csv", pages="all")-> None:
    # convert PDF into CSV file
    tabula.convert_into(pdf_path, csv_path, output_format=output_format, pages=pages)

    # convert all PDFs in a directory
    # tabula.convert_into_by_batch("input_directory", output_format='csv', pages='all')
    return None

def read_pdf(pdf_path:str, pages="all")->list[str,int]:
    # dfs >> data frames
    dfs = tabula.read_pdf(pdf_path, pages=pages)
    return dfs

# convert_pdf2csv(pdf_path='inp_pdf/NL-1.pdf', csv_path='output_csv/NL-1.csv', output_format="csv", pages="all")

# PDF_Data_Organizer/pdf2csv/inp_pdf/NL-1.pdf