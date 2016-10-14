#!/usr/bin/env python
# -*- coding:utf8 -*-

"""autotest URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.10/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from __future__ import unicode_literals
from django.conf.urls import url
from django.contrib import admin
from interapp import views

urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^lsinters.do$', views.lsinters),
    url(r'^execute.do$', views.execute),
    url(r'^executeAll.do$', views.executeAll),
    url(r'^lsresults.do$', views.lsresults),
    url(r'^delete.do$', views.delete),
    url(r'^batchdel.do$', views.batchdel),
    url(r'^saveinter.do$', views.saveinter),
    url(r'^editinter.do$', views.editinter),
    url(r'^saveServer.do$', views.saveServer),
    url(r'^templates/(.+)$', views.templates),
]
