from django.shortcuts import render, HttpResponseRedirect
from django.contrib import messages
from .forms import *
from PIL import Image, ImageChops

# Create your views here.
def CompareImages(request):
    if not request.user.is_authenticated:
        messages.error(request, "The Page You Are Trying To Visit is Login Protected.")
        return HttpResponseRedirect('/login/')
    emp_form = CompareImagesForm()
    if request.method == "POST":
        form = CompareImagesForm(request.POST, request.FILES)
        if form.is_valid():
            image1 = form.cleaned_data.get("image1")
            image2 = form.cleaned_data.get("image2")
            with open("Image_Comparator/static/Image_Comparator/Images/Image1.jpg", "wb+") as img1:
                for chunk in image1.chunks():
                    img1.write(chunk)

            with open("Image_Comparator/static/Image_Comparator/Images/Image2.jpg", "wb+") as img2:
                for chunk in image2.chunks():
                    img2.write(chunk)

            Img1 = Image.open("Image_Comparator/static/Image_Comparator/Images/Image1.jpg")
            Img2 = Image.open("Image_Comparator/static/Image_Comparator/Images/Image2.jpg")
            diff = ImageChops.difference(Img1, Img2)
            getbbox = diff.getbbox()
            if getbbox:
                diff.show()
            return render(request, 'Image_Comparator/compareimages.html', {'form' : form, 'image' : True, 'getbbox' : getbbox})
        else:
            return render(request, 'Image_Comparator/compareimages.html', {'form' : form})
    return render(request, 'Image_Comparator/compareimages.html', {'form' : emp_form})