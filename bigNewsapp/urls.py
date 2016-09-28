from django.conf.urls import url
from bigNewsapp import views
from django.conf import settings

urlpatterns = [
    url(r'^$', views.index, name='login'),
    url(r'^uploadfile/$', views.fileUpload, name='uploadFile'),
    url(r'^test/$',views.test,name='test'),
]