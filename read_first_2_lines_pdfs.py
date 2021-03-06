from pathlib import Path
import os
import PyPDF2

##Used to extract text from all PDFs in a given folder and extract first N number of lines and save results to pdf_extracted.txt in users home directory
##It also extracts author and title and saves with extracted lines in pdf_extracted.txt
print("This will check every file in the folder to see if it is a pdf\nif it is then it will open the file, copy the first 2 lines\nand put them in a text file in your home dir pdf_first_2_lines.txt\nNOTE: this does not check any nested folders.")

given_folder = input("Folder path from home dir (i.e. desktop, documents\pdfFolder: ")
num_of_lines = input("How many lines of text to extract: ")
folder = str(Path.home()) + '\\'+given_folder
#folder = 'c:\\users\\jake\\documents'
results_file = str(Path.home())+'\pdf_extracted.txt'
try:
    first_2_lines = open(str(Path.home())+'\pdf_extracted.txt', 'x').close()
except FileExistsError:
    input("File already exists in home directory, press enter to overwrite.")
    os.remove(str(Path.home())+'\pdf_first_2_lines.txt')
    first_2_lines = open(str(Path.home())+'\pdf_extracted.txt', 'x').close()
    
print("File created")
for file in os.scandir(folder):
    if file.path.endswith('.pdf'):
        pdf = open(file, 'rb')
        readpdf = PyPDF2.PdfFileReader(pdf)
        information = readpdf.getDocumentInfo()
        page = readpdf.getPage(0)
        text = page.extractText()
        head = f"""
                Author: {information.author}
                Title: {information.title}
                """
        with open('tmp.txt', 'a') as f:
            try:
                f.write(text)
            except UnicodeEncodeError:
                f.write('first page of pdf contains unsupported characters (e.g. nontext)')
            f.close
        with open('tmp.txt', 'r') as f:   
            lines = f.readlines(num_of_lines)
            with open(results_file, 'a') as f2l:
                results = (str(head) +'\r\n'+str(lines)+'\r\n--------------')
                f2l.write(results+'\r\n')
                f2l.close
            f.close()
        os.remove('tmp.txt')
