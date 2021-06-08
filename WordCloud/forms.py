from django import forms
from django.core.exceptions import ValidationError
from django.utils.translation import gettext as _
from django.forms.widgets import Select

class Select_Form(forms.Form):
    choices = (('1', 'Select Shape'), ('1','Cloud'),('2','Bottle'),('3','Home'),('4','Love'),('5','Butterfly'),('6','Corona'),('7','Apple'),('8','Woman'),('9','Shape1'),('10','Bell'),('11','Round_circle'),('12','Hexagon1'),('13','Shield'),('14','Unbounded'),('15','Tiger'),('16','Bomb'),('17','Hexagon2'),('18','Crack1'),('19','Leaf'),('20','Fire'),('21','Hexagon3'),('22','Kite'),('23','Shield1'),('24','Round_square'),('25','Crack2'),('26','Coupon1'),('27','Ox'),('28','Men'),('29','Smile'),('30','Snapchat'),('31','Fingure'),('32','BigLeaf'),('33','Sparrow'),('34','Pigon'),('35','Coupon2'),('36','Trophy1'),('37','Coupon3'),('38','Trophy2'),('39','Mug'),('40','Triangle'),('41','Batman'),('42','Water'),('43','RoundedTriangle'),('44','Human'),('45','Flash'),('46','PressButton'),('47','Bat1'),('48','Flask'),('49','Triangular'),('50','Bat2'))
    select = forms.ChoiceField(label="Select Shape", label_suffix="", choices=choices, widget=forms.Select(attrs={'class' : 'form-control'}))

class Word_Form(forms.Form):
    word = forms.CharField(label="Add Words", label_suffix="", widget=forms.TextInput(attrs={'class' : 'form-control', 'placeholder' : 
    'Enter a Word'}), required=False)

    def clean_word(self):
        inp_word = self.cleaned_data.get("word")
        if len(inp_word) == 0:
            raise ValidationError(_("Please Enter Word!"))
        return inp_word

class Word_Text_Form(forms.Form):
    textarea = forms.CharField(label='', widget=forms.Textarea(attrs={'cols' : 60, 'rows' : 10, 'placeholder' : 'Enter The Text Here And Generate Cloud', 'class' : 'form-control'}), required=False)

    def clean_textarea(self):
        inp_textarea = self.cleaned_data.get("textarea")
        if len(inp_textarea) == 0:
            raise ValidationError(_("Please Enter Text!"))
        return inp_textarea

class Word_File_Form(forms.Form):
    file = forms.FileField(label='', widget=forms.FileInput(attrs={'class' : 'form-control'}), required=False)

    def clean_file(self):
        inp_file = self.cleaned_data.get("file")
        if inp_file == None:
            raise ValidationError(_("Please Upload Files!"))
        allowed_types = ["application/pdf", "text/plain"]
        if inp_file.content_type not in allowed_types:
            raise ValidationError(_("Supported Formats: PDF, TEXT Only!"))
        if inp_file.size > (1024 * 5000):
            raise ValidationError(_("Size Should Not Be Greater Than 5 MB!"))
        return inp_file