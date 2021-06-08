from django.shortcuts import render
import PyPDF2
import os

# Create your views here.
index = 1
def Upload(request):
    global index
    if request.method == "POST":
        file = request.FILES.get('file')
        with open(f"UploadedMedia\Pdf_Merging\PDFs\Pdf{index}.pdf", "wb+") as pdf:
            for chunk in file.chunks():
                pdf.write(chunk)
        index += 1
    return render(request, 'Pdf_Merging/pdfMerge.html')

def Merge(request):
    if request.method == "POST":
        # Create a new PdfFileWriter object which represents a blank PDF document
        pdfWriter = PyPDF2.PdfFileWriter()

        files = []
        for file in os.listdir("UploadedMedia\Pdf_Merging\PDFs"):
            # Open the files that have to be merged one by one
            pdfFile = open(f"UploadedMedia\Pdf_Merging\PDFs\{file}", 'rb')

            # Read the files that you have opened
            pdfReader = PyPDF2.PdfFileReader(pdfFile)

            # Loop through all the pagenumbers for the first document
            for pageNum in range(pdfReader.numPages):
                pageObj = pdfReader.getPage(pageNum)
                pdfWriter.addPage(pageObj)

            files.append(pdfFile)
            
        # Now that you have copied all the pages in all the documents, write them into the a new document
        pdfOutputFile = open('Pdf_Merging\static\Pdf_Merging\MergePDF\MergedFiles.pdf', 'wb')
        pdfWriter.write(pdfOutputFile)

        # Close all the files - Created as well as opened
        pdfOutputFile.close()
        for file in files:
            file.close()
        return render(request, 'Pdf_Merging/pdfMerge.html', {'download' : True})
        
    for file in os.listdir("UploadedMedia/Pdf_Merging/PDFs"):
        os.remove(f"UploadedMedia/Pdf_Merging/PDFs/{file}")
    return render(request, 'Pdf_Merging/pdfMerge.html')
