# # -*- coding: utf-8 -*-

from django.http import HttpResponseRedirect, HttpResponse
from django.shortcuts import get_object_or_404, render_to_response
from django.contrib.auth.decorators import login_required
from django.core.context_processors import csrf
from django.core.paginator import Paginator, InvalidPage, EmptyPage
from django.forms import ModelForm
from jastuk.settings import MEDIA_URL
from galerija.models import *
from galerija.forms import *

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
	prim = Image.objects.get(pk=pk)
	slika = Image.objects.all()[prim]
	ocjena = Ocjene.objects.all()

	if request.method == 'POST':
		form = OcjeneForm(request.POST)
		if form.is_valid():
			komentar = form.cleaned_data['komentar']
			ocjena2 = form.cleaned_data['ocjena']
			form.save()
			izracun(ocjena, slika)
			return render_to_response('galerija/image.html', dict(slika=prim, backurl=request.META["HTTP_REFERER"], media_url=MEDIA_URL))

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
	return render_to_response('galerija/image.html', dict(slika=prim, backurl=request.META["HTTP_REFERER"], media_url=MEDIA_URL))



def izracun(ocjena, slika):
	br = len(ocjena)
	brojac = suma = i = 0
	while (i < br):
		if (ocjena[i].image == slika.image):
			if ocjena[i].ocjena != 0:
				brojac += 1
			suma = suma + ocjena[i].ocjena
		i += 1
	if suma != 0:
		slika.ocjena = suma / brojac
