from django import forms
from django.core.exceptions import ValidationError
from django.utils.translation import gettext as _

class Single_Form(forms.Form):
    text = forms.CharField(label="Enter Single Review", widget=forms.TextInput(attrs={'class' : 'form-control', 'placeholder' : 'Single Review Here'}), required=False)

    def clean_text(self):
        inp_text = self.cleaned_data.get('text')
        if len(inp_text) == 0:
            raise ValidationError(_("Please Enter Review!"))
        return inp_text

class Multiple_Form(forms.Form):
    file = forms.FileField(label="Upload Your Input CSV File", widget=forms.FileInput(attrs={'class' : 'form-control col-sm-12'}), required=False) 
    
    def clean_file(self):
        inp_file = self.cleaned_data.get('file')
        if inp_file == None:
            raise ValidationError(_("Please Upload Reviews File!"))
        allowed_types = ["text/plain", "text/csv", "application/vnd.ms-excel"]
        if inp_file.content_type not in allowed_types:
            raise ValidationError(_("Supported Formats: TEXT, CSV Only!"))
        if inp_file.size > (1024 * 5000):
            raise ValidationError(_("Size Should Not Be Greater Than 5 MB!"))
        return inp_file