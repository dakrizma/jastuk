# -*- coding: utf-8 -*-

from django.contrib import admin
from galerija.models import *

class SlikaAdmin(admin.ModelAdmin):
	list_display = ('name', 'image', 'ocjena', 'thumbnail', 'width', 'height')

class OcjeneAdmin(admin.ModelAdmin):
	list_display = ('komentar', 'ocjena', 'slika')
	list_filter = ('slika',)

admin.site.register(Slika, SlikaAdmin)
admin.site.register(Ocjene, OcjeneAdmin)