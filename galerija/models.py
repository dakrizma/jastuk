# -*- coding: utf-8 -*-

import os
from django.db import models
from PIL import Image as PImage
from jastuk.settings import MEDIA_ROOT
from django.core.files import File
from os.path import join as pjoin
from tempfile import NamedTemporaryFile
from string import join

# from django.contrib.auth.models import User
# from django.contrib import admin

class Image(models.Model):
	title = models.CharField(max_length=60, blank=True, null=True)
	image = models.FileField(upload_to="images/")
	width = models.IntegerField(blank=True, null=True)
	height = models.IntegerField(blank=True, null=True)
	ocjena = models.FloatField(default=0)
	thumbnail = models.ImageField(upload_to="images/", blank=True, null=True)
	thumbnail2 = models.ImageField(upload_to="images/", blank=True, null=True)

	def save(self, *args, **kwargs):
		super(Image, self).save(*args, **kwargs)
		im = PImage.open(pjoin(MEDIA_ROOT, self.image.name))
		self.width, self.height = im.size

		fn, ext = os.path.splitext(self.image.name)
		im.thumbnail((128,128), PImage.ANTIALIAS)
		thumb_fn = fn + "-thumb2" + ext
		tf2 = NamedTemporaryFile()
		im.save(tf2.name, "JPEG")
		self.thumbnail2.save(thumb_fn, File(open(tf2.name)), save=False)
		tf2.close()

		im.thumbnail((40,40), PImage.ANTIALIAS)
		thumb_fn = fn + "-thumb" + ext
		tf = NamedTemporaryFile()
		im.save(tf.name, "JPEG")
		self.thumbnail.save(thumb_fn, File(open(tf.name)), save=False)
		tf.close()

		super(Image, self).save(*args, **kwargs)

	def thumbnail_(self):
		return """<a href="/static/%s"><img border="0" alt="" src="/static/%s" /></a>""" % ((self.image.name, self.image.name))
	thumbnail_.allow_tags = True

	def __str__(self):
		return self.image.name

ocjene = [(i, i) for i in range(6)]

class Ocjene(models.Model):
	ocjena = models.IntegerField(max_length=1, choices=ocjene)
	komentar = models.CharField(max_length=200, blank=True, null=True)
	image = models.ForeignKey('Image')

	class Meta:
		verbose_name_plural = 'ocjene'