from django.db import models
from django.shortcuts import reverse
from users.models import Profile
from django.utils.text import slugify
from transliterate import translit
import re
from datetime import datetime


class Place(models.Model):
    title = models.CharField(max_length=100)
    location = models.CharField(max_length=100)
    comment = models.TextField(blank=True, db_index=True)
    slug = models.SlugField(max_length=100, db_index=True)
    profile = models.ForeignKey(Profile, on_delete=models.CASCADE)

    class Meta:
        app_label = 'places'

    def save(self, *args, **kwargs):
        timestamp = datetime.now().strftime('%Y%m%d%H%M%S')
        slug = slugify(translit(self.title.__str__(), "ru", reversed=True), allow_unicode=True)
        slug = re.sub(r'[^a-zA-Z0-9_-]', '', slug)  # Исключаем специальные символы
        self.slug = f"{slug}-{self.pk}-{timestamp}"
        super().save(*args, **kwargs)

    def get_absolute_url(self):
        return reverse('place_detail', kwargs={'slug': self.slug})

    def __str__(self):
        return self.title
