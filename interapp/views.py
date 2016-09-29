# -*- coding:utf-8 -*-

from django.http import HttpResponse
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt 
import sys, time, json
import traceback, logging
from utils import constant
from utils.xml_util import parse
from interapp import business
from utils import logger
log = logger.get()

reload(sys) 
sys.setdefaultencoding(constant.CHARSET)


def hello(request):
    """ hello 演示接口 """
    print(request)
    context = {}
    context['hello'] = 'Hello World!'
    context['bool'] = True
    names = ['admin', 'anonymous', 'user']
    p1 = {"name":'haha', 'age':20}
    context['names'] = names
    context['p1'] = p1
    context['now'] = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime())
    return render(request, 'hello.html', context)

def lsinters(request):
    """lsinters接口 列出配置文件中所有的测试接口"""
    (servers, inters) = business.listServersAndInters()
    ctx = {"servers":servers, "inters":inters}
    return render(request, 'inters.html', ctx)

def executeAll(request):
    """执行测试脚本"""
    res = {}
    try:
        business.runAndSave()
        res["code"] = 200
        res["msg"] = "success"
    except Exception as e:
        res["code"] = 500
        res["msg"] = e.message
        log.error(u"程序遇到异常=>" + traceback.format_exc())
    return HttpResponse(json.dumps(res), content_type="application/json")

@csrf_exempt
def execute(request):
    """执行测试脚本"""
    ua = request.META.get('HTTP_USER_AGENT', 'unknown')
    '''
    get是request.GET.get('name','xxx')
    post是request.POST.get('name','xxx')
    获取多个值用getlist
     serverids=request.GET.getlist("checkname")
     request.body 获取post请求内容
    '''
    res = {}
    try:
        serverids=interids=""
        if request.method=="GET":
            serverids=request.GET.get("serverid")
            interids=request.GET.get("interid")
        elif request.method=="POST":
            serverids=request.POST.get("serverid")
            interids=request.POST.get("interid")
#         attrs=dir(request)
#         for attr in attrs:
#             print(attr, '==>', getattr(request, attr));
        log.debug(interids)
        log.debug(type(interids))
        serverIds = json.loads(serverids)
        interIds = json.loads(interids)
        business.runAndSave(serverIds, interIds)
        res["code"] = 200
        res["msg"] = "success"
    except Exception as e:
        res["code"] = 500
        res["msg"] = e.message
        log.error(u"程序遇到异常=>" + traceback.format_exc())
    return HttpResponse(json.dumps(res), content_type="application/json")


def lsresults(request):
    """执行测试脚本"""
    ctx = {}
    try:
        results = business.listResults()
        ctx["data"] = results
        ctx["msg"] = "success"
    except Exception as e:
        ctx["code"] = 500
        ctx["msg"] = e.message
        log.error(u"程序遇到异常=>" + traceback.format_exc())
    log.info("ctx:" + str(ctx))
    return render(request, 'results.html', ctx)


