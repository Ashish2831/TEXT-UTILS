from django import forms
from django.core.exceptions import ValidationError
from django.utils.translation import gettext as _

class Trans_Form(forms.Form):
    choices = (('To', 'To'), ('af','Afrikaans'), ('al','Albanian'), ('am','Amharic'), ('ar','Arabic'), ('hy-am','Armenian'), ('az','Azzerbaijani'), ('baq','Basque'), ('be','Belarussian'), ('bn','Bengali'), ('bs','Bosnian'), ('bg','Bulgarian'), ('my','Burmese'), ('ca','Catalan'), ('zh-tw','Chinese(Taiwan)'), ('hr','Croatian'), ('cs','Czech'), ('da','Danish'), ('fa','Dari'), ('nl','Dutch'), ('en','English'), ('et','Estonian'), ('fi','Finnish'), ('fr','French'), ('ka','Grorgian'), ('de','German'), ('el','Greek'), ('gu','Gujarati'), ('ht','Haitian Creale'), ('he','Hebrew'), ('hi','Hindi'), ('hu','Hungarian'), ('is','Icelandic'), ('id','Indonesian'), ('ga','Irish Gaelic'), ('it','Italian'), ('ja','Japanese'), ('kn','Kannada'), ('kk','Kazakh'), ('km','Khmer'), ('ko','Korean'), ('ku','Kurdish'), ('lv','Latvian'), ('mk','Macedonian'), ('ms','Malay'), ('ml','Malayalam'), ('mt','Maltese'), ('mr','Marathi'), ('mn','Mongolian'), ('ne','Nepali'), ('no','Norwegian'), ('ps','Pashto'), ('fa','Parsian'), ('pl','Polish'), ('pt','Portuguese'), ('pa','Punjabi'), ('ro','Romanian'), ('ru','Russian'), ('sr','Serbian'), ('si','Sinhala'), ('sk','Slovak'), ('sl','Slovenian(Slovene)'), ('so','Somali'), ('es','Spanish'), ('sw','Swahili'), ('sv','Swedish'), ('tl','Tagalog'), ('ta','Tamil'), ('te','Telugu'), ('th','Thai'), ('tr','Turkish'), ('uk','Ukrainian'), ('ur','Urdu'), ('uz','Uzbek'), ('vi','Vietnamese'), ('yo','Yoruba'), ('zu','Zulu'))
    language = forms.ChoiceField(choices=choices, widget=forms.Select(attrs={'class' : 'btn btn-light', 'id' : 'output'}))
    textarea = forms.CharField(label='Enter Text',label_suffix="", widget=forms.Textarea(attrs={'cols' : 60, 'rows' : 15, 'placeholder' : 'Enter The Text Here', 'class' : 'form-control'}), required=False)

    def clean_textarea(self):
        inp_textarea = self.cleaned_data.get('textarea')
        if len(inp_textarea.strip()) == 0:
            raise ValidationError(_("Please Enter The Text!!"))
        return inp_textarea

    def clean_language(self):
        inp_language = self.cleaned_data.get('language')
        if inp_language == 'To':
            raise ValidationError(_("Please Select Language!!"))
        return inp_language