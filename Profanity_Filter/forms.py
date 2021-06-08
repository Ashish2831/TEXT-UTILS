from django import forms
from django.core.exceptions import ValidationError
from django.utils.translation import gettext as _

class Text_Form(forms.Form):
    textarea = forms.CharField(label='', widget=forms.Textarea(attrs={'cols' : 60, 'rows' : 10, 'placeholder' : 'Enter The Text Here', 'class' : 'form-control'}), required=False)

    def clean_textarea(self):
        inp_textarea = self.cleaned_data.get('textarea')
        if len(inp_textarea.strip()) == 0:
            raise ValidationError(_("Please Enter The Text!!"))
        return inp_textarea