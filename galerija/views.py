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
	try: page = int(request.GET.get("page", '1'))
	except ValueError: page = 1
	paginator = Paginator(slike, 6)
	try:
		slike = paginator.page(page)
	except (InvalidPage, EmptyPage):
		request = paginator.page(paginator.num_pages)
	parameters = {}
	parameters["sort"] = []
	if request.method == 'POST':
		if request.POST['action'] == 'Upload':
			form = ImageForm(request.POST, request.FILES)
			if form.is_valid():
				form.save()
				return HttpResponseRedirect(reverse('main'))
		elif request.POST['action'] == 'Apply':
			form = request.POST
			# create dictionary of properties for each image and a dict of search/filter parameters
			for k, v in form.items():
				if k in parameters:
					parameters[k] = v
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
	form = ImageForm()
	return render(request,'galerija/list.html',{'slike': slike, 'prm': parameters, 'media_url': MEDIA_URL, 'form': form})


def image(request, pk):
	slika = Image.objects.get(pk=pk)

	if request.method == 'POST':
		form = OcjeneForm(request.POST)
		if form.is_valid():
			komentar = form.cleaned_data['komentar']
			ocjena2 = form.cleaned_data['ocjena']
			obj = form.save(commit=False)
			obj.image = slika
			obj.save()
			ocjena = Ocjene.objects.all()
			rez, suma, brojac = izracun(ocjena, slika)
			slika.ocjena = rez
			return render(request, 'galerija/image.html', {'slika': slika, 'backurl': request.META["HTTP_REFERER"], 'media_url': MEDIA_URL})

			# k = 0
			# objects = Racun.objects.all()
			# br = len(objects)
			# while (k < br):
			# 	if (mjesec == objects[k].mjesec) and (godina == objects[k].godina) and (request.user == objects[k].korisnik):
			# 		greska = 'Unijeli ste podatke za taj mjesec. Za brisanje računa kliknite na \'brisanje računa\' ili nastavite sa unosom novog računa'
			# 		form = RacunForm()
			# 		return render(request, 'tarife/index.html', {'form': form, 'greska': greska})
			# 	k += 1
			# racun = form.save(commit=False)
			# racun.korisnik = request.user
			# racun.save()
			# korisnik = request.user
			# rez, rez_mjesec = izlaz(korisnik)
			# return render(request, 'tarife/izracun.html', {'rez': rez, 'rez_mjesec': rez_mjesec})
	else:
		form = OcjeneForm()
	return render(request, 'galerija/image.html', {'slika': slika, 'backurl': request.META["HTTP_REFERER"], 'media_url': MEDIA_URL, 'form': form})



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
	return (slika.ocjena, suma, brojac)
