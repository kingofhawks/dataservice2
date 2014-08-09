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

identity_service = "http://192.168.0.50:5000/v2.0"
object_store = "http://192.168.0.55:8888/v1/AUTH_tenant_id"
volume_service = "http://192.168.0.51:8776/v1/tenant_id"
# image_service = "http://192.168.0.50:9292/v1"
image_service = '192.168.0.50:9292'
compute_service = "http://192.168.0.51:8774/v2/tenant_id"

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

def get_image_list(token):
    method = 'GET'
    host = image_service
    url = '/v2/images'
    headers = {"Content-Type": "application/json", "X-Auth-Token":token}
    res = http_send(method, host, url, headers, None)
    image_list = []
    try:
        for i in range(len(res['images'])):
            if(res['images'][i].has_key('image_type')):
                name_type = res['images'][i]['name'] + ' - ' + res['images'][i]['image_type']
            else:
                image = res['images'][i]
                '''
                {
                "base_image_ref": "15338178-650e-4602-aade-55089d5aecab", 
                "checksum": "198313765c0ea6ee892aee3977773c56", 
                "container_format": "ovf", 
                "created_at": "2013-06-19T06:52:43Z", 
                "disk_format": "qcow2", 
                "file": "/v2/images/e3ba701c-abd7-4ca1-b825-f8ac2f9d8d7b/file", 
                "id": "e3ba701c-abd7-4ca1-b825-f8ac2f9d8d7b", 
                "image_location": "snapshot", 
                "image_state": "available", 
                "image_type": "snapshot", 
                "instance_uuid": "122deb84-2bf9-4786-8427-2da9ac2a4172", 
                "min_disk": 0, 
                "min_ram": 0, 
                "name": "serverSnapshot2", 
                "owner_id": "86e5ae17b73749b3957886c5ad512ba0", 
                "protected": false, 
                "schema": "/v2/schemas/image", 
                "self": "/v2/images/e3ba701c-abd7-4ca1-b825-f8ac2f9d8d7b", 
                "size": 5165547520, 
                "status": "active", 
                "tags": [], 
                "updated_at": "2013-06-19T07:10:05Z", 
                "user_id": "b9855431a321401d8845cd3a07e80042", 
                "visibility": "private"
                }
                '''
                '''
                {
                     'id':res['images'][i]['id'],
                     'container_format':res['images'][i]['container_format'],
                     'disk_format':res['images'][i]['disk_format'],
                     'name':res['images'][i]['name'],
                     'status':res['images'][i]['status'],
                     'visibility':res['images'][i]['visibility'],
                     'size':res['images'][i]['size'],
                     }
                '''
                image_list.append(image)
    except:
        image_list = []
    else:
        pass
    finally:
        pass
    return image_list

def get_server_snapshot_list(token):
    method = 'GET'
    host = image_service
    url = '/v2/images'
    headers = {"Content-Type": "application/json", "X-Auth-Token":token}
    res = http_send(method, host, url, headers, None)
    snapshot_list = []
    try:
        for i in range(len(res['images'])):
            if(res['images'][i].has_key('image_type')):
                snapshot = res['images'][i]
                '''
                {
                "base_image_ref": "15338178-650e-4602-aade-55089d5aecab", 
                "checksum": "198313765c0ea6ee892aee3977773c56", 
                "container_format": "ovf", 
                "created_at": "2013-06-19T06:52:43Z", 
                "disk_format": "qcow2", 
                "file": "/v2/images/e3ba701c-abd7-4ca1-b825-f8ac2f9d8d7b/file", 
                "id": "e3ba701c-abd7-4ca1-b825-f8ac2f9d8d7b", 
                "image_location": "snapshot", 
                "image_state": "available", 
                "image_type": "snapshot", 
                "instance_uuid": "122deb84-2bf9-4786-8427-2da9ac2a4172", 
                "min_disk": 0, 
                "min_ram": 0, 
                "name": "serverSnapshot2", 
                "owner_id": "86e5ae17b73749b3957886c5ad512ba0", 
                "protected": false, 
                "schema": "/v2/schemas/image", 
                "self": "/v2/images/e3ba701c-abd7-4ca1-b825-f8ac2f9d8d7b", 
                "size": 5165547520, 
                "status": "active", 
                "tags": [], 
                "updated_at": "2013-06-19T07:10:05Z", 
                "user_id": "b9855431a321401d8845cd3a07e80042", 
                "visibility": "private"
                }
                '''
                '''
                {
                     'id':res['images'][i]['id'],
                     'container_format':res['images'][i]['container_format'],
                     'disk_format':res['images'][i]['disk_format'],
                     'name':res['images'][i]['name'],
                     'status':res['images'][i]['status'],
                     'visibility':res['images'][i]['visibility'],
                     'size':res['images'][i]['size'],
                }
                '''
                snapshot_list.append(snapshot)
    except:
        snapshot_list = []
    else:
        pass
    finally:
        pass
    return snapshot_list

def image_delete(token, id):
    method = 'DELETE'
    host = image_service
    url = '/v2/images/%s' % (id)
    header = {"Content-Type": "application/json", "X-Auth-Token":token}
    res = http_send2(method, host, url, header, None)
    return res.status, res.reason

if __name__ == '__main__':
    token = '5d7747b6a034486193cd3ba0621b7a49'
    tenant = '86e5ae17b73749b3957886c5ad512ba0'
    get_imageList(token)
