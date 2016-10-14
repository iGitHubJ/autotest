#!/usr/bin/python
#-*-coding:utf-8-*-
from __future__ import unicode_literals
import httplib2,urllib,urlparse
import sys,os,json,traceback
import datetime,time
from utils import constant
from utils import logger
log = logger.get()

#解决python2.7 中文字符 UnicodeDecodeError: 'ascii' codec can't decode byte
reload(sys) 
sys.setdefaultencoding(constant.CHARSET)

h=httplib2.Http()

#charset = 'UTF-8'

'''
将dict转化为url参数形式的字符串（k1=v1&k2=v2）
urllib.urlencode(dict)
'''
def toUrlParams(params):
    result=""
    if isinstance(params,dict) and len(params)>0:
        for k,v in params.items():
            result += '%s=%s?'%(k,v)
        return result[:-1]

'''
get请求
HTTP/1.1 505 HTTP Version Not Supported原因和解决办法
url中存在空格
1.url编码，空格"%20"
2.用post 非拼接参数形式 do_post_form
'''
def do_get(url, params=None):
    log.debug("url:%s,params:%s"%(url, params))
    if params :
        if isinstance(params,dict):
            if '?' in url :
                #url+=toUrlParams(params)
                url += urllib.urlencode(params)
            else:
                #url += '?'+toUrlParams(params)
                url += '?' + urllib.urlencode(params)
        elif isinstance(params,str) or isinstance(params,unicode):
            if '&' in params and '=' in params:
                url+=(params if '?' in url else '?'+params)
            else:
                log.warn('参数格式错误，已忽略')
        else:
            log.warn(u'参数类型错误，必须是dict或str类型。已忽略')
    log.debug("请求地址:%s" % url)
    try:
        resp,content=h.request(url, headers={'cache-control':'no-cache','Content-Type':'application/x-www-form-urlencoded'})
        log.debug('<==>%d %s' %(resp.status, resp.reason))
        if resp.status==200 :
            return content.decode(constant.CHARSET)
    except Exception as e:
        log.error("程序遇到异常=>"+traceback.format_exc())

'''
模拟表单的post请求
'''
def do_post_form(url, params=None):
    #body=toUrlParams(params)
    body = urllib.urlencode(params)
    log.debug("请求地址:%s,请求参数%s" % (url, body))
    try:
        resp,content=h.request(url, 'POST', headers={'cache-control':'no-cache','Content-Type':'application/x-www-form-urlencoded'}, body=body)
        log.debug('<==>%d %s' %(resp.status, resp.reason))
        if(resp['status']=='200'):
            return content.decode(constant.CHARSET)
    except Exception as e:
        log.error("程序遇到异常=>"+traceback.format_exc())

'''
post请求
'''
def do_post_entity(url,body=None,content_type='text/html;charset=%s'% constant.CHARSET):
    log.debug("请求地址:%s,请求参数%s" % (url, body))
    headers={'cache-control':'no-cache',"Content-Type":content_type}
    try:
        resp,content=h.request(url, 'POST', headers=headers, body=body.encode(constant.CHARSET))
        log.debug('<==>%d %s' %(resp.status, resp.reason))
        if(resp['status']=='200'):
            return content.decode(constant.CHARSET)
    except Exception as e:
        log.error("程序遇到异常=>"+traceback.format_exc())

'''
http请求
'''
def request(url, method='GET', body=None, enc='urlencode'):
    method=method.upper()
    if method=='GET':
        return do_get(url, body)
    elif method=='POST':
        enc=enc.lower()
        content_type='text/html;charset=%s'% constant.CHARSET
        if 'json'==enc :
            content_type='applicaton/json;charset=%s' % constant.CHARSET
        elif 'urlencode'==enc:
            content_type='application/x-www-form-urlencoded;charset=%s' % constant.CHARSET
        elif 'xml'==enc:
            'text/xml;charset=%s'% constant.CHARSET
        return do_post_entity(url, body, content_type)
    else:
        log.warn('抱歉，目前仅支持GET/POST请求')

        

if __name__=='__main__':
    #录入停车场
    content=do_get("http://xbtest.parking24.cn:9090/reformer-alipay-carlife/AlipayCarParkInfoController/insertCarParkInfo", {'parkId':13})
    log.info('录入停车场返回:%s'%content)

    #车辆驶入
    intime="2016-09-13 09:40:00";
    car_number = "浙000000";
    parkId = 682504;
    s = '{"totalParkingNumer":300,"remainParkingNumber":159,"parkId":%d,"count":1,\
"data":[{"imgName":"temporary/parking_entrance/287946/201608/%s_20160825201707152.jpg",\
"inType":0,"channelName":"4号岗出入口(进场通道1)","parkingNo":"","inTime":"%s",\
"channelId":13,"reservation":0,"licensePlateNumber":"%s","remarks1":"","record_id":330557}]}'%(parkId,car_number,intime,car_number);
    #校验json格式是否正确
    log.info(json.loads(s))
    content = do_post_entity("http://xbtest.parking24.cn:9090/reformer-alipay-carlife/AlipayCarParkInfoController/carin", s, 'applicaton/json;charset=%s' % constant.CHARSET)
    log.info('车辆驶入返回:%s'%content)

    content=request(url="http://xbtest.parking24.cn:9090/reformer-alipay-carlife/AlipayCarParkInfoController/insertCarParkInfo", body={'parkId':13})
    log.info('===>:%s'%content)


'''
异常继承体系https://docs.python.org/3/library/exceptions.html#exception-hierarchy

'''


