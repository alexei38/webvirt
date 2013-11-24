from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.http import HttpResponse, HttpResponseRedirect, Http404
from host.models import Host
from host.forms import HostAddTcpForm, HostAddSshForm, HostEditTcpForm, HostEditSshForm
from django.core.urlresolvers import reverse
from webvirt.connserver import ConnServer
from django.utils import simplejson

@login_required
def index(request):
    #messages.success(request, "Skadoosh! You've updated your profile!")
    #messages.info(request, 'Yo! There are new comments on your photo!')
    #messages.error(request, 'Doh! Something went wrong.')
    #messages.warning(request, 'Uh-oh. Your account expires in 3 days.')
    form = None
    hosts = []
    host_list = []
    if request.method == 'POST':
        if request.POST['connection_type'] == 'tcp':
            form = HostAddTcpForm(request.POST)
            if form.is_valid():
                data = form.cleaned_data
                new_host = Host(name=data['name'],
                                ip=data['ip'],
                                type='tcp',
                                login=data['login'],
                                password=data['password1']
                                )
                new_host.save()
                messages.success(request, "Host successful created!")
                return HttpResponseRedirect(request.get_full_path())
        elif request.POST['connection_type'] == 'ssh':
            form = HostAddSshForm(request.POST)
            if form.is_valid():
                data = form.cleaned_data
                new_host = Host(name=data['name'],
                                ip=data['ip'],
                                type='ssh',
                                login=data['login'],
                                port=data['port']
                                )
                new_host.save()
                messages.success(request, "Host successful created!")
                return HttpResponseRedirect(request.get_full_path())
        else:
            messages.error(request, 'Not supported connection type')
    else:
        hosts = Host.objects.filter()
        for host in hosts:
            try:
                conn = ConnServer(host)
                host_list.append([host.id, host.name, conn, [conn.node_get_info()] ])
                conn.close()
            except:
                conn = None
                host_list.append([host.id, host.name, None, None])
    return render(request, 'host/host_list.html', {'current_url': ['hosts'], 'hosts': host_list, 'form': form})

@login_required
def edit(request, host_id):
    form = None
    try:
        host = Host.objects.get(id=host_id)
    except Host.DoesNotExist:
        raise Http404
    if request.method == 'POST':
        if request.POST['connection_type'] == 'tcp':
            form = HostEditTcpForm(request.POST)
            if form.is_valid():
                data = form.cleaned_data
                host.name=data['name']
                host.ip=data['ip']
                host.type='tcp'
                host.login=data['login']
                host.password=data['password1']
                host.save()
                messages.success(request, "Host successful updated!")
                return HttpResponseRedirect(request.get_full_path())
        elif request.POST['connection_type'] == 'ssh':
            form = HostEditSshForm(request.POST)
            if form.is_valid():
                data = form.cleaned_data
                host.name=data['name']
                host.ip=data['ip']
                host.type='ssh'
                host.login=data['login']
                host.port=data['port']
                host.save()
                messages.success(request, "Host successful updated!")
                return HttpResponseRedirect(request.get_full_path())
        else:
            messages.error(request, 'Not supported connection type')
    else:
        try:
            conn = ConnServer(host)
            host_info = conn.node_get_info()
            conn.close()
        except:
            conn = None
            host_info = None
    return render(request, 'host/host_overview.html', {'current_url': ['hosts'], 'host': host, 'form': form, 'host_info': host_info})

@login_required
def delete(request, host_id):
    try:
        host = Host.objects.get(id=host_id)
    except Host.DoesNotExist:
        raise Http404
    if request.method == 'POST':
        host.delete()
        messages.success(request, "Host successful removed!")
    return HttpResponseRedirect(reverse('hosts'))

def ajax_memory(request, host_id):
    try:
        host = Host.objects.get(id=host_id)
    except Host.DoesNotExist:
        raise Http404
    try:
        conn = ConnServer(host)
        memory_usage = conn.memory_get_usage()
        conn.close()
    except:
        memory_usage = {"allmem":0, "memusage":0, "percent":0}
    data = simplejson.dumps(memory_usage)
    return HttpResponse(data, mimetype='application/json')