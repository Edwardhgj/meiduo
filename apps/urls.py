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
from django.urls import path
from apps import views

app_name = 'apps'

urlpatterns = [
    path('login/', views.login),

    path('reg/', views.reg),

    path('index/', views.index),

    path('showCate/', views.showCate),

    path('showNews/', views.showNews),

    path('bannersCate/', views.bannersCate),

    path('tagCate/', views.tagCate),

    path('goodsCate/', views.goodsCate),

    path('newsCate/', views.newsCate),

    path('SubmitLogin/', views.SubmitLogin.as_view()),


    path('CateList/', views.CateList.as_view()),

    path('TagList/', views.TagList.as_view()),

    path('GoodsList/', views.GoodsList.as_view()),

    path('NewsList/', views.NewsList.as_view()),

    path('BannersList/', views.BannersList.as_view()),

    path('addCate/', views.addCate),

    path('addTag/', views.addTag),

    path('addGoods/', views.addGoods),

    path('addNews/', views.addNews),

    path('addBanners/', views.addBanners),

    path('deleteCate/', views.deleteCate),

    path('deleteTag/', views.deleteTag),

    path('deleteNews/', views.deleteNews),

    path('deleteBanners/', views.deleteBanners),

    path('submit_addCate/', views.SubmitAddCate.as_view()),

    path('submit_addTag/', views.SubmitAddTag.as_view()),

    path('submit_addGoods/', views.SubmitAddGoods.as_view()),

    path('submit_addNews/', views.SubmitAddNews.as_view()),

    path('submit_addBanner/', views.SubmitAddBanner.as_view()),


    path('user_count/', views.user_count),
]
