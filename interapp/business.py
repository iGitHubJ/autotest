#!/usr/bin/python
# -*- coding:utf8 -*-
"""
业务模块：
    执行接口，保存执行结果，实现对接口/服务器/执行结果的增删改查
    @author: 898596025@qq.com
    @license: http://www.apache.org/licenses/
    @bug: 暂不支持分页显示
    @change: 
    @copyright: 版权所有
    @since: 1.0
    @version: 1.0
"""
from __future__ import unicode_literals
from __future__ import division
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
    """
 执行接口测试，并保存执行结果
    @param  serverIds:服务器id
    @param  interIds:接口id
    """
    log.debug("==============开始执行测试脚本==============")
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
                    log.debug("验证成功")
                    success += 1
                    res = True
                else:
                    log.warn("验证失败")
                    fail += 1
                    res = False
                end = time.time()
                result = models.Result(server=server, inter=inter, req=input, resp=response, result=res, spend=(int)((end - begin) * 1000))
                result.save()
                log.debug("已将%s保存到数据库" % result)
        log.debug("==============测试脚本执行结束==============")
        log.info("本次共测试：%d个接口，成功：%d，失败：%d" % (total, success, fail))
        return (total, success, fail)
    except Exception as e:
        log.error("程序遇到异常=>" + traceback.format_exc())
    

def listResults():
    """
  查询执行结果
    """
    log.info("查询执行结果")
    return models.Result.objects.order_by('-createtime', 'id')[0:100]

def listServersAndInters(serverIds=None, interIds=None):
    """
 列出所有的服务器和接口信息
    @param  serverIds:服务器id
    @param  interIds:接口id
    """
    log.info("查询接口列表")
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
    log.debug("servers:%s,inters:%s" % (servers, inters))
    return (servers, inters)


def init():
    """如果数据库没有配置响应的数据，则将配置文件中的配置加载到数据库中"""
    servers = models.Server.objects.all();
    if servers is None or len(servers) == 0:
        result = parse()
        if result is None or len(result) == 0:
            raise Exception("请在config/config.xml文件中配置初始接口")
        else:
            servers = result['servers']
            services = result['services']
            for name in servers:
                server = models.Server(name=name);
                try:
                    server.save()
                except Exception:
                    log.error("程序遇到异常=>" + traceback.format_exc())
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
                            log.error("程序遇到异常=>" + traceback.format_exc())

        


# if __name__ == "__main__":
#     log.info("==============开始执行测试脚本==============")
#     (total, success, fail) = runAndSave()
#     log.info("==============测试脚本执行结束==============")
#     log.info("本次共测试：%d个接口，成功：%d，失败：%d" % (total, success, fail))




def delete(tag, ID):
    """
 删除服务器或者接口信息
    @param  tag:server服务器,inter接口
    @param  ID:服务器或者接口id
    """
    if tag and ID:
        if tag == 'server':
            log.debug("删除id为%d的服务器信息" % ID)
            models.Server.objects.filter(id=ID).delete()
            return True
        elif tag == 'inter':
            log.debug("删除id为%d的接口信息" % ID)
            models.Inter.objects.filter(id=ID).delete()
            return True
    return False

def batchdel(tag, ids):
    if tag and ids and isinstance(ids, list):
        if tag == 'result':
            log.debug("批量删除id为%s的测试结果信息" % (json.dumps(ids)))
            models.Result.objects.filter(id__in=ids).delete()
            return True
    return False


def findInterById(ID):
    """
 根据id查询接口信息
    @param  ID:接口id
    """
    if ID :
        return models.Inter.objects.get(id=ID)

def findServerById(ID):
    """
 根据id查询服务器地址
    @param  ID:服务器地址id
    """
    if ID :
        return models.Server.objects.get(id=ID)


def saveOrUpdateInter(inter):
    """
    保存或者更新接口地址信息
    @param  inter:接口地址对象
    """
    if inter.id is None:
        log.debug("保存%s对象" % inter)
        inter.save()
        return True
    else:
        log.debug("更新%s对象" % inter)
        models.Inter.objects.filter(id=inter.id).update(input=inter.input)
        return True
        


def saveServer(server):
    """
    保存服务器信息
    @param  server:服务器地址对象
    """
    if server:
        server.save()
        return True
    return False


