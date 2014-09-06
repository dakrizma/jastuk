# -*- coding: utf-8 -*-

from django.contrib import admin
from galerija.models import *

class ImageAdmin(admin.ModelAdmin):
	list_display = ('title', 'image', 'ocjena', 'thumbnail', 'thumbnail2', 'width', 'height')

class KomentarAdmin(admin.ModelAdmin):
	list_display = ('komentar', 'image')
	list_filter = ('image',)

class BodoviAdmin(admin.ModelAdmin):
	list_display = ('bodovi', 'image')
	list_filter = ('image',)

admin.site.register(Image, ImageAdmin)
admin.site.register(Komentar, KomentarAdmin)
admin.site.register(Bodovi, BodoviAdmin)