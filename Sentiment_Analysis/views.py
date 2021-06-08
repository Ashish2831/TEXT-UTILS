from django.shortcuts import render, HttpResponseRedirect
from django.contrib import messages
from django.http import JsonResponse
from .forms import *
from textblob import TextBlob
from collections import Counter
from nltk.corpus import stopwords
from nltk.sentiment.vader import SentimentIntensityAnalyzer
from nltk.stem import WordNetLemmatizer
from nltk.tokenize import word_tokenize
from matplotlib import pyplot as plt
# from PIL import Image
import string
import os


def Sentiment_Analyse(sentiment_text):
    score = SentimentIntensityAnalyzer().polarity_scores(sentiment_text)
    if score['neg'] > score['pos']:
        return "Negative"
    elif score['neg'] < score['pos']:
        return "Positive"
    else:
        return "Neutral"

# Create your views here.
def Sentiment(request):
    if not request.user.is_authenticated:
        messages.error(request, "The Page You Are Trying To Visit is Login Protected.")
        return HttpResponseRedirect('/login/')
    emp_sf = Single_Form()
    emp_mf = Multiple_Form()
    if request.method == "POST":
        sf = Single_Form(request.POST)
        if sf.is_valid():
            inp_text = sf.cleaned_data.get("text")
            edu = TextBlob(inp_text)
            response = edu.sentiment.polarity
            if 'okay' in inp_text.lower() or 'ok' in inp_text.lower():
                text = "Neutral"
            elif response < 0:
                text = "Negative"
            elif response == 0:
                text = "Neutral"
            else:
                text = "Positive"
            return render(request, 'Sentiment_Analysis/sentiment.html', {'sf' : sf, 'mf' : emp_mf, 'text' : text})
        else:
            return render(request, 'Sentiment_Analysis/sentiment.html', {'sf' : sf, 'mf' : emp_mf})
    if os.path.isfile("Sentiment_Analysis\static\Sentiment_Analysis\Images\graph.png"):        
        os.remove("Sentiment_Analysis\static\Sentiment_Analysis\Images\graph.png")
    return render(request, 'Sentiment_Analysis/sentiment.html', {'sf' : emp_sf, 'mf' : emp_mf})

def Sentiment_Multiple(request):
    emp_sf = Single_Form()
    if request.method == "POST":
        mf = Multiple_Form(request.POST, request.FILES)
        if mf.is_valid():
            file = mf.cleaned_data.get("file")
            with open("UploadedMedia/SentimentAnalysis/reviews.txt", 'wb+') as txt:
                for chunk in file.chunks():
                    txt.write(chunk)
            text = open('UploadedMedia/SentimentAnalysis/reviews.txt', encoding='utf-8').read()
            lower_case = text.lower()
            cleaned_text = lower_case.translate(str.maketrans('', '', string.punctuation))

            # Using word_tokenize because it's faster than split()
            tokenized_words = word_tokenize(cleaned_text, "english")

            # Removing Stop Words
            final_words = []
            for word in tokenized_words:
                if word not in stopwords.words('english'):
                    final_words.append(word)

            # Lemmatization - From plural to single + Base form of a word (example better-> good)
            lemma_words = []
            for word in final_words:
                word = WordNetLemmatizer().lemmatize(word)
                lemma_words.append(word)

            emotion_list = []
            with open('UploadedMedia/SentimentAnalysis/emotions.txt', 'r') as file:
                for line in file:
                    clear_line = line.replace("\n", '').replace(",", '').replace("'", '').strip()
                    word, emotion = clear_line.split(':')

                    if word in lemma_words:
                        emotion_list.append(emotion)

            # print(emotion_list)
            w = Counter(emotion_list)

            sentiment = Sentiment_Analyse(cleaned_text)

            fig, ax1 = plt.subplots()
            ax1.bar(w.keys(), w.values())
            fig.autofmt_xdate()
            plt.savefig('Sentiment_Analysis/static/Sentiment_Analysis/Images/graph.png')
            plt.show()
            # im = Image.open('Sentiment_Analysis/static/Sentiment_Analysis/Images/graph.png')
            # im.show()
            return render(request, 'Sentiment_Analysis/sentiment.html', {'sf' : emp_sf, 'mf' : mf, 'text' : sentiment, 'graph' : True})
        else:
            return render(request, 'Sentiment_Analysis/sentiment.html', {'sf' : emp_sf, 'mf' : mf})
    if os.path.isfile("Sentiment_Analysis\static\Sentiment_Analysis\Images\graph.png"):        
        os.remove("Sentiment_Analysis\static\Sentiment_Analysis\Images\graph.png")
    return HttpResponseRedirect('/features/sentimentanalysis/')