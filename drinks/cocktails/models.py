import random
import string
import os

from PIL import Image
from io import BytesIO
from django.db import models
from django.core.files.uploadedfile import InMemoryUploadedFile
from django.contrib.auth.models import User
from django.core.validators import MinValueValidator, MaxValueValidator


def random_string(length):
    letters = string.ascii_lowercase
    return ''.join(random.choice(letters) for _ in range(length))


class Ingredient(models.Model):
    unit_type = (('ml', 'mililitr'), ('szt', 'sztuk'), ('g', 'gram'))
    name = models.CharField(max_length=220)
    amount = models.PositiveIntegerField(default=1, validators=[MinValueValidator(1), MaxValueValidator(300)],
                                         blank=True)
    unit = models.CharField(default='ml', choices=unit_type, max_length=3)

    def __str__(self):
        return f'{self.name}  |  {self.amount} {self.unit}'


class Drink(models.Model):
    name = models.CharField(max_length=100, blank=False)
    ingredients = models.ManyToManyField(Ingredient)
    owner = models.ForeignKey(User, on_delete=models.CASCADE)
    description = models.TextField(blank=True)
    creation_date = models.DateTimeField(auto_now_add=True)
    image = models.ImageField(upload_to='images/', blank=True)
    thumbnail = models.ImageField(upload_to='thumbnails/', blank=True, null=True)
    drink_publish = models.BooleanField(default=True)
    pin_to_main_page = models.BooleanField(default=False)
    likes = models.PositiveIntegerField(default=0)

    def __str__(self):
        return f'{self.name} | {self.creation_date} | {self.description}'

    @property
    def is_liked_by_user(self):
        return self.like_set.filter(user=self.owner).exists()

    def save(self, *args, **kwargs):

        self.thumbnail = self.create_thumbnail()
        super(Drink, self).save(*args, **kwargs)

    def update_like_count(self):
        self.likes = Like.objects.filter(drink=self).count()
        self.save()

    def create_thumbnail(self):
        image = Image.open(self.image)
        max_size = (300, 200)

        if image.width > max_size[0] or image.height > max_size[1]:
            image.thumbnail(max_size, Image.LANCZOS)

        thumbnail_io = BytesIO()
        image.save(thumbnail_io, 'JPEG', quality=85)

        thumbnail_filename = random_string(10) + '.jpg'

        thumbnail_path = thumbnail_filename
        self.thumbnail.save(thumbnail_path,
                            InMemoryUploadedFile(thumbnail_io, None, thumbnail_path, 'image/jpeg',
                                                 thumbnail_io.tell(), None), save=False)

        return self.thumbnail


class Like(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    drink = models.ForeignKey(Drink, on_delete=models.CASCADE)
    timestamp = models.DateTimeField(auto_now_add=True)
