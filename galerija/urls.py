# -*- coding: utf-8 -*-

from django.conf.urls import patterns, include, url

urlpatterns = patterns('',
	# url(r'^izracun/$', 'tarife.views.izracun', name='izracun'),
	# url(r'^brisanje/$', 'tarife.views.brisanje', name='brisanje'),
	url(r'^$', 'galerija.views.main', name='main'),
)