from django import forms
from django.core.exceptions import ValidationError
from django.utils.translation import gettext as _

class File_Form(forms.Form):
    choices = (('Language','Select Language'), ('en-US','English'), ('hi-IN','Hindi'), ('mr-IN','Marathi'))
    language = forms.ChoiceField(label_suffix="", choices=choices, widget=forms.Select(attrs={'class' : 'form-control'}))
    video_file = forms.FileField(widget=forms.FileInput(attrs={'class' : 'form-control', 'aria-describedby' : 'inputGroupFileAddon04', 'aria-label' : 'Upload'}), required=False) 

    def clean_language(self):
        lang = self.cleaned_data.get("language")
        if lang == "Language":
            raise ValidationError(_("Please Select Language!!"))
        return lang

    def clean_video_file(self):
        inp_video_file = self.cleaned_data.get("video_file")
        if inp_video_file == None:
            raise ValidationError(_("Please Upload File!!"))
        allowed_types = ['video/x-flv', 'video/mp4', 'application/x-mpegURL', 'video/MP2T', 'video/3gpp', 'video/quicktime', 'video/x-msvideo', 'video/x-ms-wmv']
        if inp_video_file.content_type not in allowed_types:
            raise ValidationError(_("Please Upload File With Valid Extension!!"))
        if inp_video_file.size > (1024 * 5000):
            raise ValidationError(_("Size Should Not Be Greater Than 5 MB!!"))
        return inp_video_file 