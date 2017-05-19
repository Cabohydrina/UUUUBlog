#-*- coding:utf-8 -*-

from django.shortcuts import get_object_or_404, render
from django.http import *
from django.http import HttpResponse,HttpResponseRedirect
from django.core.urlresolvers import reverse
from django.views import generic
from django.shortcuts import render_to_response
from django.http import HttpResponse,HttpResponseRedirect
from django.core.paginator import Paginator,InvalidPage,EmptyPage,PageNotAnInteger
import time,datetime
from django.db.models import Q
from django.db import connection
from django.template import RequestContext



from django.contrib.auth.models import User
from django.views.generic.base import TemplateView
from django.contrib.auth.decorators import login_required

from UUBlog.models import Category, Article,Comment,Channel,Great,Relation
#zhou
from django import forms
from django.forms import ModelForm
from UUBlog.models import ContactForm
#zhou

import common
import modules
import utility

#关注
def focus(request,uid):
    uid=int(uid)
    #print uid
    userInfos=common.Users(request,uid)
    #print userInfos
    #print uid
    print userInfos["currentuser"].id
    #得到关注列表
    focusList=common.Relations(request,uid)
    starProfile=focusList["starList"]
    for starInfo in starProfile:
        print starInfo.nickname
   # guestBlog=userInfos["guestblog"]
    focusnum=Relation.objects.filter(fans_id=uid).count()
    fansnum=Relation.objects.filter(star_id=uid).count()

    myModules = ["profile", "hotarticlelist", "newarticlelist"]
    #myModules = ["profile"]
    moduleParams = {}
    for myModule in myModules:
        moduleParams.setdefault(myModule, {})
    moduleList = modules.GetModuleList(moduleParams)

    # 关注功能
    if userInfos["currentuser"]:
        print userInfos["currentuser"].id
        print uid
        try:
            focusInfo = Relation.objects.filter(star_id=uid, fans_id=userInfos["currentuser"].id)
        except:
            focusInfo = None

    if request.POST.has_key('focus'):
        relationInfo = Relation()
        relationInfo.star_id = uid
        relationInfo.fans_id = userInfos["currentuser"].id
        relationInfo.save()
        text = '/%d' % (uid)
        return HttpResponseRedirect(text)

    #取消关注
    if request.POST.has_key('nofocus'):
        Relation.objects.filter(star_id=uid, fans_id=userInfos["currentuser"].id).delete()
        text = '/%d' % (uid)
        return HttpResponseRedirect(text)
    #更新用户文章总数
    #guestBlog.todayviews+=1
    #guestBlog.totalviews+=1
    #guestBlog.save()
    #articleList=Article.objects.order_by("-createtime").filter(user_id=uid).filter(status=1)
    #print articleList



    return utility.my_render_to_response(request,"focusList.html",locals())

