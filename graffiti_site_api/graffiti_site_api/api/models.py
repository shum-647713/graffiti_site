from django.db import models
from django.utils import timezone
from datetime import timedelta
import os, hashlib


class TokenManager(models.Manager):
    def __init__(self, token_lifespan, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.token_lifespan = token_lifespan
    def get_queryset(self):
        queryset = super().get_queryset()
        expiration_border = timezone.now() - self.token_lifespan
        return queryset.filter(date_created__gt = expiration_border)
    def delete_expired(self, delete_users=True):
        queryset = super().get_queryset()
        expiration_border = timezone.now() - self.token_lifespan
        expired = queryset.filter(date_created__lt = expiration_border)
        if delete_users:
            for token in expired:
                token.user.delete()
        else:
            expired.delete()

class ActivationToken(models.Model):
    value = models.CharField(max_length=64)
    user = models.ForeignKey('auth.User', on_delete=models.CASCADE)
    date_created = models.DateTimeField(auto_now_add=True)
    objects = TokenManager(token_lifespan=timedelta(days=2))
    def __str__(self):
        return self.user.username

class Graffiti(models.Model):
    name = models.CharField(max_length=200)
    owner = models.ForeignKey('auth.User', related_name='graffiti', on_delete=models.CASCADE)
    def __str__(self):
        return self.name

def hash_image_upload(instance, filename):
    fname, ext = os.path.splitext(filename)
    ctx = hashlib.sha256()
    if instance.image.multiple_chunks():
        for data in instance.image.chunks(4096):
            ctx.update(data)
    else:
        ctx.update(instance.image.read())
    return os.path.join('images/', ctx.hexdigest() + ext)

class Photo(models.Model):
    image = models.ImageField(upload_to=hash_image_upload, max_length=255)
    graffiti = models.ForeignKey(Graffiti, related_name='photos', on_delete=models.CASCADE)
    def __str__(self):
        return self.image.name
