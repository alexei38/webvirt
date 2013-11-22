from django.conf.urls import patterns, include, url
from django.conf import settings

from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    # Examples:
    url(r'^$', 'machine.views.index', name='machines'),
    # url(r'^blog/', include('blog.urls')),
    url(r'^login/$', 'django.contrib.auth.views.login', {'template_name': 'login.html'}, name='login'),
    url(r'^logout/$', 'django.contrib.auth.views.logout', {'next_page': '/login/'}, name='logout'),
    url(r'^admin/', include(admin.site.urls)),
    url(r'^hosts/$', 'host.views.index', name='hosts'),
    url(r'^hosts/(\d+)/$', 'host.views.edit', name='host_edit'),
    url(r'^hosts/(\d+)/get_memory/$', 'host.views.ajax_memory', name='host_get_memory'),
    url(r'^hosts/(\d+)/delete/$', 'host.views.delete', name='host_delete'),
    url(r'^machines/$', 'machine.views.index', name='machines'),
    url(r'^pools/$', 'machine.views.index', name='pools'),
    url(r'^dashboard/$', 'machine.views.index', name='dashboard'),
    url(r'^account/(\d+)/$', 'account.views.show', name='account'),
)

