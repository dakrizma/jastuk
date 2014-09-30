# # -*- coding: utf-8 -*-

from django.http import HttpResponseRedirect, HttpResponse, HttpResponseBadRequest
from django.shortcuts import render
from django.core.paginator import Paginator, InvalidPage, EmptyPage
from jastuk.settings import STATIC_URL, MEDIA_ROOT
from galerija.models import *
from galerija.forms import *
from django.core.urlresolvers import reverse
from PIL import Image
from os.path import join
import json



def main(request):
	slike = Slika.objects.all()
	parameters = []
	try: page = int(request.GET.get("page", '1'))
	except ValueError: page = 1
	if request.method == 'POST':
		if request.POST['action'] == 'Upload':
			uploadform = SlikaForm(request.POST, request.FILES)
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
		slike = Slika.objects.order_by('-ocjena')
	else:
		slike = Slika.objects.all()
	paginator = Paginator(slike, 6)
	try:
		slike = paginator.page(page)
	except (InvalidPage, EmptyPage):
		request = paginator.page(paginator.num_pages)
	uploadform = SlikaForm()
	applyform = SortForm()
	return render(request, 'galerija/list.html', {'slike': slike, 'media_url': STATIC_URL, 'uploadform': uploadform, 'applyform': applyform})


def image(request, pk):
	slika = Slika.objects.get(pk=pk)
	ocjene = Ocjene.objects.filter(slika=slika).order_by('-id')
	zadnje = ocjene[:5]
	# if request.method == 'POST':
	# 	if request.POST['action'] == 'Izracunaj':
	# 		ocjeneform = OcjeneForm(request.POST)
	# 		if ocjeneform.is_valid():
	# 			obj = ocjeneform.save(commit=False)
	# 			obj.slika = slika
	# 			obj.save()
	# 			ocjene = Ocjene.objects.filter(slika=slika).order_by('-id')
	# 			zadnje = ocjene[:5]
	# 			izracun(ocjene, slika)
	# 			data = {
	# 				'komentar': [ocjena.komentar for ocjena in ocjene],
	# 				'ocjene': [zadnji.ocjena for zadnji in zadnje],
	# 				'prosjek': slika.ocjena,
	# 				}
	# 			return HttpResponse(json.dumps(data), content_type="application/json")
	# 	if request.POST['action'] == 'Resize':
	# 		resizeform = ResizeForm(request.POST)
	# 		if resizeform.is_valid():
	# 			sirina = int(resizeform.cleaned_data['sirina'])
	# 			visina = int(resizeform.cleaned_data['visina'])
	# 			im = Image.open(join(MEDIA_ROOT, slika.image.name))
	# 			im = ImageOps.fit(im, (sirina,visina), Image.ANTIALIAS)
	# 			im.show()
	# 			if im.mode not in ('L', 'RGB'):
	# 				im = im.convert('RGB')
	# 			im.save(join(MEDIA_ROOT, "images/slikica.jpg"))
	# 			resizeform = ResizeForm()
	# 			ocjeneform = OcjeneForm()
	# 			return render(request, 'galerija/image.html', {'slika': slika, 'zadnje': zadnje, 'ocjene': ocjene, 'media_url': STATIC_URL, 'resizeform': resizeform, 'ocjeneform': ocjeneform})
	ocjeneform = OcjeneForm()
	resizeform = ResizeForm()
	return render(request, 'galerija/image.html', {'slika': slika, 'zadnje': zadnje, 'ocjene': ocjene, 'media_url': STATIC_URL, 'ocjeneform': ocjeneform, 'resizeform': resizeform})

def izracun(ocjena, slika):
	br = len(ocjena)
	brojac = suma = 0.0
	i = 0
	while (i < br):
		if (ocjena[i].slika == slika):
			if ocjena[i].ocjena != 0:
				brojac += 1
			suma = suma + ocjena[i].ocjena
		i += 1
	if suma != 0:
		slika.ocjena = suma / brojac
		slika.save(update_fields=['ocjena'])



def ajax(request, pk):
	if request.method == 'POST':
		slika = Slika.objects.get(pk=pk)
		ocjeneform = OcjeneForm(request.POST)
		if ocjeneform.is_valid():
			obj = ocjeneform.save(commit=False)
			obj.slika = slika
			obj.save()
			ocjene = Ocjene.objects.filter(slika=slika).order_by('-id')
			zadnje = ocjene[:5]
			izracun(ocjene, slika)
			data = {
				'komentar': [ocjena.komentar for ocjena in ocjene],
				'ocjene': [zadnji.ocjena for zadnji in zadnje],
				'prosjek': slika.ocjena,
				}
			if request.is_ajax():
				return HttpResponse(json.dumps(data), content_type="application/json")
			else:
				return HttpResponse('Greska!')
		else:
			if request.is_ajax():
				errors_dict = {}
				if ocjeneform.errors:
					for error in ocjeneform.errors:
						e = ocjeneform.errors[error]
						errors_dict[error] = unicode(e)
				return HttpResponseBadRequest(json.dumps(errors_dict))
			else:
				return HttpResponse('Greska2!')
	else:
		ocjeneform = OcjeneForm()
	return render(request, 'galerija/image.html', {'form': ocjeneform})

def ajax2(request, pk):
	if request.method == 'POST':
		slika = Slika.objects.get(pk=pk)
		resizeform = ResizeForm(request.POST)
		if resizeform.is_valid():
			sirina = int(resizeform.cleaned_data['sirina'])
			visina = int(resizeform.cleaned_data['visina'])
			im = Image.open(join(MEDIA_ROOT, slika.image.name))
			im = ImageOps.fit(im, (sirina,visina), Image.ANTIALIAS)
			# im.show()
			if im.mode not in ('L', 'RGB'):
				im = im.convert('RGB')
			im.save(join(MEDIA_ROOT, "images/slikica.jpg"))

			if request.is_ajax():
				return HttpResponse("images/slikica.jpg")
			else:
				return HttpResponse('Greska!')
		else:
			if request.is_ajax():
				errors_dict = {}
				if resizeform.errors:
					for error in resizeform.errors:
						e = resizeform.errors[error]
						errors_dict[error] = unicode(e)
				return HttpResponseBadRequest(json.dumps(errors_dict))
			else:
				return HttpResponse('Greska2!')
	else:
		resizeform = ResizeForm()
	return render(request, 'galerija/image.html', {'form': resizeform})