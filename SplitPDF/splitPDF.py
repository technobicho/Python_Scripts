# import the neccessary modules
import os, PyPDF2, re

# function to extract the individual pages from each pdf found
def split_pdf_pages(root_directory, extract_to_folder):
 # traverse down through the root directory to sub-directories
 for root, dirs, files in os.walk(root_directory):
  for filename in files:
   basename, extension = os.path.splitext(filename)
   # if a file is a pdf
   if extension == ".pdf":
    # create a reference to the full filename path
    fullpath = root + "\\" + basename + extension

    # open the pdf in read mode
    opened_pdf = PyPDF2.PdfFileReader(open(fullpath,"rb"))

    # for each page in the pdf
    for i in range(opened_pdf.numPages):
    # write the page to a new pdf
     output = PyPDF2.PdfFileWriter()
     output.addPage(opened_pdf.getPage(i))
     with open(extract_to_folder + "\\" + basename + "-%s.pdf" % i, "wb") as output_pdf:
      output.write(output_pdf)
    

# function for renaming the single page pdfs based on text in the pdf
def rename_pdfs(extraced_pdf_folder, rename_folder):
 # traverse down through the root directory to sub-directories
 for root, dirs, files in os.walk(extraced_pdf_folder):
  for filename in files:
   basename, extension = os.path.splitext(filename)
   # if a file is a pdf
   if extension == ".pdf":
    # create a reference to the full filename path
    fullpath = root + "\\" + basename + extension

    # open the individual pdf
    pdf_file_obj = open(fullpath, "rb")
    pdf_reader = PyPDF2.PdfFileReader(pdf_file_obj)

    # access the individual page
    page_obj = pdf_reader.getPage(0)
    # extract the the text
    pdf_text = page_obj.extractText()
    #Clean text
    clean_text = pdf_text.replace("\n","")
    print(clean_text)
    # use regex to find information
    doc_nit = re.search('(?<=Ind.impuestos acreedor )\w+', clean_text)
    doc_num = "NIT_" + doc_nit.group(0)
    pdf_file_obj.close()
      # rename the pdf based on the information in the pdf
    os.rename(fullpath, rename_folder + "\\" + doc_num + ".pdf")

# parameter variables
root_dir = r"C:\Users\dacostac\Downloads\test_pdf\rename_pdf"
extract_to = r"C:\Users\dacostac\Downloads\test_pdf\extracted"
rename_to = r"C:\Users\dacostac\Downloads\test_pdf\renamed"

# use the two functions
split_pdf_pages(root_dir, extract_to)
rename_pdfs(extract_to,rename_to)