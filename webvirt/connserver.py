import libvirt
from libvirt import libvirtError
from libvirt import VIR_DOMAIN_XML_SECURE
import re
import time
from datetime import datetime
import string
from xml.etree import ElementTree
import socket

class ConnServer(object):
    def __init__(self, host):
        """

        Return connection object.

        """
        self.login = host.login
        self.host = host.ip
        self.passwd = host.password
        self.type = host.type
        self.port = host.port

        socket_host = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        socket_host.settimeout(0.4) #0.4 seconds
        if self.type == 'tcp':
            try:
                socket_host.connect((self.host, 16509))
                socket_host.close()
            except:
                self.conn = None
                return 1

            def creds(credentials, user_data):
                for credential in credentials:
                    if credential[0] == libvirt.VIR_CRED_AUTHNAME:
                        credential[4] = self.login
                        if len(credential[4]) == 0:
                            credential[4] = credential[3]
                    elif credential[0] == libvirt.VIR_CRED_PASSPHRASE:
                        credential[4] = self.passwd
                    else:
                        return -1
                return 0

            flags = [libvirt.VIR_CRED_AUTHNAME, libvirt.VIR_CRED_PASSPHRASE]
            auth = [flags, creds, None]
            uri = 'qemu+tcp://%s/system' % self.host
            self.conn = libvirt.openAuth(uri, auth, 0)
        if self.type == 'ssh':
            try:
                socket_host.connect((self.host, self.port))
                socket_host.close()
            except:
                self.conn = None
                return 1
            uri = 'qemu+ssh://%s@%s:%s/system' % (self.login, self.host, self.port)
            self.conn = libvirt.open(uri)


    def lookupVM(self, vname):
        """

        Return VM object.

        """
        try:
            dom = self.conn.lookupByName(vname)
        except:
            dom = None
        return dom

    def vds_get_node(self):
        """

        Get all VM in host server

        """
        vname = {}
        for vm_id in self.conn.listDomainsID():
            vm_id = int(vm_id)
            dom = self.conn.lookupByID(vm_id)
            vname[dom.name()] = dom.info()[0]
        for name in self.conn.listDefinedDomains():
            dom = self.lookupVM(name)
            vname[dom.name()] = dom.info()[0]
        return vname

    def storages_get_node(self):
        """

        Function return host server storages.

        """
        storages = {}
        for storage in self.conn.listStoragePools():
            stg = self.conn.storagePoolLookupByName(storage)
            status = stg.isActive()
            storages[storage] = status
        for storage in self.conn.listDefinedStoragePools():
            stg = self.storagePool(storage)
            status = stg.isActive()
            storages[storage] = status
        return storages

    def node_get_info(self):
        """

        Function return host server information: hostname, arch, memory, cpu, uri

        """
        info = []
        getInfo = self.conn.getInfo()
        info.append(self.conn.getHostname())
        info.append(getInfo[0])
        info.append(getInfo[1])
        info.append(getInfo[2])
        info.append(self.conn.getURI())
        return info

    def memory_get_usage(self):
        """

        Function return memory usage on node.

        """
        allmem = self.conn.getInfo()[1] * 1048576
        get_freemem = self.conn.getMemoryStats(-1, 0)
        if type(get_freemem) == dict:
            freemem = (get_freemem.values()[0] + \
                       get_freemem.values()[2] + \
                       get_freemem.values()[3]) * 1024
            percent = (freemem * 100) / allmem
            percent = 100 - percent
            percent = str(percent) + '%'
            memusage = (allmem - freemem)
        else:
            memusage = None
            percent = None
        return {"allmem":allmem, "memusage":memusage, "percent":percent}

    def cpu_get_usage(self):
        """

        Function return cpu usage on node.

        """
        prev_idle = 0
        prev_total = 0
        cpu = self.conn.getCPUStats(-1, 0)
        if type(cpu) == dict:
            for num in range(2):
                idle = self.conn.getCPUStats(-1, 0).values()[1]
                total = sum(self.conn.getCPUStats(-1, 0).values())
                diff_idle = idle - prev_idle
                diff_total = total - prev_total
                diff_usage = (1000 * (diff_total - diff_idle) / diff_total + 5) / 10
                prev_total = total
                prev_idle = idle
                if num == 0:
                    time.sleep(1)
                else:
                    if diff_usage < 0:
                        diff_usage = 0
        else:
            diff_usage = None
        return diff_usage


    def vds_on_cluster(self):
        """

        Function show all host and vds

        """
        vname = {}
        host_mem = self.conn.getInfo()[1] * 1048576
        for vm_id in self.conn.listDomainsID():
            vm_id = int(vm_id)
            dom = self.conn.lookupByID(vm_id)
            mem = get_xml_path(dom.XMLDesc(0), "/domain/memory")
            mem = int(mem) * 1024
            mem_usage = (mem * 100) / host_mem
            vcpu = get_xml_path(dom.XMLDesc(0), "/domain/vcpu")
            vname[dom.name()] = (dom.info()[0], vcpu, mem, mem_usage)
        for name in self.conn.listDefinedDomains():
            dom = self.lookupVM(name)
            mem = get_xml_path(dom.XMLDesc(0), "/domain/memory")
            mem = int(mem) * 1024
            mem_usage = (mem * 100) / host_mem
            vcpu = get_xml_path(dom.XMLDesc(0), "/domain/vcpu")
            vname[dom.name()] = (dom.info()[0], vcpu, mem, mem_usage)
        return vname

    def close(self):
        """

        Close libvirt connection.

        """
        self.conn.close()