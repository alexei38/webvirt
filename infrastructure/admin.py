from django.contrib import admin

# Register your models here.

from django.contrib import admin
from infrastructure.models import *
from guardian.admin import GuardedModelAdmin
# Register your models here.
class MachineAdmin(GuardedModelAdmin):
    ordering = ('-created_on',)
    date_hierarchy = 'created_on'

class HostAdmin(GuardedModelAdmin):
    pass

class PoolAdmin(GuardedModelAdmin):
    pass

class ImageAdmin(GuardedModelAdmin):
    pass

admin.site.register(Machine, MachineAdmin)
admin.site.register(Host, HostAdmin)
admin.site.register(Pool, PoolAdmin)
admin.site.register(Image, ImageAdmin)
