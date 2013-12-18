from django.db import models

# Create your models here.

class Host(models.Model):
    name = models.CharField(max_length=50, unique=True)
    ip = models.CharField(max_length=50)
    login = models.CharField(max_length=50)
    password = models.CharField(max_length=50, blank=True, null=True)
    type = models.CharField(max_length=3)
    port = models.IntegerField(blank=True, null=True, default='22')
    def __unicode__(self):
        return u'%s' % self.name

class Pool(models.Model):
    name = models.CharField(max_length=50, unique=True)
    source_device = models.CharField(max_length=50)
    target_device = models.CharField(max_length=50)
    format_type = models.CharField(max_length=10)
    host = models.ForeignKey(Host)
    def __unicode__(self):
        return u'%s' % self.name

class Image(models.Model):
    name = models.CharField(max_length=50)
    path = models.CharField(max_length=50)
    pool = models.ForeignKey(Pool)
    def __unicode__(self):
        return u'%s' % self.name

class Template(models.Model):
    name = models.CharField(max_length=50)
    path = models.CharField(max_length=50)
    def __unicode__(self):
        return u'%s' % self.name

class Machine(models.Model):
    name = models.CharField(max_length=40, unique=True)
    ip = models.CharField(max_length=40)
    arch = models.CharField(max_length=20)
    vcpu = models.IntegerField(max_length=20)
    vmem = models.IntegerField(max_length=20)
    virtio = models.BooleanField(max_length=20)
    ostype = models.CharField(max_length=20)
    network = models.CharField(max_length=50)
    virt_type = models.CharField(max_length=10)
    image = models.ForeignKey(Image)
    host = models.ForeignKey(Host)
    description = models.CharField(max_length=255)
    created_on = models.DateField(auto_now_add=True)
    updated_on = models.DateField(auto_now_add=True)
    def __unicode__(self):
        return u'%s' % self.name
    class Meta:
        permissions = ( 
                ( "control_machine", "Can control machine" ),
            )

