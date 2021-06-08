from django import forms
from django.core.exceptions import ValidationError
from django.utils.translation import gettext as _

class CompareImagesForm(forms.Form):
    image1 = forms.FileField(widget=forms.FileInput(attrs={'class' : 'form-control'}), required=False)
    image2 = forms.FileField(widget=forms.FileInput(attrs={'class' : 'form-control'}), required=False)

    def clean_image1(self):
        inp_image1 = self.cleaned_data.get("image1")
        if inp_image1 == None:
            raise ValidationError(_("Please Upload Image1"))
        allowed_types = ['image/apng', 'image/avif', 'image/gif', 'image/jpeg', 'image/png', 'image/svg+xml', 'image/webp']
        if inp_image1.content_type not in allowed_types:
            raise ValidationError(_("Please Upload Image With Valid Extension!!"))
        if inp_image1.size > (1024 * 256):
            raise ValidationError(_("Size of Image Should Not Be Greater Than 256 kB!!"))
        return inp_image1

    def clean_image2(self):
        inp_image2 = self.cleaned_data.get("image2")
        if inp_image2 == None:
            raise ValidationError(_("Please Upload Image2"))
        allowed_types = ['image/apng', 'image/avif', 'image/gif', 'image/jpeg', 'image/png', 'image/svg+xml', 'image/webp']
        if inp_image2.content_type not in allowed_types:
            raise ValidationError(_("Please Upload Image With Valid Extension!!"))
        if inp_image2.size > (1024 * 5000):
            raise ValidationError(_("Size of Image Should Not Be Greater Than 5 MB!!"))
        return inp_image2