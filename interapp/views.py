# -*- coding:utf-8 -*-
from __future__ import unicode_literals
from django.http import HttpResponse
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt 
import sys, time, json
import traceback, logging
from utils import constant
from utils.xml_util import parse
from interapp import business
from utils import logger
from interapp import models
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

def templates(request, path):
    return render(request, path);

def lsinters(request):
    """lsinters接口 列出配置文件中所有的测试接口"""
    (servers, inters) = business.listServersAndInters()
    ctx = {"servers":servers, "inters":inters}
    return render(request, 'inters.html', ctx)

@csrf_exempt
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
        log.error("程序遇到异常=>" + traceback.format_exc())
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
    serverids = interids = ""
    if request.method == "GET":
        serverids = request.GET.get("serverid").strip()
        interids = request.GET.get("interid").strip()
    elif request.method == "POST":
        serverids = request.POST.get("serverid").strip()
        interids = request.POST.get("interid").strip()
    else:
        res["code"] = 500
        res["msg"] = "请使用GET/POST请求"
        return HttpResponse(json.dumps(res), content_type="application/json")
#         attrs=dir(request)
#         for attr in attrs:
#             print(attr, '==>', getattr(request, attr));
    log.debug(interids)
    log.debug(type(interids))
    try:
        serverIds = json.loads(serverids)
        interIds = json.loads(interids)
        business.runAndSave(serverIds, interIds)
        res["code"] = 200
        res["msg"] = "success"
    except Exception as e:
        res["code"] = 500
        res["msg"] = e.message
        log.error("程序遇到异常=>" + traceback.format_exc())
    return HttpResponse(json.dumps(res), content_type="application/json")


def lsresults(request):
    """执行测试脚本"""
    ctx = {}
    try:
        results = business.listResults()
        ctx["results"] = results
        ctx["msg"] = "success"
    except Exception as e:
        ctx["code"] = 500
        ctx["msg"] = e.message
        log.error("程序遇到异常=>" + traceback.format_exc())
#     log.info("ctx:" + str(ctx))
    return render(request, 'results.html', ctx)

@csrf_exempt
def delete(request):
    tag = ID = None
    ctx = {"code":500}
    if request.method == "GET":
        tag = request.GET.get("tag").strip()
        ID = request.GET.get("id").strip()
    elif request.method == "POST":
        tag = request.POST.get("tag").strip()
        ID = request.POST.get("id").strip()
    try:
        if business.delete(tag, (int)(ID)):
            log.debug("删除成功")
            ctx["code"] = 200
            ctx["msg"] = "success"
    except Exception as e:
        ctx["msg"] = e.message
        log.error("程序遇到异常=>" + traceback.format_exc())
    return HttpResponse(json.dumps(ctx), content_type="application/json")

@csrf_exempt
def batchdel(request):
    tag = ids = None
    ctx = {"code":500}
    if request.method == "GET":
        tag = request.GET.get("tag")
        ids = request.GET.get("ids").strip()
    elif request.method == "POST":
        tag = request.POST.get("tag").strip()
        ids = request.POST.get("ids").strip()
    try:
        ids = json.loads(ids)
        if business.batchdel(tag, ids):
            log.debug("删除成功")
            ctx["code"] = 200
            ctx["msg"] = "success"
    except Exception as e:
        ctx["msg"] = e.message
        log.error("程序遇到异常=>" + traceback.format_exc())
    return HttpResponse(json.dumps(ctx), content_type="application/json")

def editinter(request):
    ID = None
    if request.method == "GET":
        ID = request.GET.get("id")
    elif request.method == "POST":
        ID = request.POST.get("id")
    inter = business.findInterById((int)(ID));
    if inter:
        ctx = {"id":ID, "service":inter.service, "path":inter.path, "comment":inter.comment, "method":inter.method, "enc":inter.enc, "input":inter.input, "output":inter.output}
        ctx['optype'] = 'edit'
        return render(request, "saveinter.html", ctx)
    else:
        return HttpResponse(json.dumps({"code":500, "msg":"no data found"}), content_type="application/json")


def saveinter(request):
    ID = None
    if request.method == "GET":
        return HttpResponse(json.dumps({"code":405, "msg":"please use POST http method"}), content_type="application/json")
    elif request.method == "POST":
        log.debug(">>>>>"+json.dumps(request.POST))
        optype = request.POST.get("optype").strip()
        service = request.POST.get("service").strip()
        path = request.POST.get("path").strip()
        method = request.POST.get("method").strip()
        enc = request.POST.get("enc").strip()
        input = request.POST.get("input").strip()
        output = request.POST.get("output").strip()
        comment = request.POST.get("comment").strip()
        if optype == 'edit':
            ID = request.POST.get("id")
        try:
            if business.saveOrUpdateInter(models.Inter(id=ID, service=service, path=path, method=method, enc=enc, input=input, output=output, comment=comment)):
                log.debug("执行成功")
                return lsinters(request)
        except Exception as ex:#重复
            log.error("程序遇到异常=>" + traceback.format_exc())
            ctx={"errmsg":ex.message}
            return render(request, "error.html", ctx)
            

@csrf_exempt
def saveServer(request):
    name=None
    comment=None
    ctx = {"code":500}
    if request.method == "GET":
        name = request.GET.get("name").strip()
        comment = request.GET.get("comment").strip()
    elif request.method == "POST":
        name = request.POST.get("name").strip()
        comment = request.POST.get("comment").strip()
    try:
        if business.saveServer(models.Server(name=name, comment=comment)):
            log.debug("服务器添加成功")
            ctx["code"] = 200
            ctx["msg"] = "success"
    except Exception as e:
        ctx["msg"] = e.message
        log.error("程序遇到异常=>" + traceback.format_exc())
    return HttpResponse(json.dumps(ctx), content_type="application/json")

