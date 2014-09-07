# # -*- coding: utf-8 -*-

from django.http import HttpResponseRedirect, HttpResponse
from django.shortcuts import get_object_or_404, render_to_response
from django.contrib.auth.decorators import login_required
from django.core.context_processors import csrf
from django.core.paginator import Paginator, InvalidPage, EmptyPage
from django.forms import ModelForm
from jastuk.settings import MEDIA_URL
from galerija.models import *

def main(request):
	slike = Image.objects.all()

	form = request.POST
	parameters = {}
	parameters["sort"] = []

	# create dictionary of properties for each image and a dict of search/filter parameters
	for k, v in form.items():
		if k in parameters:
			parameters[k] = v

	try: page = int(request.GET.get("page", '1'))
	except ValueError: page = 1
	# save or restore parameters from session
	if page != 1 and "parameters" in request.session:
		parameters = request.session["parameters"]
	else:
		request.session["parameters"] = parameters

	sort = ''
	if parameters["sort"]:
		sort = parameters["sort"]
	if sort == "ocjena":
		slike = Image.objects.order_by('-ocjena')
	else:
		slike = Image.objects.all()

	paginator = Paginator(slike, 6)
	try:
		slike = paginator.page(page)
	except (InvalidPage, EmptyPage):
		request = paginator.page(paginator.num_pages)

	d = dict(slike=slike, prm=parameters, media_url=MEDIA_URL)
	d.update(csrf(request))
	return render_to_response('galerija/list.html', d)

def image(request, pk):
	slika = Image.objects.get(pk=pk)
	return render_to_response('galerija/image.html', dict(slika=slika, backurl=request.META["HTTP_REFERER"], media_url=MEDIA_URL))

def izracun():
	objects = Slike.objects.all()
	br = len(objects)
	i = 0
	while (i<br):

	return rez