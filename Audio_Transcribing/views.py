from django.shortcuts import render, HttpResponseRedirect
from django.contrib import messages
from .forms import *
import speech_recognition as sr 
import os
from pydub import AudioSegment
from pydub.utils import which
AudioSegment.converter = which("ffmpeg")
from pydub import AudioSegment
from pydub.silence import split_on_silence

# create a speech recognition object
r = sr.Recognizer()

# a function that splits the audio file into chunks
# and applies speech recognition
def get_large_audio_transcription(path, lang):
    """
    Splitting the large audio file into chunks
    and apply speech recognition on each of these chunks
    """
    # open the audio file using pydub
    sound = AudioSegment.from_file(path)
    # split audio sound where silence is 700 miliseconds or more and get chunks
    chunks = split_on_silence(sound,
        # experiment with this value for your target audio file
        min_silence_len = 500,
        # adjust this per requirement
        silence_thresh = sound.dBFS-14,
        # keep the silence for 1 second, adjustable as well
        keep_silence=200,
    )
    folder_name = "UploadedMedia/Audio_Transcribing/Audio-Chunks"
    # create a directory to store the audio chunks
    if not os.path.isdir(folder_name):
        os.mkdir(folder_name)
    whole_text = ""
    # process each chunk 
    for i, audio_chunk in enumerate(chunks, start=1):
        # export audio chunk and save it in
        # the `folder_name` directory.
        chunk_filename = os.path.join(folder_name, f"chunk{i}.wav")
        audio_chunk.export(chunk_filename, format="wav")
        # recognize the chunk
        with sr.AudioFile(chunk_filename) as source:
            audio_listened = r.record(source)
            # try converting it to text
            try:
                text = r.recognize_google(audio_listened, language=lang)
            except sr.UnknownValueError as e:
                whole_text += "\n[Inaudible]\n"
            else:
                text = f"{text.capitalize()}. "
                whole_text += text

    for file in os.listdir("UploadedMedia/Audio_Transcribing/Audio-Chunks"):
        os.remove(f"UploadedMedia/Audio_Transcribing/Audio-Chunks/{file}")

    # return the text for all chunks detected
    return whole_text

# Create your views here.
def Audio_Transcribing(request):
    if not request.user.is_authenticated:
        messages.error(request, "The Page You Are Trying To Visit is Login Protected.")
        return HttpResponseRedirect('/login/')
    emp_form = File_Form()
    if request.method == "POST":
        form = File_Form(request.POST, request.FILES)
        if form.is_valid():
            file = form.cleaned_data.get("audio_file")
            lang = form.cleaned_data.get("language")
            with open("UploadedMedia/Audio_Transcribing/Audio/audio.mp3", "wb+") as audio:
                for chunk in file.chunks():
                    audio.write(chunk)
            text = get_large_audio_transcription("UploadedMedia/Audio_Transcribing/Audio/audio.mp3", lang)
            return render(request, "Audio_Transcribing/audio_transcribing.html", {'form' : form, 'text' : text})
        else:
            return render(request, "Audio_Transcribing/audio_transcribing.html", {'form' : form})
    return render(request, "Audio_Transcribing/audio_transcribing.html", {'form' : emp_form})