# -*- coding: utf-8 -*-

import os
from django.db import models
from PIL import Image, ImageOps
from jastuk.settings import MEDIA_ROOT
from django.core.files import File
from os.path import join
from tempfile import NamedTemporaryFile
from cStringIO import StringIO
from django.core.files.base import ContentFile

class Slika(models.Model):
	name = models.TextField(max_length=300, blank=True, null=True)
	image = models.FileField(upload_to="images/")
	width = models.IntegerField(blank=True, null=True)
	height = models.IntegerField(blank=True, null=True)
	ocjena = models.DecimalField(default=0.0, max_digits=5, decimal_places=2)
	thumbnail = models.ImageField(upload_to="images/", blank=True, null=True)

	def save(self, *args, **kwargs):
		super(Slika, self).save(*args, **kwargs)
		im = Image.open(join(MEDIA_ROOT, self.image.name))
		self.width, self.height = im.size

		fn, ext = os.path.splitext(self.image.name)
		thumb_fn = fn + "-thumb" + ext
		if im.mode not in ('L', 'RGB'):
			im = im.convert('RGB')
		img_type = im.format
		if img_type == 'PNG':
			DJANGO_TYPE = 'image/png'
			extension = 'png'
		elif img_type == 'GIF':
			DJANGO_TYPE = 'image/gif'
			extension = 'gif'
		else:
			DJANGO_TYPE = 'image/jpeg'
			extension = 'jpeg'
		if self.ocjena == 0:
			im = ImageOps.fit(im, (320,180), Image.ANTIALIAS)
			temp_thumb = StringIO()
			im.save(temp_thumb, extension)
			temp_thumb.seek(0)
	
			self.thumbnail.save(thumb_fn, ContentFile(temp_thumb.read()), save=False)
			temp_thumb.close()

		super(Slika, self).save(*args, **kwargs)

	def __str__(self):
		return self.image.name

	class Meta:
		verbose_name_plural = 'slike'

ocjene = [(i, i) for i in range(6)]

class Ocjene(models.Model):
	ocjena = models.IntegerField(max_length=1, choices=ocjene)
	komentar = models.TextField(max_length=300, blank=True, null=True)
	slika = models.ForeignKey(Slika)

	class Meta:
		verbose_name_plural = 'ocjene'