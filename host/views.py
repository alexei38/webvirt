from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.http import HttpResponseRedirect
from host.models import Host
from host.forms import HostAddTcpForm, HostAddSshForm

@login_required
def index(request):
    #messages.success(request, "Skadoosh! You've updated your profile!")
    #messages.info(request, 'Yo! There are new comments on your photo!')
    #messages.error(request, 'Doh! Something went wrong.')
    #messages.warning(request, 'Uh-oh. Your account expires in 3 days.')
    form = None
    hosts = None
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
                return HttpResponseRedirect(request.get_full_path())
        else:
            messages.error(request, 'Not supported connection type')
    else:
    	hosts = Host.objects.filter()

    return render(request, 'host/host_list.html', {'hosts': hosts, 'form': form})

@login_required
def show(request, id):
    host = Host.objects.get(id=id)
    return render(request, 'host/host_overview.html', {'host': host})

@login_required
def update(request):
    return render(request, 'host/host_overview.html')