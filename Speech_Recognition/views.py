from django.shortcuts import render, HttpResponseRedirect
from django.contrib import messages
from .forms import *
import pyttsx3
import speech_recognition as sr

def Speech():
    r = sr.Recognizer()

    with sr.Microphone() as source:
        r.adjust_for_ambient_noise(source)

        audio = r.listen(source)

        # recognize speech using google

        try:
            print("You have said \n" + r.recognize_google(audio))
            print("Audio Recorded Successfully \n ")


        except Exception as e:
            print("Error :  " + str(e))

        # write audio
        with open("recorded.wav", "wb") as f:
            f.write(audio.get_wav_data())

def Voice(text, gender):
    engine = pyttsx3.init()
    voices = engine.getProperty('voices')
    if gender == 'male':
        engine.setProperty('voice', voices[0].id)
    else:
        engine.setProperty('voice', voices[1].id)
    engine.say(text)
    engine.setProperty('rate', 120)
    engine.setProperty('volume', 0.9)
    engine.runAndWait()

# Create your views here.
def SpeechRecognition(request):
    if not request.user.is_authenticated:
        messages.error(request, "The Page You Are Trying To Visit is Login Protected.")
        return HttpResponseRedirect('/login/')
    return render(request, 'Speech_Recognition/speechrecognition.html', {'speech' : True})

def BrowserVoice(request):
    if not request.user.is_authenticated:
        messages.error(request, "The Page You Are Trying To Visit is Login Protected.")
        return HttpResponseRedirect('/login/')
    emp_form = Voice_Form()
    if request.method == "POST":
        form = Voice_Form(request.POST)
        if form.is_valid():
            gender = form.cleaned_data.get("gender")
            text = form.cleaned_data.get("text")
            Voice(text, gender)
        else:
            return render(request, 'Speech_Recognition/speechrecognition.html', {'speech' : True, 'form' :form })
    return render(request, 'Speech_Recognition/browservoice.html', {'speech' : True, 'form' : emp_form})