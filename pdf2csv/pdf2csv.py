# source >> https://nbviewer.org/github/chezou/tabula-py/blob/master/examples/tabula_example.ipynb
import tabula


# help(tabula.read_pdf)
#This function converts a PDF file to a CSV file and saves the output to the specified path.
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

if __name__ == '__main__':
    # convert_pdf2csv(pdf_path='inp_pdf/Balance-Sheet-Example.pdf', csv_path='output_csv/Balance-Sheet-Example.csv', output_format="csv", pages="all")
    tabula.convert_into('inp_pdf/Balance-Sheet-Example.pdf', 'output_csv/Balance-Sheet-Example.txt', output_format='csv', pages='all')