from django.db import models


class Graffiti(models.Model):
    name = models.CharField(max_length=200)
    owner = models.ForeignKey('auth.User', related_name='graffiti', on_delete=models.CASCADE)

class Photo(models.Model):
    image = models.ImageField(upload_to='images/')
    graffiti = models.ForeignKey(Graffiti, related_name='photos', on_delete=models.CASCADE)
