# -*- coding: utf-8 -*-

from django.contrib import admin
from galerija.models import *

class ImageAdmin(admin.ModelAdmin):
	list_display = ('title', 'image', 'ocjena', 'thumbnail', 'thumbnail2', 'width', 'height')

class OcjeneAdmin(admin.ModelAdmin):
	list_display = ('komentar', 'ocjena', 'image')
	list_filter = ('image',)

admin.site.register(Image, ImageAdmin)
admin.site.register(Ocjene, OcjeneAdmin)