#!/usr/bin/python
# -*- coding:utf8 -*-
from __future__ import division
import sys,os,json
import datetime,time
from xml.dom.minidom import parse
import xml.dom.minidom
from utils import constant
from autotest import settings
from utils import logger
log = logger.get()

reload(sys) 
sys.setdefaultencoding(constant.CHARSET)

def parse(xml_path=settings.CONFIG_ROOT+'\\config.xml'):
    # 使用minidom解析器打开 XML 文档
    DOMTree = xml.dom.minidom.parse(xml_path)
    collection = DOMTree.documentElement

    #解析servers
    oservers = collection.getElementsByTagName("server")
    servers=[]
    for server in oservers:
        servers.append(server.childNodes[0].data.strip())
    log.info('servers : %s'% json.dumps(servers))
    #解析interfaces
    oservices = collection.getElementsByTagName("service")
    services=[]
    for service in oservices:
        interfaces=[]
        name=service.getAttribute("name")
        ointerfaces=service.getElementsByTagName("interface")
        for interface in ointerfaces:
            inter={}
            inter['url']=interface.getElementsByTagName("url")[0].childNodes[0].data.strip()
            inter['method']=interface.getElementsByTagName("method")[0].childNodes[0].data.strip()
            inter['enc']=interface.getElementsByTagName("enc")[0].childNodes[0].data.strip()
            inter['input']=interface.getElementsByTagName("input")[0].childNodes[0].data.strip()
            inter['output']=interface.getElementsByTagName("output")[0].childNodes[0].data.strip()
            interfaces.append(inter)
        services.append({name:interfaces})
    result={'servers':servers,'services':services}
    log.info("xml解析：%s" % json.dumps(result))
    return result;

if __name__=='__main__':
    parse()


















