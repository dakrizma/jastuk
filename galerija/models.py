# -*- coding: utf-8 -*-

import os
from django.db import models
from PIL import Image as PImage
from jastuk.settings import MEDIA_ROOT
from django.core.files import File
from os.path import join as pjoin
from tempfile import NamedTemporaryFile
from string import join

class Slika(models.Model):
	name = models.CharField(max_length=60, blank=True, null=True)
	image = models.FileField(upload_to="images/")
	width = models.IntegerField(blank=True, null=True)
	height = models.IntegerField(blank=True, null=True)
	ocjena = models.DecimalField(default=0.0, max_digits=5, decimal_places=2)
	thumbnail = models.ImageField(upload_to="images/", blank=True, null=True)

	def save(self, *args, **kwargs):
		super(Slika, self).save(*args, **kwargs)
		im = PImage.open(pjoin(MEDIA_ROOT, self.image.name))
		self.width, self.height = im.size

		fn, ext = os.path.splitext(self.image.name)
		im.thumbnail((120,120), PImage.ANTIALIAS)
		thumb_fn = fn + "-thumb" + ext
		tf = NamedTemporaryFile()
		im.save(tf.name, "JPEG")
		self.thumbnail.save(thumb_fn, File(open(tf.name)), save=False)
		tf.close()

		super(Slika, self).save(*args, **kwargs)

	def __str__(self):
		return self.image.name

ocjene = [(i, i) for i in range(6)]

class Ocjene(models.Model):
	ocjena = models.IntegerField(max_length=1, choices=ocjene)
	komentar = models.CharField(max_length=200, blank=True, null=True)
	slika = models.ForeignKey(Slika)

	class Meta:
		verbose_name_plural = 'ocjene'