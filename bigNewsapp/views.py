from django.shortcuts import render
from django.shortcuts import render_to_response
from django.http import HttpResponse
from django.http import HttpResponseRedirect
from .Class.forms import AddForm
from .Class.files import FileForm
from .Class.login import User
import qiniu
from qiniu import Auth, put_file, etag, urlsafe_base64_encode, put_data
import qiniu.config
from django.conf import settings
from django.core.files import File
from django.core.files.base import ContentFile
from django.core.files.uploadedfile import InMemoryUploadedFile
from django.db.models import FileField
import json
import time
from django.contrib.auth import authenticate, login
import os


# Create your views here.
# coding:utf-8


def index(request):
    if request.method == 'POST':
        uf = User(request.POST)
        if uf.is_valid():
            # 获取表单用户密码
            username = uf.cleaned_data['username']
            password = uf.cleaned_data['password']
            # 获取的表单数据与数据库进行比较
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                return HttpResponseRedirect('/filesystem/uploadfile/')
            else:
                return HttpResponseRedirect('/filesystem/')
    else:
        uf = User()
    return render_to_response('login.html', {'uf': uf})


def fileUpload(request):
    if request.user.is_authenticated():  # 判断用户是否已登录
        user = request.user  # 获取已登录的用户
    else:
        return HttpResponseRedirect('/filesystem/')
    q = Auth(settings.QINIU_ACCESS_KEY, settings.QINIU_SECRET_KEY)
    bucket_name = settings.QINIU_BUCKET_DEFAULT
    if request.method == 'POST':
        form = FileForm(request.POST)
        if form.is_valid():
            localfile=form.cleaned_data['key']
            key=os.path.basename(localfile)
            token = q.upload_token(bucket_name, key, 3600)
            ret, info = put_file(token, key, localfile)
            print(ret, info)
            assert ret['key'] == key
            assert ret['hash'] == etag(localfile)
            return render(request, 'result.html', {'result': key, 'STRING': 'success'})

    else:
        form = FileForm()
    return render(request, 'upload.html', {'FILEPATH': form})


def fildDownload(request):
    q = Auth(settings.QINIU_ACCESS_KEY, settings.QINIU_SECRET_KEY)
    bucket_name = settings.QINIU_BUCKET_DEFAULT


def test(request):
    q = Auth(settings.QINIU_ACCESS_KEY, settings.QINIU_SECRET_KEY)
    bucket_name = settings.QINIU_BUCKET_DEFAULT
    if request.method == 'POST':
        file = request.POST.get('myPath')
        key = os.path.basename(file)
        print(key)
        localfile = file
        print(localfile)
        token = q.upload_token(bucket_name, key, 3600)
        ret, info = put_file(token, key, localfile)
        print(ret, info)
        assert ret['key'] == key
        assert ret['hash'] == etag(localfile)
        return render(request, 'result.html', {'result': key, 'STRING': 'success'})
    else:
        return render(request, 'test.html')
