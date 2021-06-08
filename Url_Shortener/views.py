from django.shortcuts import render
from .forms import *
import pyshorteners

# Create your views here.
def UrlShortener(request):
    emp_uf = Url_Form()
    if request.method == 'POST':
        uf = Url_Form(request.POST)
        if uf.is_valid():
            url = uf.cleaned_data.get('url')
            shortener = pyshorteners.Shortener()
            shorten = shortener.tinyurl.short(url)          
            return render(request, 'Url_Shortener/urlShortener.html', {'uf' : emp_uf, 'url' : shorten})
        else:
            return render(request, 'Url_Shortener/urlShortener.html', {'uf': uf})
    return render(request, 'Url_Shortener/urlShortener.html', {'uf' : emp_uf})