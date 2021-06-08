from django.shortcuts import render, HttpResponseRedirect
from django.contrib import messages
from .forms import *
import easyocr
from pylab import rcParams
from IPython.display import Image
rcParams['figure.figsize'] = 8, 16

# Create your views here.
def TextExtracter(request):
    if not request.user.is_authenticated:
        messages.error(request, "The Page You Are Trying To Visit is Login Protected.")
        return HttpResponseRedirect('/login/')
    emp_ff = File_Form()
    if request.method == 'POST':
        ff = File_Form(request.POST, request.FILES)
        if ff.is_valid():
            file = ff.cleaned_data.get('file')
            reader = easyocr.Reader(['en'])
            with open('UploadedMedia/Text_Extracter/Images/Text.jpg', 'wb+') as jpg:         
                for chunk in file.chunks():
                    jpg.write(chunk)
            output = reader.readtext('UploadedMedia/Text_Extracter/Images/Text.jpg')
            text = ""
            for tup in output:
                text = text + tup[1] + "\n"
        else:
            return render(request, 'Text_Extracter/textExtracter.html', {'ff' : ff})
        return render(request, 'Text_Extracter/textExtracter.html', {'ff' : emp_ff, 'extract' : text})
    return render(request, 'Text_Extracter/textExtracter.html', {'ff' : emp_ff})