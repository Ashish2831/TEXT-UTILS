from django.shortcuts import render
from .forms import *
import nltk
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize, sent_tokenize 
import numpy as np
import networkx as nx
from pdfminer import high_level

def summarize(file):
    with open(file, 'r') as f:
        text = f.read()

    # Tokenizing the text 
    stopWords = set(stopwords.words("english")) 
    words = word_tokenize(text) 

    # Creating a frequency table to keep the 
    # score of each word 

    freqTable = dict() 
    for word in words: 
        word = word.lower() 
        if word in stopWords: 
            continue
        if word in freqTable: 
            freqTable[word] += 1
        else: 
            freqTable[word] = 1

    # Creating a dictionary to keep the score 
    # of each sentence 
    sentences = sent_tokenize(text) 
    sentenceValue = dict() 

    for sentence in sentences: 
        for word, freq in freqTable.items(): 
            if word in sentence.lower(): 
                if sentence in sentenceValue: 
                    sentenceValue[sentence] += freq 
                else: 
                    sentenceValue[sentence] = freq 

    sumValues = 0
    for sentence in sentenceValue: 
        sumValues += sentenceValue[sentence] 

    # Average value of a sentence from the original text 

    average = int(sumValues / len(sentenceValue)) 

    # Storing sentences into our summary. 
    summary = '' 
    for sentence in sentences: 
        if (sentence in sentenceValue) and (sentenceValue[sentence] > (1.2 * average)): 
            summary += " " + sentence 
    return summary 

def Summarizer(request):
    emp_tf = Text_Form()
    emp_ff = File_Form()
    return render(request, 'Summarizer/summarise.html', {'tf' : emp_tf, 'ff' : emp_ff})

def Summarize_Text(request):
    emp_tf = Text_Form()
    emp_ff = File_Form()
    summary = ""
    if request.method == 'POST':
        tf = Text_Form(request.POST)
        if tf.is_valid():
            text = tf.cleaned_data.get('textarea')
            with open('UploadedMedia/Summarizer/Text/Text.txt', 'w') as txt:
                txt.write(text)
            summary = summarize('UploadedMedia/Summarizer/Text/Text.txt')
            return render(request, 'Summarizer/summarise.html', {'tf' : emp_tf, 'ff' : emp_ff, 'summary' : summary})
        else:
            return render(request, 'Summarizer/summarise.html', {'tf' : tf, 'ff' : emp_ff})    
    return render(request, 'Summarizer/summarise.html', {'tf' : emp_tf, 'ff' : emp_ff})

def Summarize_File(request):
    emp_tf = Text_Form()
    emp_ff = File_Form()
    summary = ""
    if request.method == 'POST':
        ff = File_Form(request.POST, request.FILES)
        if ff.is_valid():
            file = ff.cleaned_data.get('file')
            if file.name.split('.')[1] == 'pdf':
                with open('UploadedMedia/Summarizer/Text/Text.pdf', 'wb+') as pdf:
                    for chunk in file.chunks():
                        pdf.write(chunk)

                local_pdf_filename = 'UploadedMedia/Summarizer/Text/Text.pdf'
                pages = len(list(high_level.extract_pages(local_pdf_filename)))

                with open('UploadedMedia/Summarizer/Text/Text.txt', 'w') as txt:         
                    for page in range(pages):
                        extracted_text = high_level.extract_text(local_pdf_filename, "", [page])
                        txt.write(extracted_text)

                summary = summarize('UploadedMedia/Summarizer/Text/Text.txt') 
            else:
                with open('UploadedMedia/Summarizer/Text/Text.txt', 'wb+') as txt:
                    for chunk in file.chunks():
                        txt.write(chunk)
                summary = summarize('UploadedMedia/Summarizer/Text/Text.txt')       
        else:
            return render(request, 'Summarizer/summarise.html', {'tf' : emp_tf, 'ff' : ff})

        return render(request, 'Summarizer/summarise.html', {'tf' : emp_tf, 'ff' : emp_ff, 'summary' : summary})
    return render(request, 'Summarizer/summarise.html', {'tf' : emp_tf, 'ff' : emp_ff})
