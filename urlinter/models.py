#-*- coding:utf-8 -*-
from __future__ import unicode_literals

from django.db import models
import datetime

# Create your models here.
class Inter(models.Model):
    id = models.IntegerField(primary_key=True)
    addr = models.URLField()
    method = models.CharField(max_length = 20)
    enc = models.CharField(max_length = 20)
    inputs = models.CharField(max_length = 255,db_column='input')
    output = models.TextField()
    response = models.TextField()
    createtime = models.DateTimeField(default = datetime.datetime.now())
    result = models.BooleanField(default = False)
    spend = models.IntegerField()
    class Meta:
        db_table = 'inter'
        get_latest_by = 'createtime'
        
    def __repr__(self):
        return '[addr:%s,method:%s,input:%s,response:%s,output:%s,spend:%f]' %(self.addr,self.method,self.inputs,self.response,self.output,self.spend)
    
    __str__=__repr__
