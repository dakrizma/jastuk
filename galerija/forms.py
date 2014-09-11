# -*- coding: utf-8 -*-

from django import forms
from django.forms import ModelForm
from galerija.models import *
from django.utils.translation import ugettext_lazy as _


class OcjeneForm(ModelForm):
	class Meta:
		model = Ocjene
		labels = {
			'komentar': _(u'Komentar'),
			'ocjena': _('Ocjena slike'),
			}
		exclude = ('image',)

class ImageForm(ModelForm):
	class Meta:
		model = Image
		field = ('image', 'name')
		exclude = ('width', 'height', 'ocjena', 'thumbnail', 'thumbnail2')

izbor = (
	('ocjena', 'ocjena'),
	('unos', 'unos'),
	)

class SortForm(forms.Form):
	sort = forms.ChoiceField(choices=izbor)