# -*- coding: utf-8 -*-

from django.conf.urls import patterns, url

urlpatterns = patterns('',
	url(r'^$', 'galerija.views.main', name='main'),
	url(r'^image/(\d+)/$', 'galerija.views.image', name='image'),
	url(r'^ajax/(\d+)/$', 'galerija.views.ajax', name='ajax'),
)