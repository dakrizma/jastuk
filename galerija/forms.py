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
		exclude = ('slika',)

class SlikaForm(ModelForm):
	class Meta:
		model = Slika
		field = ('image', 'name')
		exclude = ('width', 'height', 'ocjena', 'thumbnail')

izbor = (
	('ocjena', 'ocjena'),
	('unos', 'unos'),
	)

class SortForm(forms.Form):
	sort = forms.ChoiceField(choices=izbor)

class ResizeForm(forms.Form):
	visina = forms.IntegerField(label=u'Visina', min_value=1)
	sirina = forms.IntegerField(label=u'Širina', min_value=1)
