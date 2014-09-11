# # -*- coding: utf-8 -*-

from django.http import HttpResponseRedirect, HttpResponse
from django.shortcuts import get_object_or_404, render_to_response, render
from django.contrib.auth.decorators import login_required
from django.core.context_processors import csrf
from django.core.paginator import Paginator, InvalidPage, EmptyPage
from django.forms import ModelForm
from jastuk.settings import MEDIA_URL
from galerija.models import *
from galerija.forms import *
from django.core.urlresolvers import reverse

def main(request):
	slike = Image.objects.all()
	parameters = []
	try: page = int(request.GET.get("page", '1'))
	except ValueError: page = 1
	if request.method == 'POST':
		if request.POST['action'] == 'Upload':
			uploadform = ImageForm(request.POST, request.FILES)
			if uploadform.is_valid():
				uploadform.save()
				return HttpResponseRedirect(reverse('main'))
		elif request.POST['action'] == 'Apply':
			applyform = SortForm(request.POST)
			if applyform.is_valid():
				parameters = applyform.cleaned_data['sort']
	if page != 1 and "parameters" in request.session:
		parameters = request.session["parameters"]
	else:
		request.session["parameters"] = parameters
	if parameters == "ocjena":
		slike = Image.objects.order_by('-ocjena')
	else:
		slike = Image.objects.all()
	paginator = Paginator(slike, 6)
	try:
		slike = paginator.page(page)
	except (InvalidPage, EmptyPage):
		request = paginator.page(paginator.num_pages)
	uploadform = ImageForm()
	applyform = SortForm()
	return render(request, 'galerija/list.html', {'slike': slike, 'media_url': MEDIA_URL, 'uploadform': ImageForm, 'applyform': applyform})


def image(request, pk):
	slika = Image.objects.get(pk=pk)
	ocjene = Ocjene.objects.filter(image=slika).order_by('-id')
	zadnje = ocjene[:5]
	if request.method == 'POST':
		form = OcjeneForm(request.POST)
		if form.is_valid():
			obj = form.save(commit=False)
			obj.image = slika
			obj.save()
			ocjene = Ocjene.objects.filter(image=slika).order_by('-id')
			zadnje = ocjene[:5]
			izracun(ocjene, slika)
			form = OcjeneForm()
			return render(request, 'galerija/image.html', {'slika': slika, 'zadnje': zadnje, 'ocjene': ocjene, 'backurl': request.META["HTTP_REFERER"], 'media_url': MEDIA_URL, 'form': form})
	form = OcjeneForm()
	return render(request, 'galerija/image.html', {'slika': slika, 'zadnje': zadnje, 'ocjene': ocjene, 'backurl': request.META["HTTP_REFERER"], 'media_url': MEDIA_URL, 'form': form})

def izracun(ocjena, slika):
	br = len(ocjena)
	brojac = suma = 0.0
	i = 0
	while (i < br):
		if (ocjena[i].image == slika):
			if ocjena[i].ocjena != 0:
				brojac += 1
			suma = suma + ocjena[i].ocjena
		i += 1
	if suma != 0:
		slika.ocjena = suma / brojac
		slika.save()