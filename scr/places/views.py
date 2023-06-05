from django.contrib.auth.decorators import login_required
from places.models import Place
from django.shortcuts import render, redirect, get_object_or_404
from .forms import AddPlaceForm
from config.settings import yandex_api_key


@login_required
def places(request):
    profile_places = Place.objects.filter(profile=request.user.profile)
    return render(request, 'places.html', {'profile_places': profile_places})


@login_required
def add_place(request):
    api_key = yandex_api_key
    if request.method == 'POST':
        form = AddPlaceForm(request.POST)
        if form.is_valid():
            place = form.save(commit=False)
            place.profile = request.user.profile
            place.save()
            return redirect('places:places')
    else:
        form = AddPlaceForm()

    return render(request, 'add_place.html', {'form': form, 'api_key': api_key})


@login_required
def place_detail(request, slug):
    place = get_object_or_404(Place, slug=slug)
    api_key = yandex_api_key

    if request.method == 'POST':
        form = AddPlaceForm(request.POST, instance=place)
        if form.is_valid():
            form.save()
            return redirect('places:places')
    else:
        form = AddPlaceForm(instance=place)

    return render(request, 'place_detail.html', {'form': form, 'place': place, 'api_key': api_key})


@login_required
def place_delete(request, slug):
    place_to_delete = Place.objects.get(profile=request.user.profile, slug__iexact=slug)
    place_to_delete.delete()
    return redirect('places:places')


def handler404(request, exception):
    return render(request, 'errors/404.html', status=404)


def handler500(request):
    return render(request, 'errors/500.html', status=500)
