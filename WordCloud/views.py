from django.shortcuts import render, HttpResponseRedirect
from django.contrib import messages
from .forms import *
from io import FileIO
from os.path import curdir
from typing import Sized
from wordcloud import WordCloud, STOPWORDS
from pdfminer import high_level
import os
from PIL import Image
import numpy as np

curdir = os.path.dirname(__file__)

def create_wordcloud(text, wine_mask):
    stopwords = set(STOPWORDS) 
    wc = WordCloud(background_color='white', contour_width=2, contour_color='black', mask=wine_mask, max_words=50, stopwords=STOPWORDS)
    wc.generate(text)
    wc.to_file(os.path.join(curdir, 'static\\WordCloud\\Images\\wc.png'))  
    im = Image.open("WordCloud\static\WordCloud\Images\wc.png") 
    im.show() 

# Create your views here.
def wordCloud(request):
    select = Select_Form()
    emp_wtform = Word_Text_Form()
    emp_wf = Word_Form()
    file_form = Word_File_Form()
    return render(request, 'WordCloud/wordCloud.html', {'wf' : emp_wf, 'wtform' : emp_wtform, 'select' : select, 'file' : file_form})

words = []
flag = False
def AddWords(request):
    if not request.user.is_authenticated:
        messages.error(request, "The Page You Are Trying To Visit is Login Protected.")
        return HttpResponseRedirect('/login/')
    emp_wtform = Word_Text_Form()
    emp_wf = Word_Form()
    select = Select_Form()
    file_form = Word_File_Form()
    if request.method == 'POST':
        wf = Word_Form(request.POST)
        if wf.is_valid():
            word = wf.cleaned_data.get('word')
            words.append(word) 
            return render(request, 'WordCloud/wordCloud.html', {'wf' : emp_wf, 'wtform' : emp_wtform, 'words' : words, 'select' : select, 'file' : file_form})
        return render(request, 'WordCloud/wordCloud.html', {'wf' : wf, 'wtform' : emp_wtform, 'words' : words, 'select' : select, 'file' : file_form})
    else:
        global flag
        if flag:
            flag = False
            return render(request, 'WordCloud/wordCloud.html', {'wf' : emp_wf, 'wtform' : emp_wtform, 'words' : words, 'select' : select, 'file' : file_form})
        else:
            words.clear()
            return HttpResponseRedirect('/features/wordcloud/')

def GenerateWords(request):
    emp_wtform = Word_Text_Form()
    emp_wf = Word_Form()
    select_form = Select_Form()
    file_form = Word_File_Form()
    if request.method == "POST":
        select = Select_Form(request.POST)
        if select.is_valid():
            choice = select.cleaned_data.get("select")  
            wine_mask = np.array(Image.open(os.path.join(curdir, f'static\\WordCloud\\Images\\{choice}.png')))
            if len(words) == 0:
                return render(request, 'WordCloud/wordCloud.html', {'wf' : emp_wf, 'wtform' : emp_wtform, 'select' : select_form, 'file' : file_form, 'NoWords' : True})
            create_wordcloud(" ".join(words), wine_mask)  
            words.clear()
        return render(request, 'WordCloud/wordCloud.html', {'wf' : emp_wf, 'wtform' : emp_wtform, 'select' : select_form, 'file' : file_form})
    return HttpResponseRedirect('/features/wordcloud/')

def GenerateText(request):
    emp_wf = Word_Form()
    select_form = Select_Form()
    file_form = Word_File_Form()
    if request.method == "POST":
        form = Word_Text_Form(request.POST)
        select = Select_Form(request.POST)
        if form.is_valid() and select.is_valid():
            text = form.cleaned_data.get("textarea")
            file = form.cleaned_data.get("file")
            choice = select.cleaned_data.get("select")  
            wine_mask = np.array(Image.open(os.path.join(curdir, f'static\\WordCloud\\Images\\{choice}.png')))
            create_wordcloud(text, wine_mask)  
        words.clear()
        return render(request, 'WordCloud/wordCloud.html', {'wf' : emp_wf, 'wtform' : form, 'select' : select_form, 'file' : file_form})
    return HttpResponseRedirect('/features/wordcloud/')

def GenerateFile(request):
    emp_wtform = Word_Text_Form()
    emp_wf = Word_Form()
    select_form = Select_Form()
    if request.method == "POST":
        select_form = Select_Form(request.POST)
        file_form = Word_File_Form(request.POST, request.FILES)
        if file_form.is_valid() and select_form.is_valid():
            file = file_form.cleaned_data.get("file")
            choice = select_form.cleaned_data.get("select")
            wine_mask = np.array(Image.open(os.path.join(curdir, f'static\\WordCloud\\Images\\{choice}.png')))

            if file.name.split('.')[1] == 'pdf':
                with open('UploadedMedia/WordCloud/Text.pdf', 'wb+') as pdf:
                    for chunk in file.chunks():
                        pdf.write(chunk)

                local_pdf_filename = 'UploadedMedia/WordCloud/Text.pdf'
                pages = len(list(high_level.extract_pages(local_pdf_filename)))
    
                filetext = ""
                for page in range(pages):
                    extracted_text = high_level.extract_text(local_pdf_filename, "", [page])
                    filetext += extracted_text

            else:
                with open("UploadedMedia/WordCloud/file.txt", 'wb+') as txt:
                    for chunk in file.chunks():
                        txt.write(chunk)
                with open("UploadedMedia/WordCloud/file.txt", encoding="utf8") as txt:
                    filetext = txt.read()    
            create_wordcloud(filetext, wine_mask)  
        words.clear()
        return render(request, 'WordCloud/wordCloud.html', {'wf' : emp_wf, 'wtform' : emp_wtform, 'select' : select_form, 'file' : file_form})
    return HttpResponseRedirect('/features/wordcloud/')

def delete_word(request, index):
    global flag
    flag = True
    words.pop(index)
    return HttpResponseRedirect('/features/wordcloud/addwords/')