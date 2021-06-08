from django.shortcuts import render, HttpResponseRedirect
from .forms import *
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.core.cache import cache
from django.contrib.auth.models import Group
from datetime import datetime

# Create your views here.
def Home(request):
    return render(request, 'Utils/index.html', {'Home' : 'danger'})

def Register(request):
    if request.user.is_authenticated:
        return HttpResponseRedirect('/')
    emp_register = Registration_Form()
    if request.method == 'POST':
        register = Registration_Form(request.POST)
        if register.is_valid():
            messages.success(request, "Registration Completed Successfully!!")
            user = register.save()
            user_profile = UserProfile()
            latest = User.objects.latest('id')
            user_profile.user_id = latest
            user_profile.save()
            user_group = Group.objects.get(name='Users')
            user.groups.add(user_group)
            return render(request, 'Utils/register.html', {'register' : emp_register, 'success' : True})
        else:
            return render(request, 'Utils/register.html', {'register' : register})
    return render(request, 'Utils/register.html', {'register' : emp_register})

def Login(request):
    if request.user.is_authenticated:
        return HttpResponseRedirect('/')
    emp_login_form = Login_Form()
    emp_form = Reset_Password_Form()
    if request.method == "POST":
        login_form = Login_Form(request, request.POST)
        if login_form.is_valid():
            uname = login_form.cleaned_data.get('username')
            upass = login_form.cleaned_data.get('password')
            user = authenticate(username=uname, password=upass)
            if user != None:
                login(request, user)
                return HttpResponseRedirect(f"/dashboard/{user.id}/")
            else:
                return render(request, 'Utils/login.html', {'Login' : 'danger', 'login' : login_form})
        else:
            return render(request, 'Utils/login.html', {'Login' : 'danger', 'login' : login_form, 'form': emp_form})
    return render(request, 'Utils/login.html', {'Login' : 'danger', 'login' : emp_login_form, 'form' : emp_form})

def PasswordReset(request):
    if request.method == "POST":
        emp_login_form = Login_Form()
        form = Reset_Password_Form(request.POST)
        forgot = Forgot_Password_Form(user=request.user)
        if form.is_valid():
            request.session['email'] = form.cleaned_data.get('email')
            return render(request, 'Utils/password_reset.html', {'forgot' : forgot})
        else:
            return render(request, 'Utils/login.html', {'Login' : 'danger', 'login' : emp_login_form, 'form' : form, 'error' : True})
    return HttpResponseRedirect('/login/')

def ResetDone(request):
    if request.method == "POST":
        user = User.objects.get(email=request.session.get('email'))
        forgot = Forgot_Password_Form(user=user, data=request.POST)
        if forgot.is_valid():
            messages.success(request, "Password Reset Successfully!")
            forgot.save()
            request.session.clear()
            return HttpResponseRedirect('/login/')
        else:
            return render(request, 'Utils/password_reset.html', {'forgot' : forgot})
    return HttpResponseRedirect('/login/')

def Logout(request): 
    logout(request)
    cache.clear()
    return HttpResponseRedirect('/login/')

def Password_Change(request):
    if not request.user.is_authenticated:
        messages.error(request, "The Page You Are Trying To Visit is Login Protected. Please Login!")
        return HttpResponseRedirect('/login/')
    emp_form = Password_Change_Form(request.user)
    if request.method == "POST":
        form = Password_Change_Form(request.user, request.POST)
        if form.is_valid():
            form.save()
        else:
            return render(request, 'Utils/password_change.html', {'form' : form})
    return render(request, 'Utils/password_change.html', {'form' : emp_form})

def About(request):
    return render(request, 'Utils/about.html', {'About' : 'danger'})

def Contact(request):
    emp_Form = Contact_Form()
    if request.method == "POST":
        form = Contact_Form(request.POST)
        if form.is_valid():
            messages.success(request, "Form Submitted Successfully!!")
            form.save()
            db = Contacts.objects.latest("id")
            db.date = datetime.now()
            db.save()
        else:
            return render(request, 'Utils/contact.html', {'Contact' : 'danger', 'form' : form})
    return render(request, 'Utils/contact.html', {'Contact' : 'danger', 'form' : emp_Form})

def Features(request):
    if not request.user.is_authenticated:
        messages.error(request, "The Page You Are Trying To Visit is Login Protected.")
        return HttpResponseRedirect('/login/')
    features = Feature.objects.all()
    Search = Search_Form()
    return render(request, 'Utils/features.html', {'Features' : 'danger', 'features' : features, 'Search' : Search})

def Dashboard(request, id):
    if not request.user.is_authenticated:
        messages.error(request, "The Page You Are Trying To Visit is Login Protected.")
        return HttpResponseRedirect('/login/')
    user = User.objects.get(pk=id)
    user_profile = UserProfile.objects.get(user_id=id) 
    emp_register = Registration_Form(instance=user)
    emp_profile = UserProfileForm(instance=user_profile)
    success = True
    if request.method == "POST":
        messages.success(request, "Profile Updated Successfully")
        if request.POST.get('profile_picture-clear',False):     
            # Clear checkbox is checked so delete the old photo and set to default
            # If the photo is already not default
            if os.path.isfile(user_profile.profile_picture.path) and user_profile.profile_picture.name != 'no_photo.jpg':
                os.remove(user_profile.profile_picture.path)
                user_profile.profile_picture = 'no_photo.jpg'

        elif not type(request.FILES.get('profile_picture',0)) is int:
            allowed_types = ['image/jpeg', 'image/png', 'image/gif']
            if request.FILES.get('profile_picture').content_type not in allowed_types:
                success = False
                # Stick to old photo, because no photo uploaded actually
                user_profile.profile_picture = user_profile.profile_picture.name
            
            elif request.FILES.get('profile_picture').size > (1024 * 250):
                success = False

            # New photo uploaded, delete old
            elif os.path.isfile(user_profile.profile_picture.path) and user_profile.profile_picture.name != 'no_photo.jpg':
                os.remove(user_profile.profile_picture.path)
                user_profile.profile_picture = request.FILES.get('profile_picture')

            else:
                user_profile.profile_picture = request.FILES.get('profile_picture')

        else:
            # Stick to old photo, because no photo uploaded actually
            user_profile.profile_picture = user_profile.profile_picture.name
        
        user.username = request.POST.get('username')
        user.email = request.POST.get('email')
        user.first_name = request.POST.get('first_name')
        user.last_name = request.POST.get('last_name')
        user_profile.address = request.POST.get('address')
        user_profile.city = request.POST.get('city')
        user_profile.country = request.POST.get('country')
        user_profile.postal_code = request.POST.get('postal_code')
        user_profile.profession = request.POST.get('profession')
        user_profile.university = request.POST.get('university')
        user_profile.about_me = request.POST.get('about_me')

        # Call to save method
        user.save()
        user_profile.save()

        user = User.objects.get(pk=id)
        user_profile = UserProfile.objects.get(user_id=id) 
        register = Registration_Form(request.POST, instance=user)
        profile = UserProfileForm(request.POST, request.FILES, instance=user_profile)

        request.session['profile'] = user_profile.profile_picture.url
        return render(request, "Utils/dashboard.html", {'register' : register, 'profile' : profile, 
        'user_profile' : user_profile, 'success' : success}) 

    request.session['profile'] = user_profile.profile_picture.url
    return render(request, "Utils/dashboard.html", {'register' : emp_register, 'profile' : emp_profile, 'user_profile' : user_profile, 'success' : success}) 

def Delete_User(request, id):
    user = User.objects.get(pk=id)
    user.delete()
    messages.success(request, "Your Account Deleted Successfully!!")
    return HttpResponseRedirect('/login/')

def Remove_Profile_Picure(request, id):
    user = User.objects.get(pk=id)
    user_profile = UserProfile.objects.get(user_id=user)
    if user_profile.profile_picture != 'no_photo.jpg':
        if os.path.isfile(user_profile.profile_picture.path):
            os.remove(user_profile.profile_picture.path)
    user_profile.profile_picture = 'no_photo.jpg'
    user_profile.save()
    messages.success(request, "Profile Picture Updated Successfully")
    return HttpResponseRedirect(f"/dashboard/{id}")

def Search(request):
    if request.method == "POST":
        search = Search_Form(request.POST)
        if search.is_valid():
            data = search.cleaned_data.get('search')
            features = Feature.objects.filter(text__icontains=data)
            return render(request, 'Utils/features.html', {'Features' : 'danger', 'features' : features, 'Search' : search})
    return HttpResponseRedirect('/features/')

