#!/usr/bin/python
# -*- coding:utf8 -*-
import sys, os, json
import datetime, time
from utils import constant
from utils.xml_util import parse
from utils import compare_util
from utils import http_request
from urlinter.models import Inter
from utils import logger
log = logger.get()

reload(sys) 
sys.setdefaultencoding(constant.CHARSET)

def runAndSave():
    log.debug(u"==============开始执行测试脚本==============")
    total = success = fail = 0
    try:
        result = parse()
        servers = result['servers']
        services = result['services'];

        for service in services:
            for name, interfaces in service.items():
                log.debug("name=%s,value=%s" % (name, interfaces))
                for interface in interfaces:
                    url = interface['url']
                    method = interface['method']  # GET/POST/PUT/HEAD
                    enc = interface['enc']  # json/xml/urlencode
                    inputs = interface['input']
                    output = interface['output']
                    for server in servers:
                        total += 1
                        addr = 'http://%s/%s%s' % (server, name, url)
                        begin = time.time()
                        resp = http_request.request(url=addr, method=method, body=inputs)
                        log.debug(u"返回:%s" % resp)
                        res = False
                        if compare_util.loosecmp(output, resp):
                            log.info(u"验证成功")
                            success += 1
                            res = True
                        else:
                            log.warn(u"验证失败")
                            fail += 1
                            res = False
                        end = time.time()
                        inter = Inter(addr=addr, method=method, enc=enc, inputs=inputs, output=output, response=resp, result=res, spend=(end - begin))
                        inter.save()
                        log.debug(u"已将%s保存到数据库"% inter)
        log.debug(u"==============测试脚本执行结束==============")
        log.info(u"本次共测试：%d个接口，成功：%d，失败：%d" % (total, success, fail))
        return (total, success, fail)
    except Exception as e:
        log.error(u"程序遇到异常=>" + traceback.format_exc())
    

def listResults():
    log.info(u"查询执行结果")
    inters=Inter.objects.order_by('-createtime','id')[0:100]
#     log.info(u"执行结果"+inters)
    return inters


# if __name__ == "__main__":
#     log.info("==============开始执行测试脚本==============")
#     (total, success, fail) = runAndSave()
#     log.info("==============测试脚本执行结束==============")
#     log.info("本次共测试：%d个接口，成功：%d，失败：%d" % (total, success, fail))




