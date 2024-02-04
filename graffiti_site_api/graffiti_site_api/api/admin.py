from django.contrib import admin
from .models import ActivationToken, Graffiti, Photo


admin.site.register(ActivationToken)
admin.site.register(Graffiti)
admin.site.register(Photo)
