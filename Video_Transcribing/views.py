from django.shortcuts import render, HttpResponseRedirect
from django.contrib import messages
from .forms import *
import os
import speech_recognition as sr 
import moviepy.editor as mp
from pydub import AudioSegment
from pydub.utils import which
AudioSegment.converter = which("ffmpeg")
from pydub import AudioSegment
from pydub.silence import split_on_silence

r = sr.Recognizer()

def get_transcribed_text(path, lang):
    clip = mp.VideoFileClip(path)  
    clip.audio.write_audiofile(r"UploadedMedia/Video_Transcribing/Audio/converted.wav")

    # Splitting the large audio file into chunks and apply speech recognition on each of these chunks
    # open the audio file using pydub
    sound = AudioSegment.from_file("UploadedMedia/Video_Transcribing/Audio/converted.wav")
    # split audio sound where silence is 700 miliseconds or more and get chunks
    chunks = split_on_silence(sound,
        # experiment with this value for your target audio file
        min_silence_len = 500,
        # adjust this per requirement
        silence_thresh = sound.dBFS-14,
        # keep the silence for 1 second, adjustable as well
        keep_silence=200,
    )
    folder_name = "UploadedMedia/Video_Transcribing/Audio-Chunks"
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

    for file in os.listdir("UploadedMedia/Video_Transcribing/Audio-Chunks"):
        os.remove(f"UploadedMedia/Video_Transcribing/Audio-Chunks/{file}")

    # return the text for all chunks detected
    return whole_text

# Create your views here.
def Video_Transcribing(request):
    if not request.user.is_authenticated:
        messages.error(request, "The Page You Are Trying To Visit is Login Protected.")
        return HttpResponseRedirect('/login/')
    emp_form = File_Form()
    if request.method == "POST":
        form = File_Form(request.POST, request.FILES)
        if form.is_valid():
            video = form.cleaned_data.get("video_file")
            lang = form.cleaned_data.get("language")
            with open("UploadedMedia/Video_Transcribing/Video/video.mp4", "wb+") as mp4:
                for chunk in video.chunks():
                    mp4.write(chunk)
            text = get_transcribed_text("UploadedMedia/Video_Transcribing/Video/video.mp4", lang)
            return render(request, "Video_Transcribing/video_transcribing.html", {'form' : form, 'text' : text})
        else:
            return render(request, "Video_Transcribing/video_transcribing.html", {'form' : form})
    return render(request, "Video_Transcribing/video_transcribing.html", {'form' : emp_form})