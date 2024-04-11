from django.shortcuts import render, redirect, get_object_or_404
from .models import Video
from .forms import VideoForm, SearchForm
from django.contrib import messages
from django.db import IntegrityError
from django.core.exceptions import ValidationError
from django.db.models.functions import Lower
from pprint import pprint
# Create your views here.

def home(request):
    app_name = 'Exercise Videos'
    return render(request, 'video_collection/home.html', {'app_name': app_name})

#You already added that video
def add(request):
    if request.method == "POST": # add a new video via post request.
        new_video_form = VideoForm(request.POST)
        if new_video_form.is_valid():
            try:
                new_video_form.save()
                return redirect('video_list') # save and redirect.
            except ValidationError:
                messages.warning(request, 'Invalid YouTube URL') # Bad URL.
            except IntegrityError:
                messages.warning(request, 'You already added that video') # Duplicate Video.

        # form is not valid so we tell the user to check their data.
        messages.warning(request, 'Check the data entered')
        return render(request, 'video_collection/add.html', {'new_video_form' : new_video_form})

    new_video_form = VideoForm()
    return render(request, 'video_collection/add.html', {'new_video_form' : new_video_form})

def video_list(request):
    search_form = SearchForm(request.GET)

    if search_form.is_valid(): # Make sure search is valid
        search_term = search_form.cleaned_data['search_term']
        videos = Video.objects.filter(name__icontains=search_term).order_by(Lower('name')) # order by search term
    else:
        search_form = SearchForm() # no search term so do by name exclusively.
        videos = Video.objects.order_by(Lower('name'))

    return render(request, 'video_collection/video_list.html', {'videos' : videos, 'search_form': search_form})

def video_info(request, video_pk):
    video = get_object_or_404(Video, pk=video_pk) # Use primary key for video indexing.
    return render(request, 'video_collection/video_info.html', {'video': video})
