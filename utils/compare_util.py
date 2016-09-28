# -*- coding:utf8 -*-

import json
import traceback
import sys
from utils import constant
from utils import logger
log = logger.get()

reload(sys) 
sys.setdefaultencoding(constant.CHARSET)
"""
比较连个dict的key是否相同，松散、模糊对比
"""
def loosecmp(a, b):
    if a==b:
        return True
    if type(a) != type(b):
        return False
    if isinstance(a,str) or isinstance(a,unicode):
        a=json.loads(a)
        b=json.loads(b)
    if len(a) != len(b):
        return False
    if isinstance(a,list) or isinstance(a,tuple):
        a=a[0]
        b=b[0]
    for k in a.keys():
        if b.get(k) is None:
            return False
    for k in b.keys():
        if a.get(k) is None:
            return False
    return True

'''
严格对比
'''
def strictcmp(a, b):
    if loosecmp(a, b):
        if isinstance(a,str) or isinstance(a,unicode):
            a=json.loads(a)
            b=json.loads(b)
        if len(a) != len(b):
            return False
        if isinstance(a,list) or isinstance(a,tuple):
            a=a[0]
            b=b[0]
        for k in a.keys():
            if a.get(k) != b.get(k):
                return False
        return True
    else:
        return False

    
'''
dict
dict[key] if key is not exists in dict, return KeyError
dict.get(key) if key is not exists in dict, return None
'''
if __name__ == '__main__':
    a = {'username':'tcp','id':1,'addr':{'prov':'zj','city':'hz'}}
    b = {'username':'zkn'}
    c = {'username':'4.8.1'}
    log.info( loosecmp(a,b))
    log.info( loosecmp(b,c))
    log.info( strictcmp(a,b))
    log.info( strictcmp(b,c))


    
