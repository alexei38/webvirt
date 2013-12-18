from django.conf.urls import patterns, include, url
from django.conf import settings

from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    # Examples:
    url(r'^$', 'infrastructure.machine.index', name='machines'),
    url(r'^login/$', 'django.contrib.auth.views.login', {'template_name': 'login.html'}, name='login'),
    url(r'^logout/$', 'django.contrib.auth.views.logout', {'next_page': '/login/'}, name='logout'),
    url(r'^admin/', include(admin.site.urls)),

    url(r'^hosts/$', 'infrastructure.host.index', name='hosts'),
    url(r'^hosts/(\d+)/$', 'infrastructure.host.edit', name='host_edit'),
    url(r'^hosts/(\d+)/get_memory/$', 'infrastructure.host.ajax_memory', name='host_get_memory'),
    url(r'^hosts/(\d+)/delete/$', 'infrastructure.host.delete', name='host_delete'),

    url(r'^machines/$', 'infrastructure.machine.index', name='machines'),
    url(r'^machines/add/$', 'infrastructure.machine.add', name='machines_add'),
    url(r'^machines/(\d+)/$', 'infrastructure.machine.edit', name='machines_edit'),

    url(r'^pools/$', 'infrastructure.pools.index', name='pools'),
    url(r'^pools/add/$', 'infrastructure.pools.add_pool', name='pools_add'),
    url(r'^pools/(\d+)/$', 'infrastructure.pools.images', name='images'),
    url(r'^pools/(\d+)/add/$', 'infrastructure.pools.add_images', name='images_add'),
)