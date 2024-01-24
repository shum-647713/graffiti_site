from django.db import models
import os, hashlib


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
