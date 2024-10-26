from django.contrib import admin

from .models import Pereval, PerevalImage, PerevalLevel, Coordinates

admin.site.register(Pereval)
admin.site.register(Coordinates)
admin.site.register(PerevalImage)
admin.site.register(PerevalLevel)
