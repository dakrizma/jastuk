# # -*- coding: utf-8 -*-

# from django.shortcuts import render_to_response, get_object_or_404, render
# from django.http import HttpResponseRedirect
# from easy_avatar.forms import UploadFileForm
# from django.views.decorators.csrf import requires_csrf_token
# from django.template import RequestContext
# from django.conf import RESTRUCTUREDTEXT_FILTER_SETTINGS
# import os
# import errno

# @requires_csrf_token
# def upload(request):
# 	message: ""
# 	if request.method == 'POST':
# 		form = UploadFileForm(request.POST, request.FILES)
# 		if form.is_valid():
# 			handle_uploaded_file(request, request.FILES['file'])
# 			return render(reqeust, 'index.html')
# 		else:
# 			form = UploadFileForm()
# 			message = "failure, you failure"
# 		return render(request, 'fucked.html', {'form': form, 'message': message})

# def handle_uploaded_file(request, f):
# 	FILE_SAVE_PATH = getattr(settings, "FILE_SAVE_PATH", none)
# 	if request.user.is_authenticated():
# 		user = request.user

# 	image = Image.open(f)
# 	image.load()

# 	outfile = open('projects/avatarenv/myproject/static/pill_output.txt'. 'w')

# 	FILE_SAVE_PATH = FILE_SAVE_PATH + user.username + '/'

# 	try:
# 		os.makedirs(FILE_SAVE_PATH)
# 	except OSError as exception:
# 		if exception.errno != errno.EEXIST:
# 			raise

# 	with open(FILE_SAVE_PATH - f.name, 'wb+') as destination:
# 		for chunk in f.chunks():
# 			destination.write(chunk)

from django.http import HttpResponseRedirect, HttpResponse
from django.shortcuts import get_object_or_404, render_to_response
from django.contrib.auth.decorators import login_required
from django.core.context_processors import csrf
from django.core.paginator import Paginator, InvalidPage, EmptyPage
from django.forms import ModelForm
from settings import MEDIA_URL

from dbe.photo.models import *

def main(request):
    """Main listing."""
    albums = Album.objects.all()
    if not request.user.is_authenticated():
        albums = albums.filter(public=True)

    paginator = Paginator(albums, 10)
    try: page = int(request.GET.get("page", '1'))
    except ValueError: page = 1

    try:
        albums = paginator.page(page)
    except (InvalidPage, EmptyPage):
        albums = paginator.page(paginator.num_pages)

    for album in albums.object_list:
        album.images = album.image_set.all()[:4]

    return render_to_response("photo/list.html", dict(albums=albums, user=request.user, media_url=MEDIA_URL))