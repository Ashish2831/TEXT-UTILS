from django import forms
from django.core.exceptions import ValidationError
from django.utils.translation import gettext as _

class Url_Form(forms.Form):
    url = forms.CharField(label="", widget=forms.TextInput(attrs={'class' : 'form-control', 'placeholder' : 
    'Paste long url and shorten it'}), required=False)

    def clean_url(self):
        inp_url = self.cleaned_data['url']
        if len(inp_url.strip()) == 0:
            raise ValidationError(_("Please Enter URL!!"))  
        return inp_url