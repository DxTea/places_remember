from django.db import models
from django.shortcuts import reverse
from users.models import Profile
from django.utils.text import slugify
from transliterate import translit


class Place(models.Model):
    title = models.CharField(max_length=100)
    location = models.CharField(max_length=100)
    comment = models.TextField(blank=True, db_index=True)
    slug = models.SlugField(max_length=100, db_index=True)
    profile = models.ForeignKey(Profile, on_delete=models.CASCADE)

    class Meta:
        app_label = 'places'

    def save(self, *args, **kwargs):
        self.slug = slugify(translit(self.title.__str__(), "ru", reversed=True), allow_unicode=True) + str(self.pk)
        super().save(*args, **kwargs)

    def get_absolute_url(self):
        return reverse('place_detail', kwargs={'slug': self.slug})

    def __str__(self):
        return self.title
