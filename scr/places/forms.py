import re
from django import forms
from .models import Place
from django.core.exceptions import ValidationError
from django.db import models
from django.utils.text import slugify

class AddPlaceForm(forms.ModelForm):
    class Meta:
        model = Place
        fields = ['title', 'location', 'comment']

    def clean_title(self):
        title = self.cleaned_data['title']
        slug = slugify(title, allow_unicode=True)

        if self.instance.pk is None or title != self.initial['title']:
            place_exists = Place.objects.filter(
                models.Q(title=title) | models.Q(slug=slug)
            ).exists()

            if place_exists:
                raise ValidationError('Место с таким названием или слагом уже существует.')

        if not re.match(r'^[\w\s.-]+$', title):
            raise ValidationError('Название места содержит недопустимые символы.')

        return title

    def save_form(self, profile):
        new_place = Place.objects.update_or_create(
            title=self.cleaned_data['title'],
            location=self.cleaned_data['location'],
            comment=self.cleaned_data['comment'],
            profile=profile
        )
        return new_place
