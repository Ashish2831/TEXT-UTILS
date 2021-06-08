from django.shortcuts import render, HttpResponseRedirect
from django.contrib import messages
from better_profanity import profanity
from .forms import *

# Create your views here.
def Profanity(request):
    if not request.user.is_authenticated:
        messages.error(request, "The Page You Are Trying To Visit is Login Protected.")
        return HttpResponseRedirect('/login/')
    emp_tf = Text_Form()
    if request.method == 'POST':
        tf = Text_Form(request.POST)
        if tf.is_valid():
            text = tf.cleaned_data.get('textarea')
            profanity.load_censor_words()
            custom_words = ['swear', 'abuse']
            profanity.add_censor_words(custom_words)
            output = profanity.censor(text)
            return render(request, 'Profanity_Filter/profanity.html', {'tf' : emp_tf, 'output' : output})
        else:
            return render(request, 'Profanity_Filter/profanity.html', {'tf' : tf})
    return render(request, 'Profanity_Filter/profanity.html', {'tf' : emp_tf})
