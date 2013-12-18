from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.http import HttpResponse, HttpResponseRedirect, Http404
from infrastructure.models import Pool
from django.core.urlresolvers import reverse
from webvirt.connserver import ConnServer
from django.utils import simplejson

@login_required
def index(request):
    pools = []
    form = None
    return render(request, 'pool/pools.html', {'current_url': ['pools'], 'pools': pools, 'form': form})

def add_pool(request):
    pools = []
    form = None
    return render(request, 'pool/pools.html', {'current_url': ['pools'], 'pools': pools, 'form': form})

def images(request, pool_id):
    images = []
    form = None
    return render(request, 'pool/images.html', {'current_url': ['pools'], 'pools': images, 'form': form})

def add_images(request, pool_id):
    images = []
    form = None
    return render(request, 'pool/images.html', {'current_url': ['pools'], 'pools': images, 'form': form})
