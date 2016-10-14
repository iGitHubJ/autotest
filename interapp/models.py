# -*- coding:utf-8 -*-
"""
模型：
    @author: 898596025@qq.com
    @license: http://www.apache.org/licenses/
    @change: 
    @copyright: 版权所有
    @since: 1.0
    @version: 1.0
"""
from __future__ import unicode_literals
from django.db import models
import datetime
from django.template.defaultfilters import default

class AuthGroup(models.Model):
    id = models.IntegerField(primary_key=True)  # AutoField?
    name = models.CharField(unique=True, max_length=80)

    class Meta:
        managed = False
        db_table = 'auth_group'


class AuthGroupPermissions(models.Model):
    id = models.IntegerField(primary_key=True)  # AutoField?
    group = models.ForeignKey(AuthGroup, models.DO_NOTHING)
    permission = models.ForeignKey('AuthPermission', models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'auth_group_permissions'
        unique_together = (('group', 'permission'),)


class AuthPermission(models.Model):
    id = models.IntegerField(primary_key=True)  # AutoField?
    content_type = models.ForeignKey('DjangoContentType', models.DO_NOTHING)
    codename = models.CharField(max_length=100)
    name = models.CharField(max_length=255)

    class Meta:
        managed = False
        db_table = 'auth_permission'
        unique_together = (('content_type', 'codename'),)


class AuthUser(models.Model):
    id = models.IntegerField(primary_key=True)  # AutoField?
    password = models.CharField(max_length=128)
    last_login = models.DateTimeField(blank=True, null=True)
    is_superuser = models.BooleanField()
    first_name = models.CharField(max_length=30)
    last_name = models.CharField(max_length=30)
    email = models.CharField(max_length=254)
    is_staff = models.BooleanField()
    is_active = models.BooleanField()
    date_joined = models.DateTimeField()
    username = models.CharField(unique=True, max_length=150)

    class Meta:
        managed = False
        db_table = 'auth_user'


class AuthUserGroups(models.Model):
    id = models.IntegerField(primary_key=True)  # AutoField?
    user = models.ForeignKey(AuthUser, models.DO_NOTHING)
    group = models.ForeignKey(AuthGroup, models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'auth_user_groups'
        unique_together = (('user', 'group'),)


class AuthUserUserPermissions(models.Model):
    id = models.IntegerField(primary_key=True)  # AutoField?
    user = models.ForeignKey(AuthUser, models.DO_NOTHING)
    permission = models.ForeignKey(AuthPermission, models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'auth_user_user_permissions'
        unique_together = (('user', 'permission'),)


class DjangoAdminLog(models.Model):
    id = models.IntegerField(primary_key=True)  # AutoField?
    object_id = models.TextField(blank=True, null=True)
    object_repr = models.CharField(max_length=200)
    action_flag = models.PositiveSmallIntegerField()
    change_message = models.TextField()
    content_type = models.ForeignKey('DjangoContentType', models.DO_NOTHING, blank=True, null=True)
    user = models.ForeignKey(AuthUser, models.DO_NOTHING)
    action_time = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'django_admin_log'


class DjangoContentType(models.Model):
    id = models.IntegerField(primary_key=True)  # AutoField?
    app_label = models.CharField(max_length=100)
    model = models.CharField(max_length=100)

    class Meta:
        managed = False
        db_table = 'django_content_type'
        unique_together = (('app_label', 'model'),)


class DjangoMigrations(models.Model):
    id = models.IntegerField(primary_key=True)  # AutoField?
    app = models.CharField(max_length=255)
    name = models.CharField(max_length=255)
    applied = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'django_migrations'


class DjangoSession(models.Model):
    session_key = models.CharField(primary_key=True, max_length=40)
    session_data = models.TextField()
    expire_date = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'django_session'


class Inter(models.Model):
    """
    接口地址
    """
    id = models.AutoField(primary_key=True)
    service = models.CharField(max_length=100)
    path = models.CharField(max_length=100)
    method = models.CharField(max_length=20, default='POST', blank=True, null=True)
    enc = models.CharField(max_length=50, default='json', blank=True, null=True)
    input = models.TextField(blank=True, null=True)
    output = models.TextField(blank=True, null=True)
    comment = models.CharField(blank=True, null=True, max_length=100)
    createtime = models.DateTimeField(auto_now=True)
    
    class Meta:
        managed = False
        db_table = 'inter'
        get_latest_by = 'createtime'
        unique_together = (('service', 'path', 'input'),)
        
    def __repr__(self):
        return '[id:%s,service:%s,path:%s,method:%s,enc:%s,input:%s,output:%s,comment:%s]' % (self.id, self.service, self.path, self.method, self.enc, self.input, self.output, self.comment)
    
    __str__ = __repr__
        


class Server(models.Model):
    """
    服务器地址
    """
    id = models.AutoField(primary_key=True)  # AutoField?
    name = models.CharField(unique=True, max_length=100)
    comment = models.CharField(blank=True, null=True, max_length=100)
    createtime = models.DateTimeField(auto_now=True)
    
    class Meta:
        managed = False
        db_table = 'server'
        get_latest_by = 'createtime'
    def __repr__(self):
        return '[id:%s,name:%s,comment:%s]' % (self.id, self.name, self.comment)
    
    __str__ = __repr__
        

class Result(models.Model):
    """
    调用结果
    """
    id = models.AutoField(primary_key=True)  # AutoField?
    inter = models.ForeignKey(Inter, models.DO_NOTHING)
    server = models.ForeignKey(Server, models.DO_NOTHING)
#     inter_id = models.IntegerField()
#     server_id = models.IntegerField()
    req = models.TextField()
    resp = models.TextField(blank=True, null=True) 
    result = models.BooleanField()
    spend = models.IntegerField(blank=True, null=True)
    createtime = models.DateTimeField(auto_now=True)

    class Meta:
        managed = False
        db_table = 'result'
        get_latest_by = 'createtime'
        
    def __repr__(self):
        return '[id:%s,inter:%s,server:%s,req:%s,resp:%s,result:%s,spend:%d]' % (self.id, self.inter, self.server, self.req, self.resp, self.result, self.spend)
    
    __str__ = __repr__
