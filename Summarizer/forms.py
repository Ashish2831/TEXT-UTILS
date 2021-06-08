from django import forms
from django.utils.translation import gettext as _
from django.core.exceptions import ValidationError

class Text_Form(forms.Form):
    textarea = forms.CharField(label='', widget=forms.Textarea(attrs={'cols' : 60, 'rows' : 10, 'placeholder' : 'Enter The Text Here', 'class' : 'form-control'}), required=False) 

    def clean_textarea(self):
        inp_textarea = self.cleaned_data.get('textarea')
        if len(inp_textarea.strip()) == 0:
            raise ValidationError(_("Please Enter The Text!!"))
        return inp_textarea

class File_Form(forms.Form):
    file = forms.FileField(label="File", widget=forms.FileInput(attrs={'class' : 'form-control'}), required=False)

    def clean_file(self):
        inp_file = self.cleaned_data.get('file')
        if inp_file == None:
            raise ValidationError(_("Please Upload The File!!"))
        allowed_types = ["application/pdf", "text/plain"]
        if inp_file.content_type not in allowed_types:
            raise ValidationError(_("Supported Formats: PDF, TEXT Only!"))
        if inp_file.size > (1024 * 5000):
            raise ValidationError(_("Size Should Not Be Greater Than 5 MB!"))
        return inp_file