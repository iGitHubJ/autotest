#!/usr/bin/python
# -*- coding:utf8 -*-
import sys, os, json
import datetime, time, traceback
from utils import constant
from utils.xml_util import parse
from utils import compare_util
from utils import http_request
from interapp import models
from utils import logger
log = logger.get()

reload(sys) 
sys.setdefaultencoding(constant.CHARSET)

def runAndSave(serverIds=None, interIds=None):
    log.debug(u"==============开始执行测试脚本==============")
    total = success = fail = 0
    try:
        (servers, inters) = listServersAndInters(serverIds, interIds)
        for inter in inters:
            for server in servers:
                total += 1
                url = 'http://%s/%s%s' % (server.name, inter.service, inter.path)
                method = inter.method
                enc = inter.enc
                input = inter.input
                output = inter.output
                begin = time.time()
                response = http_request.request(url=url, method=method, body=input)
                res = False
                if compare_util.loosecmp(output, response):
                    log.debug(u"验证成功")
                    success += 1
                    res = True
                else:
                    log.warn(u"验证失败")
                    fail += 1
                    res = False
                end = time.time()
                result = models.Result(server=server, inter=inter, req=input, resp=response, result=res, spend=(int)((end - begin) * 1000))
                result.save()
                log.debug(u"已将%s保存到数据库" % result)
        log.debug(u"==============测试脚本执行结束==============")
        log.info(u"本次共测试：%d个接口，成功：%d，失败：%d" % (total, success, fail))
        return (total, success, fail)
    except Exception as e:
        log.error(u"程序遇到异常=>" + traceback.format_exc())
    

def listResults():
    log.info(u"查询执行结果")
    return models.Result.objects.order_by('-createtime', 'id')[0:100]

def listServersAndInters(serverIds=None, interIds=None):
    log.info(u"查询接口列表")
    servers = None
    inters = None
    if serverIds and isinstance(serverIds, list) and len(serverIds) > 0:
        servers = models.Server.objects.filter(id__in=serverIds).order_by('-createtime', 'id')
    else:
        servers = models.Server.objects.order_by('-createtime', 'id')[0:100]
    
    if interIds and isinstance(interIds, list) and len(interIds) > 0:
        inters = models.Inter.objects.filter(id__in=interIds).order_by('-createtime', 'id')
    else:
        inters = models.Inter.objects.order_by('-createtime', 'id')[0:100]
    log.debug("servers:%s,inters:%s"%(servers,inters))
    return (servers, inters)


def init():
    """init() 如果数据库没有配置响应的数据，则将配置文件中的配置加载到数据库中"""
    servers = models.Server.objects.all();
    if servers is None or len(servers) == 0:
        result = parse()
        if result is None or len(result) == 0:
            raise Exception(u"请在config/config.xml文件中配置初始接口")
        else:
            servers = result['servers']
            services = result['services']
            for name in servers:
                server = models.Server(name=name);
                try:
                    server.save()
                except Exception:
                    log.error(u"程序遇到异常=>" + traceback.format_exc())
            for service in services:
                for name, interfaces in service.items():
                    for interface in interfaces:
                        url = interface['url']
                        method = interface['method']  # GET/POST/PUT/HEAD
                        enc = interface['enc']  # json/xml/urlencode
                        input = interface['input']
                        output = interface['output']
                        inter = models.Inter(service=name, path=url, method=method, enc=enc, input=input, output=output)
                        try:
                            inter.save()
                        except Exception:
                            log.error(u"程序遇到异常=>" + traceback.format_exc())

        


# if __name__ == "__main__":
#     log.info("==============开始执行测试脚本==============")
#     (total, success, fail) = runAndSave()
#     log.info("==============测试脚本执行结束==============")
#     log.info("本次共测试：%d个接口，成功：%d，失败：%d" % (total, success, fail))




