from django import forms
from host.models import Host
from django.db.models import Q
from django.utils.translation import ugettext_lazy as _
import re

class HostAddTcpForm(forms.Form):
    name = forms.CharField(error_messages={'required': _('No hostname has been entered')},
                           max_length=40)
    ip = forms.CharField(error_messages={'required': _('No IP / Domain name has been entered')},
                               max_length=100)
    login = forms.CharField(error_messages={'required': _('No login has been entered')},
                            max_length=20)
    password1 = forms.CharField(error_messages={'required': _('No password has been entered')},
                                max_length=20)
    password2 = forms.CharField(error_messages={'required': _('No password confirm name has been entered')},
                                max_length=20)
    def clean(self):
        password1 = self.cleaned_data.get('password1')
        password2 = self.cleaned_data.get('password2')
        if password1 and password1 != password2:
            raise forms.ValidationError(_('Your password didn\'t match. Please try again.'))
        return self.cleaned_data

    def clean_name(self):
        name = self.cleaned_data['name']
        have_symbol = re.match('[^a-zA-Z0-9._-]+', name)
        if have_symbol:
            raise forms.ValidationError(_('The hostname must not contain any special characters'))
        elif len(name) > 20:
            raise forms.ValidationError(_('The hostname must not exceed 20 characters'))
        try:
            Host.objects.get(name=name)
        except Host.DoesNotExist:
            return name
        else:
            raise forms.ValidationError(_('This hostname is already connected'))

    def clean_ip(self):
        ip = self.cleaned_data['ip']
        have_symbol = re.match('[^a-z0-9.-]+', ip)
        wrong_ip = re.match('^0.|^255.', ip)
        if have_symbol:
            raise forms.ValidationError(_('Hostname must contain only numbers, or the domain name separated by "."'))
        elif wrong_ip:
            raise forms.ValidationError(_('Wrong IP address'))
        try:
            Host.objects.get(ip=ip)
        except Host.DoesNotExist:
            return ip
        else:
            raise forms.ValidationError(_('This IP / Domain is already connected'))

class HostAddSshForm(forms.Form):
    name = forms.CharField(error_messages={'required': _('No hostname has been entered')},
                           max_length=40)
    ip = forms.CharField(error_messages={'required': _('No IP / Domain name has been entered')},
                               max_length=100)
    login = forms.CharField(error_messages={'required': _('No login has been entered')},
                            max_length=20)
    port = forms.IntegerField(error_messages={'required': _('No SSH port has been entered')})

    def clean_name(self):
        name = self.cleaned_data['name']
        have_symbol = re.match('[^a-zA-Z0-9._-]+', name)
        if have_symbol:
            raise forms.ValidationError(_('The host name must not contain any special characters'))
        elif len(name) > 20:
            raise forms.ValidationError(_('The host name must not exceed 20 characters'))
        try:
            Host.objects.get(name=name)
        except Host.DoesNotExist:
            return name
        raise forms.ValidationError(_('This host is already connected'))

    def clean_ip(self):
        ip = self.cleaned_data['ip']
        have_symbol = re.match('[^a-z0-9.-]+', ip)
        wrong_ip = re.match('^0.|^255.', ip)
        if have_symbol:
            raise forms.ValidationError(_('Hostname must contain only numbers, or the domain name separated by "."'))
        elif wrong_ip:
            raise forms.ValidationError(_('Wrong IP address'))
        try:
            Host.objects.get(ip=ip)
        except Host.DoesNotExist:
            return ip
        raise forms.ValidationError(_('This host is already connected'))

class HostEditTcpForm(forms.Form):
    name = forms.CharField(error_messages={'required': _('No hostname has been entered')},
                           max_length=40)
    ip = forms.CharField(error_messages={'required': _('No IP / Domain name has been entered')},
                               max_length=100)
    login = forms.CharField(error_messages={'required': _('No login has been entered')},
                            max_length=20)
    password1 = forms.CharField(error_messages={'required': _('No password has been entered')},
                                max_length=20)
    password2 = forms.CharField(error_messages={'required': _('No password confirm name has been entered')},
                                max_length=20)

    def clean(self):
        ip = self.cleaned_data.get('ip')
        name = self.cleaned_data.get('name')

        ip_have_symbol = re.match('[^a-z0-9.-]+', ip)
        if ip_have_symbol:
            raise forms.ValidationError(_('Hostname must contain only numbers, or the domain name separated by "."'))

        ip_wrong = re.match('^0.|^255.', ip)
        if ip_wrong:
            raise forms.ValidationError(_('Wrong IP address'))
        
        other_host = Host.objects.filter(~Q(name=name), ip = ip)
        if len(other_host) > 0:
            raise forms.ValidationError(_('This host is already connected'))

        password1 = self.cleaned_data.get('password1')
        password2 = self.cleaned_data.get('password2')
        if password1 and password1 != password2:
            raise forms.ValidationError(_('Your password didn\'t match. Please try again.'))
        return self.cleaned_data

class HostEditSshForm(forms.Form):
    name = forms.CharField(error_messages={'required': _('No hostname has been entered')},
                           max_length=40)
    ip = forms.CharField(error_messages={'required': _('No IP / Domain name has been entered')},
                               max_length=100)
    login = forms.CharField(error_messages={'required': _('No login has been entered')},
                            max_length=20)
    port = forms.IntegerField(error_messages={'required': _('No SSH port has been entered')})

    def clean(self):
        ip = self.cleaned_data.get('ip')
        name = self.cleaned_data.get('name')

        ip_have_symbol = re.match('[^a-z0-9.-]+', ip)
        if ip_have_symbol:
            raise forms.ValidationError(_('Hostname must contain only numbers, or the domain name separated by "."'))

        ip_wrong = re.match('^0.|^255.', ip)
        if ip_wrong:
            raise forms.ValidationError(_('Wrong IP address'))
        
        other_host = Host.objects.filter(~Q(name=name), ip = ip)
        if len(other_host) > 0:
            raise forms.ValidationError(_('This host is already connected'))

        return self.cleaned_data