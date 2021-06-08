from django import forms
from django.core.exceptions import ValidationError
from django.utils.translation import gettext as _

class File_Form(forms.Form):
    file = forms.FileField(label="File", widget=forms.FileInput(attrs={'class' : 'form-control'}), required=False)

    def clean_file(self):
        inp_file = self.cleaned_data.get('file')
        if inp_file == None:
            raise ValidationError(_("Please Upload The File!!"))
        allowed_types = ["image/bmp", "image/gif", "image/jpeg", "image/svg+xml", "image/tiff", "image/webp", "image/apng", "image/avif", "image/png"]
        if inp_file.content_type not in allowed_types:
            raise ValidationError(_("Please Upload Files With Valid Extension!"))
        if inp_file.size > (1024 * 5000):
            raise ValidationError(_("Size Should Not Be Greater Than 5 MB!"))
        return inp_file

