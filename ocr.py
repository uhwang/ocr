'''
09/06/2023

python ocr.py input-path input-extension output-path output-pdf

Ex: 
python ocr.py d:/ocr jpg d:/ocr/pdf d:/ocr/pdf/book.pdf
python ocr.py d:/ocr/pdf pdf d:/ocr book.pdf --merge-only

'''
from PIL import Image
import sys
import pathlib
import pytesseract as ocr
from pypdf import PdfMerger

# change the path if necessary
ocr.pytesseract.tesseract_cmd = r'C:\\Tesseract-OCR\\tesseract.exe'

def print_usage():
    print("python [path1] [ext1] [path2] [ofile] [--merge-only]\n"
          "path1 : input folder\n"
          "ext1  : the extension of input files(jpg or png or pdf)\n"
          "path2 : subfolder name under path1\n"
          "ofile : output file(ex: aaa.pdf\n"
          "--merge-only: merge multiple pdfs(ext must be pdf)"
          "Ex) python aaa\bbb png ./ book.pdf")

def save(options):

    if len(options) < 4: 
        print_usage()
        return
        
    path1 = pathlib.Path(options[0])
    ext  = options[1]
    path2 = pathlib.Path(options[2])
    
    print("=> List all files")
    files = [f for f in path1.glob("*.%s"%ext) if f.is_file()]
    print("=> %d files"%len(files))
    
    print("=> Create output folder")
    
    if path2.exists() == False:
        try:
            path2.mkdir()
        except Exception as e:
            print("... Error: %s\n... Fail to create %s"%
                 (e,path2))
            return False
            
    print("=> Success")
    
    if "--merge-only" in options:
        pdf_list = files
    else:
        
        pdf_list = []
        
        for i_, f_ in enumerate(files):
            #f_in = pathlib.Path.joinpath(path1, f_)
            f_in = f_
            f_out= pathlib.Path.joinpath(path2, "%s.pdf"%f_.stem)
            print("%s --> %s"%(str(f_in),str(f_out)))
            
            try:
                pdf = ocr.image_to_pdf_or_hocr(str(f_in), extension='pdf')
                with open(str(f_out), 'w+b') as f:
                    f.write(pdf) # pdf type is bytes by default
            except Exception as e:
                print("... Error: %s"%e)
                return
            pdf_list.append(f_out)
            #print("=> Converting %d"%i_)
            
    merger = PdfMerger()

    for p in pdf_list:
        merger.append(str(p))
    
    pdf_final = pathlib.Path(options[3])
    merger.write(str(pdf_final))
    merger.close()
    
if __name__ == "__main__":
    save(sys.argv[1:])
