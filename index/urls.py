"""day01 URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path,include,re_path
from index import views
from rest_framework_jwt.views import obtain_jwt_token
from rest_framework_jwt.settings import api_settings
from index.pay import page1,PaGe

urlpatterns = [
    # path('admin/', admin.site.urls),
    path('GetCateGoods/', views.GetCateGoods.as_view()),
    path('getGoods/', views.GetGoods.as_view()),
    path('getImageCode/', views.getImageCode),
    path('Reg/', views.Reg.as_view()),
    # re_path(r'jlogin/', obtain_jwt_token, name='jlogin'),
    path('login/',views.login.as_view()),
    path('addCart/',views.AddCart.as_view()),  #增加购物车
    path('commit_order/',views.Commit_order.as_view()), #提交订单
    path('create_order/',views.Create_order.as_view()), #创建订单
    path('cartlist/',views.Cartlist.as_view()),
    path('add_address/',views.Add_address.as_view()),
    path('getOrder/',views.GetOrder.as_view()),
    #传过来的数据内部直接处理好了
    path('getpayurl',page1),
    path('page1_',PaGe),
    path('finish_order/<str:name>',views.finish_order),
    path('sendmes/',views.sendmes)



]
