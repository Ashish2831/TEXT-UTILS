"""Text_Utils URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from django.conf.urls.static import static
from . import settings

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('Utils.urls')),
    path('accounts/', include('allauth.urls')),
    path('features/summarizer/', include('Summarizer.urls')),
    path('features/profanityfilter/', include('Profanity_Filter.urls')),
    path('features/urlshortener/', include('Url_Shortener.urls')),
    path('features/textextracter/', include('Text_Extracter.urls')),
    path('features/sentimentanalysis/', include('Sentiment_Analysis.urls')),
    path('features/Translator/', include('Translator.urls')),
    path('features/Image_Comparator/', include('Image_Comparator.urls')),
    path('features/Pdf_Merging/', include('Pdf_Merging.urls')),
    path('features/Audio_Transcribing/', include('Audio_Transcribing.urls')),
    path('features/Video_Transcribing/', include('Video_Transcribing.urls')),
    path('features/Speech_Recognition/', include('Speech_Recognition.urls')),
    path('features/wordcloud/', include('WordCloud.urls')),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
