from django import forms
from .models import Place
from django.core.exceptions import ValidationError


class AddPlaceForm(forms.ModelForm):
    class Meta:
        model = Place
        fields = ['title', 'location', 'comment']

    def clean_title(self):
        title = self.cleaned_data['title']
        if self.instance.pk is None or title != self.initial['title']:
            place_exists = Place.objects.filter(title=title).exists()
            if place_exists:
                raise ValidationError('Место с таким названием уже существует.')
        return title

    def save_form(self, profile):
        new_place = Place.objects.update_or_create(
            title=self.cleaned_data['title'],
            location=self.cleaned_data['location'],
            comment=self.cleaned_data['comment'],
            profile=profile
        )
        return new_place
