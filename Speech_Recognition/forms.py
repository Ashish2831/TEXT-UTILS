from django import forms

class Voice_Form(forms.Form):
    choices = (('male', 'Male'), ('female', 'Female'))
    gender = forms.ChoiceField(choices=choices, widget=forms.Select(), required=False)
    text = forms.CharField(widget=forms.TextInput(attrs={'placeholder' : 'Text'}), required=False)