import json
import hashlib
import time
import socket
import requests
import urllib3
import os
import random
import datetime
import base64
import ping3
import uuid
from urlparser import urlparser

import mecord.pb.uauth_common_pb2 as uauth_common_pb2
import mecord.pb.uauth_ext_pb2 as uauth_ext_pb2
import mecord.pb.common_ext_pb2 as common_ext_pb2
import mecord.pb.aigc_ext_pb2 as aigc_ext_pb2
import mecord.pb.rpcinput_pb2 as rpcinput_pb2
from mecord import store 
from mecord import utils 
from mecord import taskUtils 
from mecord import constant 

def resolve_dns_with_ali(domain):
    for url in ["https://dns.alidns.com/resolve", "https://alidns_ip/resolve", "http://dns.alidns.com/resolve", "http://alidns_ip/resolve"]:
        params = {
            "name": domain,
            "type": 1,
            "short": 1,
            # "uid": "35396342",
        }
        response = requests.get(url, params=params)
        if response.status_code == 200:
            result = response.json()
            taskUtils.taskPrint(None, f"resolve_dns_with_ali {domain} -> {result}")
            return result
    return []
       
def resolve_dns_with_tencent(domain):
    for url in ["https://119.29.29.99/d?"]:
        params_str = f"dn={domain}&token=772808172"
        response = requests.get(f"{url}{params_str}")
        result = response.content.decode("utf-8").split(";")
        taskUtils.taskPrint(None, f"resolve_dns_with_tencent {domain} -> {result}")
        return result

def _try_network():
    try:
        for url in ["https://www.baidu.com/", "https://www.google.com/"]:
            s = requests.session()
            s.keep_alive = False
            s.headers.update({'Connection':'close'})
            res = s.get(url=url, timeout=30)
            taskUtils.taskPrint(None, f"=== probe url={url} result_code={res.status_code}")
            s.close()
            
        for ip in ["www.baidu.com", "www.google.com", "1.1.1.1", "8.8.8.8", "208.67.222.222"]:
            res = ping3.ping(ip, timeout=5)
            if res:
                taskUtils.taskPrint(None, f"=== ping {ip} success")
            else:
                taskUtils.taskPrint(None, f"=== probe {url} fail")
    finally:
        return
    
DIRECT_DOMAIN = {
    "https://api.mecordai.com/proxymsg" : "https://api-us-dc.mecordai.com/proxymsg",
    "https://api-sg.mecordai.com/proxymsg" : "https://api-sg-dc.mecordai.com/proxymsg"
}
def _domain_post(url, data):
    try:
        s = requests.session()
        requests.adapters.DEFAULT_RETRIES = 2
        s.keep_alive = False
        res = s.post(url=url, data=data, timeout=30, headers={'Connection':'close'})
        if res.status_code == 200:
            res_content = res.content
            res.close()
            return True, res_content 
        else:
            return False, f"status_code={res.status_code}"
    except Exception as e:
        return False, f"{e}"
    finally:
        s.close()
def _ip_post(url, data, direct_ip):
    try:
        s = requests.session()
        requests.adapters.DEFAULT_RETRIES = 2
        s.keep_alive = False
        domain = urlparser.urlparse(url).hostname
        real_url = url.replace(domain, direct_ip)
        res = s.post(url=real_url, data=data, timeout=30, headers={'Connection':'close','Host':domain}, verify=False)
        if res.status_code == 200:
            res_content = res.content
            res.close()
            return True, res_content 
        else:
            return False, f"status_code={res.status_code}"
    except Exception as e:
        return False, f"{e}"
    finally:
        s.close()
def post(url, data, direct_ip=None):
    try:
        s = requests.session()
        requests.adapters.DEFAULT_RETRIES = 2
        s.keep_alive = False
        s.headers.update({'Connection':'close'})
        real_url = url
        if direct_ip:
            domain = urlparser.urlparse(url).hostname
            real_url = real_url.replace(domain, direct_ip)
            s.headers.update({'Host':domain})
        res = s.post(url=real_url, data=data, timeout=30, verify=False)
        if res.status_code == 200:
            res_content = res.content
            res.close()
            return res_content 
        else:
            raise Exception(f"status_code={res.status_code}")
    except:
        if url in DIRECT_DOMAIN:
            taskUtils.taskPrint(None, f"domain request fail! redo to dc")
            success, result = _domain_post(DIRECT_DOMAIN[url], data)
            if success:
                return result
        taskUtils.taskPrint(None, f"domain request fail! redo to direct ip")
        domain = urlparser.urlparse(url).hostname
        for ip in resolve_dns_with_ali(domain):
            if len(ip) > 0:
                success, result = _ip_post(url,data,ip)
                if success:
                    return result
        for ip in resolve_dns_with_tencent(domain):
            if len(ip) > 0:
                success, result = _ip_post(url,data,ip)
                if success:
                    return result
        _try_network()
        raise Exception(f"all host & ip has fail!")
    finally:
        s.close()