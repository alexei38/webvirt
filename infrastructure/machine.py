from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.http import HttpResponse, HttpResponseRedirect, Http404
from infrastructure.models import Machine, Host, Image
from infrastructure.forms import MachineAddForm, MachineEditForm
from django.core.urlresolvers import reverse
from webvirt.connserver import ConnServer
from django.utils import simplejson
from guardian.shortcuts import get_objects_for_user, get_perms

@login_required
def index(request):
    machines = []
    perms = []
    try:
        machines = get_objects_for_user(request.user, 'control_machine', klass=Machine)
    except:
        raise Http404
    return render(request, 'machine/machines.html', {'current_url': ['machines'], 'machines': machines })

@login_required
def add(request):
    form = None
    hosts = get_all_host(request)
    images = get_all_image(request)
    if request.method == 'POST':
        form = MachineAddForm(request.POST)
        if form.is_valid():
            data = form.cleaned_data
            new_machine = Machine(name=data['name'],
                                arch=data['arch'],
                                vcpu=data['vcpu'],
                                vmem=data['vmem'],
                                virtio=data['virtio'],
                                ostype=data['ostype'],
                                image=data['image'],
                                host=data['host'],
                                description=data['description']
                                )
            new_machine.save()
            messages.success(request, "VM successful created!")
            return HttpResponseRedirect(reverse('machines_edit', args=[new_machine.id]))
    return render(request, 'machine/machine_add.html', {
                        'current_url': ['machines'],
                        'form': form,
                        'hosts': hosts,
                        'images': images,
                        'title': 'Add Machine'
                        })

@login_required
def edit(request, machine_id):
    hosts = get_all_host(request)
    images = get_all_image(request)
    form = None
    try:
        machine = Machine.objects.get(id=machine_id)
    except Machine.DoesNotExist:
        raise Http404
    if 'control_machine' not in get_perms(request.user, machine):
        raise Http404
    if request.method == 'POST':
        print request.POST
        form = MachineEditForm(request.POST)
        if form.is_valid():
            data = form.cleaned_data
            machine.name=data['name']
            machine.arch=data['arch']
            machine.vmem=data['vmem']
            machine.virtio=data['virtio']
            machine.vcpu=data['vcpu']
            machine.image=data['image']
            machine.host=data['host']
            machine.description=data['description']
            machine.save()
            messages.success(request, "Machine successful updated!")
            return HttpResponseRedirect(reverse('machines_edit', args=[machine.id]))
    return render(request, 'machine/machine_id.html', {
                        'current_url': ['machines'],
                        'machine': machine,
                        'form': form,
                        'hosts': hosts,
                        'images': images,
                        'title': 'Edit Machine'
                        })

def get_all_host(request):
    try:
        hosts = get_objects_for_user(request.user, 'change_host', klass=Host)
    except:
        hosts = []
    return hosts

def get_all_image(request):
    try:
        images = get_objects_for_user(request.user, 'change_image', klass=Image)
    except:
        images = []
    return images
