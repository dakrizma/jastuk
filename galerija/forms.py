# -*- coding: utf-8 -*-

from django import forms
from django.forms import ModelForm
from galerija.models import Ocjene
from django.utils.translation import ugettext_lazy as _


class OcjeneForm(ModelForm):
    class Meta:
        model = Ocjene
        labels = {
			'komentar': _(u'Komentar'),
			'ocjena': _('Ocjena slike'),
			}