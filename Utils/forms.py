from django import forms
from .models import *
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import password_validation
from django.utils.translation import gettext as _
from django.core.exceptions import ValidationError
from django.core.validators import EmailValidator
from django.contrib.auth.forms import AuthenticationForm, UsernameField, PasswordResetForm, PasswordChangeForm, SetPasswordForm

class Registration_Form(UserCreationForm):
    password1 = forms.CharField(label="Password", widget=forms.PasswordInput(attrs={'class' : 'form-control', 'placeholder' : 'Enter Your Password'}), required=False)
    password2 = forms.CharField(label="Confirm Password", widget=forms.PasswordInput(attrs={'class' : 'form-control', 'placeholder' : 'Confirm Your Password'}), required=False)
    
    def __init__(self, *args, **kwargs):
        super(Registration_Form, self).__init__(*args, **kwargs)
        self.label_suffix = ""
        self.fields.get('username').required = False
    
    class Meta:
        model = User
        fields = ['username', 'email', 'first_name', 'last_name']

        labels = {
            'first_name' : 'First Name',
            'last_name' : 'Last Name',
            'email' : 'Email',
        }

        widgets = {
            'username' : forms.TextInput(attrs={'class' : 'form-control', 'placeholder' : 'Username'}),
            'first_name' : forms.TextInput(attrs={'class' : 'form-control', 'placeholder' : 'First Name'}),
            'last_name' : forms.TextInput(attrs={'class' : 'form-control', 'placeholder' : 'Last Name'}),
            'email' : forms.TextInput(attrs={'class' : 'form-control', 'placeholder' : 'Email'}),
        }

        help_texts = {
            'username' : "You can keep it same as your email!",
        }

    def clean_username(self):
        inp_username = self.cleaned_data.get('username')
        if len(inp_username) == 0:
            raise ValidationError(_("Please Enter Username!"))
        return inp_username

    def clean_first_name(self):
        inp_first_name = self.cleaned_data.get('first_name')
        if len(inp_first_name) == 0:
            raise ValidationError(_("Please Enter First Name!"))
        return inp_first_name

    def clean_last_name(self):
        inp_last_name = self.cleaned_data.get('last_name')
        if len(inp_last_name) == 0:
            raise ValidationError(_("Please Enter Last Name!"))
        return inp_last_name

    def clean_email(self):
        inp_email = self.cleaned_data.get('email')
        if len(inp_email) == 0:
            raise ValidationError(_("Please Enter Email!"))
        validator = EmailValidator(_("Please Enter Valid Email!")) 
        validator(inp_email)
        if User.objects.filter(email=inp_email, is_active=True).exists():
            raise ValidationError(_(f"{inp_email} Already Exists!"))
        return inp_email

    def clean_password1(self):
        inp_password1 = self.cleaned_data.get('password1')
        if len(inp_password1) == 0:
            raise ValidationError(_("Please Enter Password!"))
        if len(inp_password1) < 8:
            raise ValidationError(_("Password Must Be of 8 Characters!"))
        return inp_password1

    def clean_password2(self):
        inp_password1 = self.data.get('password1')
        inp_password2 = self.cleaned_data.get('password2')
        if len(inp_password2) == 0:
            raise ValidationError(_("Please Confirm Your Password!"))
        if inp_password1 != inp_password2:
            raise ValidationError(_("Password and Confirm Password Must Matched!"))
        return inp_password2

class UserProfileForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super(UserProfileForm, self).__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            field.required = False

    class Meta:
        model = UserProfile
        fields = "__all__"

        widgets = {
            'profile_picture' : forms.FileInput(attrs={'style' : 'visibility : hidden', 'class' : 'form-control'}),
            'address' : forms.TextInput(attrs={'class' : 'form-control', 'placeholder' : 'Home Address'}),
            'city' : forms.TextInput(attrs={'class' : 'form-control', 'placeholder' : 'City'}),
            'country' : forms.TextInput(attrs={'class' : 'form-control', 'placeholder' : 'Country'}),
            'postal_code' : forms.TextInput(attrs={'class' : 'form-control', 'placeholder' : 'Postal Code'}),
            'profession' : forms.TextInput(attrs={'class' : 'form-control', 'placeholder' : 'Profession'}),
            'university' : forms.TextInput(attrs={'class' : 'form-control', 'placeholder' : 'University'}),
            'about_me' : forms.Textarea(attrs={'class' : 'form-control', 'placeholder' : 'A Few Words About You......', 'rows' : '4'}),
        }

    def clean_profile_picture(self):
        inp_profile_picture = self.cleaned_data.get('profile_picture', False)
        if type(inp_profile_picture) != 'django.db.models.fields.files.FieldFile':
            # Means no file uploaded so go for default file
            return inp_profile_picture 
        elif inp_profile_picture == False:
            return 'no_photo.jpg'
        else:
            allowed_type = ['image/jpeg', 'image/png', 'image/gif']
            if inp_profile_picture.content_type not in allowed_type:
                raise ValidationError(_("Please Upload File With Valid Extension!"))
            if inp_profile_picture.size > (1024 * 250):
                raise ValidationError(_("Please Upload File Upto 250 KB!"))
        return inp_profile_picture
        
class Login_Form(AuthenticationForm):
    username = UsernameField(widget=forms.TextInput(attrs={'autofocus': True, 'class' : 'form-control text-dark', 'placeholder' : 'Username'}), required=False)
    password = forms.CharField(
        label=_("Password"),
        strip=False,
        widget=forms.PasswordInput(attrs={'autocomplete': 'current-password', 'class' : 'form-control text-dark', 'placeholder' : "Password"}),required=False
    )
    
    def clean_username(self):
        inp_username = self.cleaned_data.get('username')
        if len(inp_username) == 0:
            raise ValidationError(_("Please Enter Username!"))
        return inp_username

    def clean_password(self):
        inp_password = self.cleaned_data.get('password')
        if len(inp_password) == 0:
            raise ValidationError(_("Please Enter Password!"))
        return inp_password

class Reset_Password_Form(PasswordResetForm):
    email = forms.EmailField(
        label=_("Email"),
        label_suffix=_(""),
        max_length=254,
        widget=forms.EmailInput(attrs={'autocomplete': 'email', 'class' : 'form-control', 'placeholder' : 'Enter Your Email'}),
        required=False
    )

    def clean_email(self):
        inp_email = self.cleaned_data.get('email')
        if len(inp_email) == 0:
            raise ValidationError(_("Please Enter Email!"))
        validator = EmailValidator(_("Please Enter a Valid Email Address!"))
        validator(inp_email)
        if not User.objects.filter(email=inp_email, is_active=True).exists():
            raise ValidationError(_("Provided Email Does Not Exist. Please Register Yourself!"))
        return inp_email

class Password_Change_Form(PasswordChangeForm):
    old_password = forms.CharField(
        label=_("Old password"),
        strip=False,
        widget=forms.PasswordInput(attrs={'autocomplete': 'current-password', 'autofocus': True, 'class' : 'form-control', 'placeholder' : "Enter Your Old Password"}),
    )

    new_password1 = forms.CharField(
        label=_("New password"),
        widget=forms.PasswordInput(attrs={'autocomplete': 'new-password', 'class' : 'form-control', 'placeholder' : "Enter Your New Password"}),
        strip=False,
        help_text=password_validation.password_validators_help_text_html(),
    )

    new_password2 = forms.CharField(
        label=_("New password confirmation"),
        strip=False,
        widget=forms.PasswordInput(attrs={'autocomplete': 'new-password', 'class' : 'form-control', 'placeholder' : "Confirm Your New Password"}),
    )

class Forgot_Password_Form(SetPasswordForm):
    new_password1 = forms.CharField(
        label=_("New password"),
        widget=forms.PasswordInput(attrs={'autocomplete': 'new-password', 'class' : 'form-control', 'placeholder' : 'New Password'}),
        strip=False,
        help_text=password_validation.password_validators_help_text_html(),
        required=False,
    )
    new_password2 = forms.CharField(
        label=_("New password confirmation"),
        strip=False,
        widget=forms.PasswordInput(attrs={'autocomplete': 'new-password', 'class' : 'form-control', 'placeholder' : 'New Password Confirmation'}),
        required=False,
    )
    
    def clean_new_password1(self):
        inp_password1 = self.cleaned_data.get('new_password1')
        if len(inp_password1) == 0:
            raise ValidationError(_("Please Enter Password!"))
        if len(inp_password1) < 8:
            raise ValidationError(_("Password Must Be of 8 Characters!"))
        return inp_password1

    def clean_new_password2(self):
        inp_password1 = self.data.get('new_password1')
        inp_password2 = self.cleaned_data.get('new_password2')
        if len(inp_password2) == 0:
            raise ValidationError(_("Please Confirm Your Password!"))
        if inp_password1 != inp_password2:
            raise ValidationError(_("Password and Confirm Password Must Matched!"))
        return inp_password2

class Contact_Form(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super(Contact_Form, self).__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            field.required = False

    class Meta:
        model = Contacts
        fields = '__all__'

        widgets = {
            'name' : forms.TextInput(attrs={'class' : 'input100', 'placeholder' : 'Name'}),
            'email' : forms.EmailInput(attrs={'class' : 'input100', 'placeholder' : 'Email'}),
            'mobile' : forms.TextInput(attrs={'class' : 'input100', 'placeholder' : 'Mobile Number'}),
            'message' : forms.Textarea(attrs={'class' : 'input100', 'placeholder' : 'Message', 'rows' : '5'})
        }

    def clean_name(self):
        inp_name = self.cleaned_data.get("name")
        if len(inp_name) == 0:
            raise ValidationError(_("Name is required!!"))
        return inp_name

    def clean_email(self):
        inp_email = self.cleaned_data.get("email")
        if len(inp_email) == 0:
            raise ValidationError(_("Email is required!!"))
        validator = EmailValidator(_("Please Enter Valid Email!!"))
        validator(inp_email)
        return inp_email

    def clean_mobile(self):
        inp_mobile = self.cleaned_data.get("mobile")
        if len(inp_mobile) == 0:
            raise ValidationError(_("Mobile Number is required!!"))
        return inp_mobile

    def clean_message(self):
        inp_message = self.cleaned_data.get("message")
        if len(inp_message) == 0:
            raise ValidationError(_("Message is required!!"))
        return inp_message
