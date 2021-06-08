from django.shortcuts import render
from .forms import *
from googletrans import Translator

# Create your views here.
def Translate(request):
    emp_tf = Trans_Form()
    output = ""
    if request.method == 'POST':
        tf = Trans_Form(request.POST)   
        if tf.is_valid(): 
            translator = Translator()
            Text = tf.cleaned_data.get('textarea')
            To = tf.cleaned_data.get('language')
            translator = Translator(service_urls=['translate.googleapis.com'])
            output = translator.translate(Text, dest=To)
        else:
            return render(request, 'Translator/translator.html', {'tf' : tf})
    return render(request, 'Translator/translator.html', {'tf' : emp_tf, 'output' : output})