# coding=utf-8
import json
import urllib
import urllib2
import httplib
import logging
import datetime
import time

true = True
null = None

# identity_service = "192.168.0.50:35357"
# volume_service = "192.168.0.51:8776"
compute_service = "192.168.0.51:8774"
image_service = "192.168.0.50:9292"

def http_send(method, host, url, header, body):
    conn = httplib.HTTPConnection(host)
    conn.request(method, url, body, header)
    response = conn.getresponse()
    data = response.read()
    try:
        dict_res = json.loads(data)
    except:
        dict_res = {}
    else:
        pass
    finally:
        conn.close()
    return dict_res

def http_send2(method, host, url, header, body):
    conn = httplib.HTTPConnection(host)
    conn.request(method, url, body, header)
    response = conn.getresponse()
    conn.close()
    return response

def server_list(token, tenant):
    method = 'GET'
    host = compute_service
    url = '/v2/%s/servers/detail' % (tenant)
    headers = {"Content-Type": "application/json", "X-Auth-Token":token}
    res = http_send(method, host, url, headers, None)
    ins_list = []
    try:
        for server in res['servers']:
            '''
            {
            "OS-DCF:diskConfig": "MANUAL", 
            "OS-EXT-SRV-ATTR:host": "compute3", 
            "OS-EXT-SRV-ATTR:hypervisor_hostname": "compute3", 
            "OS-EXT-SRV-ATTR:instance_name": "instance-00000037", 
            "OS-EXT-STS:power_state": 1, 
            "OS-EXT-STS:task_state": null, 
            "OS-EXT-STS:vm_state": "active", 
            "accessIPv4": "", 
            "accessIPv6": "", 
            "addresses": {
                "private": [
                    {
                        "addr": "10.101.101.6", 
                        "version": 4
                    }
                ]
            }, 
            "config_drive": "", 
            "created": "2013-06-17T05:41:08Z", 
            "flavor": {
                "id": "1", 
                "links": [
                    {
                        "href": "http://192.168.0.51:8774/86e5ae17b73749b3957886c5ad512ba0/flavors/1", 
                        "rel": "bookmark"
                    }
                ]
            }, 
            "hostId": "a8ca5519a47a7974bd9ad5e6fe0cba9f09ba8b761252e6adb5d308d4", 
            #"id": "122deb84-2bf9-4786-8427-2da9ac2a4172", 
            #"image": {
                "id": "15338178-650e-4602-aade-55089d5aecab", 
                "links": [
                    {
                        "href": "http://192.168.0.51:8774/86e5ae17b73749b3957886c5ad512ba0/images/15338178-650e-4602-aade-55089d5aecab", 
                        "rel": "bookmark"
                    }
                ]
            }, 
            #"key_name": null, 
            "links": [
                {
                    "href": "http://192.168.0.51:8774/v2/86e5ae17b73749b3957886c5ad512ba0/servers/122deb84-2bf9-4786-8427-2da9ac2a4172", 
                    "rel": "self"
                }, 
                {
                    "href": "http://192.168.0.51:8774/86e5ae17b73749b3957886c5ad512ba0/servers/122deb84-2bf9-4786-8427-2da9ac2a4172", 
                    "rel": "bookmark"
                }
            ], 
            "metadata": {}, 
            #"name": "testServer2_3", 
            "progress": 0, 
            "security_groups": [
                {
                    "name": "default"
                }
            ],
            "status": "ACTIVE", 
            "tenant_id": "86e5ae17b73749b3957886c5ad512ba0", 
            "updated": "2013-06-19T07:10:06Z", 
            "user_id": "b9855431a321401d8845cd3a07e80042"
            }
            '''
            server.setdefault('task_state',server['OS-EXT-STS:task_state'])
            ins_list.append(server)
            '''
            ins = {
                   'OS-EXT-SRV-ATTR:host':res['servers'][i]['OS-EXT-SRV-ATTR:host'],
                   'OS-EXT-SRV-ATTR:hypervisor_hostname':res['servers'][i]['OS-EXT-SRV-ATTR:hypervisor_hostname'],
                   'OS-EXT-STS:power_state':res['servers'][i]['OS-EXT-STS:power_state'],
                   'OS-EXT-STS:vm_state':res['servers'][i]['OS-EXT-STS:vm_state'],
                   'OS-EXT-STS:task_state':res['servers'][i]['OS-EXT-STS:task_state'],
                   'created':res['servers'][i]['created'],
                   'hostId':res['servers'][i]['hostId'],
                   'id':res['servers'][i]['id'],
                   'image':res['servers'][i]['image']['id'],
                   'flavor':res['servers'][i]['flavor']['id'],
                   'key_name':res['servers'][i]['key_name'],
                   'name':res['servers'][i]['name'],
                   'status':res['servers'][i]['status'],
                   'security_groups':res['servers'][i]['security_groups'][0]['name'],
                   'updated':res['servers'][i]['updated'],
                   'tenant_id':res['servers'][i]['tenant_id'],
                   'user_id':res['servers'][i]['user_id'],
                   }
            '''
    except:
        ins_list = []
    else:
        pass
    finally:
        pass
    return ins_list

def get_server_detail(token, tenant, server):
    method = 'GET'
    host = compute_service
    url = '/v2/%s/servers/%s' % (tenant, server)
    headers = {"Content-Type": "application/json", "X-Auth-Token":token}
    res = http_send(method, host, url, headers, None)
    try:
        server = res['server']
        '''
        server = {
        "OS-DCF:diskConfig": "MANUAL",
        "OS-EXT-SRV-ATTR:host": "compute1",
        "OS-EXT-SRV-ATTR:hypervisor_hostname": "compute1",
        "OS-EXT-SRV-ATTR:instance_name": "instance-00000038",
        "OS-EXT-STS:power_state": 1,
        "OS-EXT-STS:task_state": null,
        "OS-EXT-STS:vm_state": "active",
        #"accessIPv4": "",
        #"accessIPv6": "",
        #"addresses": {
            "private": [
                {
                    "addr": "10.101.101.8",
                    "version": 4
                }
            ]
        },
        #"config_drive": "",
        #"created": "2013-06-17T05:44:34Z",
        #"flavor": {
            "id": "1",
            "links": [
                {
                    "href": "http://192.168.0.51:8774/86e5ae17b73749b3957886c5ad512ba0/flavors/1",
                    "rel": "bookmark"
                }
            ]
        },
        #"hostId": "d13b8cd12cab4fb35ff1a5ec55ab884d3974a0be97279f5facd8d81d",
        #"id": "d6dad2dc-7e3c-4c16-a4a3-ab0b874efbfa",
        #"image": {
            "id": "15338178-650e-4602-aade-55089d5aecab",
            "links": [
                {
                    "href": "http://192.168.0.51:8774/86e5ae17b73749b3957886c5ad512ba0/images/15338178-650e-4602-aade-55089d5aecab",
                    "rel": "bookmark"
                }
            ]
        },
        #"key_name": null,
        "links": [
            {
                "href": "http://192.168.0.51:8774/v2/86e5ae17b73749b3957886c5ad512ba0/servers/d6dad2dc-7e3c-4c16-a4a3-ab0b874efbfa",
                "rel": "self"
            },
            {
                "href": "http://192.168.0.51:8774/86e5ae17b73749b3957886c5ad512ba0/servers/d6dad2dc-7e3c-4c16-a4a3-ab0b874efbfa",
                "rel": "bookmark"
            }
        ],
        #"metadata": {},
        #"name": "testServer2_4",
        #"progress": 0,
        #"security_groups": [
            {
                "name": "default"
            }
        ],
        #"status": "ACTIVE",
        #"tenant_id": "86e5ae17b73749b3957886c5ad512ba0",
        #"updated": "2013-06-19T07:10:07Z",
        #"user_id": "b9855431a321401d8845cd3a07e80042"
        }
        '''
    except:
        server = {}
    else:
        pass
    finally:
        pass
    return server

def server_create(token, tenant, name, image, flavor, metadata):
    method = 'POST'
    host = compute_service
    url = '/v2/%s/servers' % (tenant)
    header = {"Content-Type": "application/json", "X-Auth-Token":token}
    param = {"server": 
              {
               "name": name,
               "imageRef": image,
               "flavorRef": flavor,
               "metadata": metadata,
               "security_group":"new_security",
               "personality": [],
               }
              }
    res = http_send(method, host, url, header, json.dumps(param))
    '''
    {u'server': 
        {
        u'links': [
            {
            u'href': u'http://192.168.0.51:8774/v2/86e5ae17b73749b3957886c5ad512ba0/servers/be20343e-99b7-40fe-ab98-f185885122cb', 
            u'rel': u'self'
            }, 
            {
            u'href': u'http://192.168.0.51:8774/86e5ae17b73749b3957886c5ad512ba0/servers/be20343e-99b7-40fe-ab98-f185885122cb', 
            u'rel': u'bookmark'
            }
            ], 
        u'OS-DCF:diskConfig': u'MANUAL', 
        u'id': u'be20343e-99b7-40fe-ab98-f185885122cb', 
        u'security_groups': [{u'name': u'default'}], 
        u'adminPass': u'7w4EoW8VVSwY'
        }
    }
    '''
    '''
    {u'badRequest': {u'message': u'Server name is an empty string', u'code': 400}}
    '''
    try:
        res['server']
        code = 200
        message = 'server create successful ,password:' + res['server']['adminPass']
    except:
        res['badRequest']
        code = res['badRequest']['code']
        message = res['badRequest']['message']
    else:
        pass
    finally:
        pass
    return code, message

def server_delete(token, tenant, server):
    method = 'DELETE'
    host = compute_service
    url = '/v2/%s/servers/%s' % (tenant, server)
    header = {"Content-Type": "application/json", "X-Auth-Token":token}
    res = http_send2(method, host, url, header, None)
    return res.status, res.reason

def server_create_image(token, tenant, server, i_name):
    method = 'POST'
    host = compute_service
    url = '/v2/%s/servers/%s/action' % (tenant, server)
    header = {"Content-Type": "application/json", "X-Auth-Token":token}
    param = {
             "createImage" : 
             {
              "name" : i_name,
              "metadata": 
              {
               }
              }
             }
    res = http_send2(method, host, url, header, json.dumps(param))
    return res.status, res.reason

# replace with server_list
# def get_server_info(token, tenant, server):
#    method = 'GET'
#    url = compute_service
#    body = '/v2/%s/servers/%s' % (tenant, server)
#    headers = {"Content-Type": "application/json", "X-Auth-Token":token}
#    res = http_send(method, url, body, headers, None)
#    vh = {}
#    try:
#        res['server']
#    except:
#        res = None
#    else:
#        vh = {
#            'name':res['server']['name'],
#            'addresses':res['server']['addresses']['private'],
#            'key_name':res['server']['key_name'],
#            'status': res['server']['status'],
#            # 'vm_state':res['server']['OS-EXT-STS:vm_state'],
#            # 'power_state':res['server']['OS-EXT-STS:power_state'],
#            }
#        # print vh
#    finally:
#        pass
#    return vh

# depreacted,instead by glance.get_serverSnapshotList
def get_image_list(token, tenant):
    method = 'GET'
    host = image_service
    url = '/v2/images'
    headers = {"Content-Type": "application/json", "X-Auth-Token":token}
    res = http_send(method, host, url, headers, None)
    image_list = []
    try:
        res['images']
    except:
        res = None
    else:
        for i in range(len(res['images'])):
            image = {
                     'id':res['images'][i]['id'],
                     'container_format':res['images'][i]['container_format'],
                     'disk_format':res['images'][i]['disk_format'],
                     'name':res['images'][i]['name'],
                     'status':res['images'][i]['status'],
                     'visibility':res['images'][i]['visibility'],
                     'size':res['images'][i]['size'],
                     }
            image_list.append(image)
        # print image_list
    finally:
        pass
    return image_list


def get_flavor_list(token, tenant):
    method = 'GET'
    host = compute_service
    url = '/v2/%s/flavors/detail' % (tenant)
    headers = {"Content-Type": "application/json", "X-Auth-Token":token}
    res = http_send(method, host, url, headers, None)
    flavor_list = []
    try:
        for i in range(len(res['flavors'])):
            flavor = {
                     'id':res['flavors'][i]['id'],
                     'disk':res['flavors'][i]['disk'],
                     'name':res['flavors'][i]['name'],
                     'ram':res['flavors'][i]['ram'],
                     'swap':res['flavors'][i]['swap'],
                     'vcpus':res['flavors'][i]['vcpus'],
                     'public':res['flavors'][i]['os-flavor-access:is_public'],
                     'rxtx':res['flavors'][i]['rxtx_factor'],
                     }
            flavor_list.append(flavor)
    except:
        flavor_list = []
    else:
        pass
    finally:
        pass
    return flavor_list

def flavor_detail(token, tenant, id):
    method = 'GET'
    host = compute_service
    url = '/v2/%s/flavors/%s' % (tenant, id)
    headers = {"Content-Type": "application/json", "X-Auth-Token":token}
    res = http_send(method, host, url, headers, None)
    flavorInfo = {}
    try:
        flavorInfo = res['flavor']
    except:
        flavorInfo = {}
    else:
        pass
    finally:
        pass
    return flavorInfo

def get_volume_list(token, tenant):
    method = 'GET'
    host = compute_service
    url = '/v2/%s/os-volumes' % (tenant)
    headers = {"Content-Type": "application/json", "X-Auth-Token":token}
    res = http_send(method, host, url, headers, None)
    volume_list = []
    try:
        res['volumes']
    except:
        res = None
    else:
        for i in range(len(res['volumes'])):
            volume = {
                     'createdAt':res['volumes'][i]['createdAt'],
                     'displayDescription':res['volumes'][i]['displayDescription'],
                     'displayName':res['volumes'][i]['displayName'],
                     'id':res['volumes'][i]['id'],
                     'size':res['volumes'][i]['size'],
                     'status':res['volumes'][i]['status'],
                     'attachments':res['volumes'][i]['attachments'],
                     }
            volume_list.append(volume)
        # print volume_list
    finally:
        pass
    return volume_list

def volume_detail(token, tenant, volume_id):
    method = 'GET'
    host = compute_service
    url = '/v2/%s/os-volumes/%s' % (tenant, volume_id)
    headers = {"Content-Type": "application/json", "X-Auth-Token":token}
    res = http_send(method, host, url, headers, None)
    try:
        detail = res['volume']
    except:
        detail = {}
    else:
        pass
    finally:
        pass
    return detail

def volume_delete(token, tenant, volume_id):
    method = 'DELETE'
    host = compute_service
    url = '/v2/%s/os-volumes/%s' % (tenant, volume_id)
    headers = {"Content-Type": "application/json", "X-Auth-Token":token}
    res = http_send2(method, host, url, headers, None)
    code = res.status
    message = res.reason
    print code
    if(res.status != 202):
        data = http_send(method, host, url, headers, None)
        try:
            code = data['badRequest']['code']
            message = data['badRequest']['message']
        except:
            code = 500
            message = 'Unknown'
    return code, message

def volume_create_snapshot(token, tenant, s_name, s_desc, volume_id):
    method = 'POST'
    host = compute_service
    url = '/v2/%s/os-snapshots' % (tenant)
    header = {"Content-Type": "application/json", "X-Auth-Token":token}
    param = {
             "snapshot": 
              {
               "display_name": s_name,
               "display_description": s_desc,
               "volume_id": volume_id,
               "force": True
               }
             }
    res = http_send2(method, host, url, header, json.dumps(param))
    return res.status, res.reason

def volume_delete_snapshot(token, tenant, s_id):
    method = 'DELETE'
    host = compute_service
    url = '/v2/%s/os-snapshots/%s' % (tenant, s_id)
    headers = {"Content-Type": "application/json", "X-Auth-Token":token}
    res = http_send2(method, host, url, headers, None)
    return res.status, res.reason

def get_volume_snapshot_list(token, tenant):
    method = 'GET'
    host = compute_service
    url = '/v2/%s/os-snapshots' % (tenant)
    headers = {"Content-Type": "application/json", "X-Auth-Token":token}
    res = http_send(method, host, url, headers, None)
    volume_snapshot_list = []
    try:
        for i in res['snapshots']:
            volume_snapshot_list.append(i)
    except:
        volume_snapshot_list = []
    else:
        pass
    finally:
        pass
    return volume_snapshot_list

def get_floating_ip_list(token, tenant):
    method = 'GET'
    host = compute_service
    url = '/v2/%s/os-floating-ips' % (tenant)
    headers = {"Content-Type": "application/json", "X-Auth-Token":token}
    res = http_send(method, host, url, headers, None)
    floating_ip_list = []
    try:
        for i in range(len(res['floating_ips'])):
            floating_ip = {
                           'fixed_ip':res['floating_ips'][i]['fixed_ip'],
                           'id':res['floating_ips'][i]['id'],
                           'instance_id':res['floating_ips'][i]['instance_id'],
                           'ip':res['floating_ips'][i]['ip'],
                           'pool':res['floating_ips'][i]['pool'],
                           }
            floating_ip_list.append(floating_ip)
    except:
        floating_ip_list = []
    else:
        pass
    finally:
        pass
    return floating_ip_list

def get_keypair_list(token, tenant):
    method = 'GET'
    host = compute_service
    url = '/v2/%s/os-keypairs' % (tenant)
    headers = {"Content-Type": "application/json", "X-Auth-Token":token}
    res = http_send(method, host, url, headers, None)
    keypair_list = []
    try:
        for i in range(len(res['keypairs'])):
            '''
            {
            "keypair": {
                "fingerprint": "ee:3a:7c:90:5d:52:b4:77:be:12:75:3b:d6:44:f8:62", 
                "name": "key2", 
                "public_key": "ssh-rsa AAAAB3NzaC1yc2EAAAABIwAAAIEA1iCKAiElaikAoYlYNv2qMrWyjTMeo0Rp+wrJJ87RsEYK0ateXeesiyiotPYmCVVulMAwqilKi8ZeaTn0m6/WAhQc+7tZ+wYK8i3zA6MR0HS5snSfcA2z1p5CS+l+geRvmlf8BNPnMg+j+j2drENIHsLp4Qh0FAVlMbvkYr0xY1k= Generated by Nova\n"
            }
            }
            '''
            keypair = res['keypairs'][i]['keypair']
            keypair_list.append(keypair)
    except:
        keypair_list = []
    else:
        pass
    finally:
        pass
    return keypair_list
    
def get_security_group_list(token, tenant):
    method = 'GET'
    host = compute_service
    url = '/v2/%s/os-security-groups' % (tenant)
    headers = {"Content-Type": "application/json", "X-Auth-Token":token}
    res = http_send(method, host, url, headers, None)
    security_group_list = []
    try:
        for i in range(len(res['security_groups'])):
            security_group = {
                           'description':res['security_groups'][i]['description'],
                           'id':res['security_groups'][i]['id'],
                           'name':res['security_groups'][i]['name'],
                           'rules':res['security_groups'][i]['rules'],
                           'tenant_id':res['security_groups'][i]['tenant_id'],
                           }
            security_group_list.append(security_group)
    except:
        security_group_list = []
    else:
        pass
    finally:
        pass
    return security_group_list

def get_floating_ip_pool(token, tenant):
    method = 'GET'
    host = compute_service
    url = '/v2/%s/os-floating-ip-pools' % (tenant)
    headers = {"Content-Type": "application/json", "X-Auth-Token":token}
    res = http_send(method, host, url, headers, None)
    floating_ip_pool_list = []
    try:
        for i in res['floating_ip_pools']:
            floating_ip_pool_list.append(i)
    except:
        floating_ip_pool_list = []
    else:
        pass
    finally:
        pass
    return floating_ip_pool_list

def floating_ip_allocate(token, tenant, pool):
    method = 'POST'
    host = compute_service
    url = '/v2/%s/os-floating-ips' % (tenant)
    headers = {"Content-Type":"application/json", "X-Auth-Token":token}
    param = {"pool": pool}
    res = http_send2(method, host, url, headers, json.dumps(param))
    return res.status, res.reason

def floating_ip_deallocate(token, tenant, ipid):
    method = 'DELETE'
    host = compute_service
    url = '/v2/%s/os-floating-ips/%s' % (tenant, ipid)
    headers = {"Content-Type":"application/json", "X-Auth-Token":token}
    res = http_send2(method, host, url, headers, None)
    return res.status, res.reason

def floating_ip_associate(token, tenant, ip, server):
    method = 'POST'
    host = compute_service
    url = '/v2/%s/servers/%s/action' % (tenant, server)
    headers = {"Content-Type":"application/json", "X-Auth-Token":token}
    param = {
           "addFloatingIp": {
                             "address": ip
                            }
           }
    res = http_send2(method, host, url, headers, json.dumps(param))
    return res.status, res.reason

def floating_ip_unassociate(token, tenant, ip, server):
    method = 'POST'
    host = compute_service
    url = '/v2/%s/servers/%s/action' % (tenant, server)
    headers = {"Content-Type":"application/json", "X-Auth-Token":token}
    param = {
           "removeFloatingIp": {
                             "address": ip
                            }
           }
    res = http_send2(method, host, url, headers, json.dumps(param))
    return res.status, res.reason

def tenant_usage(token, tenant, start , end):
    method = 'GET'
    host = compute_service
    url = '/v2/%s/os-simple-tenant-usage/%s?start=%s&end=%s' % (tenant, tenant, start , end)
    header = {"Content-Type": "application/json", "X-Auth-Token":token}
    tenant_usage = {}
    server_usage_list = []
    param = {}
    res = http_send(method, host, url, header, json.dumps(param))
    try:
        tenant_usage = {
                      'start':res['tenant_usage']['start'],
                      'stop':res['tenant_usage']['stop'],
                      'tenant_id':res['tenant_usage']['tenant_id'],
                      'total_hours':res['tenant_usage']['total_hours'],
                      'total_local_gb_usage':res['tenant_usage']['total_local_gb_usage'],
                      'total_memory_mb_usage':res['tenant_usage']['total_memory_mb_usage'],
                      'total_vcpus_usage':res['tenant_usage']['total_vcpus_usage'],
                      }
        for s_u in res['tenant_usage']['server_usages']:
            '''
            s_u = {
                "ended_at": null,
                "flavor": "m1.tiny",
                "hours": 8.3333333333333335e-09,
                "instance_id": "b538dab6-0111-462c-bedf-cd73f4e180ce",
                "local_gb": 0,
                "memory_mb": 512,
                "name": "osdbServer",
                "started_at": "2013-06-08T01:18:13.000000",
                "state": "active",
                "tenant_id": "86e5ae17b73749b3957886c5ad512ba0",
                "uptime": 1003322,
                "vcpus": 1
            }
            '''
            server_usage_list.append(s_u)
    except:
        tenant_usage = {}
        server_usage_list = []
    else:
        pass
    finally:
        pass
    return tenant_usage, server_usage_list
