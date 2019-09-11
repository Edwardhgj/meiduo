from django.shortcuts import render
from django.http import HttpResponse

from django.contrib.auth.hashers import check_password, make_password
from django.views import View
from utils.response_code import RET, error_map
from rest_framework.views import APIView
from rest_framework.response import Response
from apps.serializers import *
from datetime import datetime

# Create your views here.


# 展示登陆页
def login(request):
    return render(request, 'admin/login.html')

# 提交登陆
import json


class SubmitLogin(View):
    def post(self, request):  #反射

        mes = {}
        name = request.POST.get('name')
        passwd = request.POST.get('passwd')
        # print(name,passwd)

        if not all([name, passwd]):
            mes['code'] = RET.DATAERR
            mes['message'] = error_map[RET.DATAERR]
        else:
            # 查询name

            admin = Sadmin.objects.filter(username=name).first()
            print(admin.username)
            if admin:
                # 比较密码
                if check_password(passwd, admin.password):
                    # 登陆成功
                    request.session['admin_id'] = admin.id
                    mes['code'] = RET.OK
                    mes['message'] = error_map[RET.OK]
                else:
                    mes['code'] = RET.PWDERR
                    mes['message'] = error_map[RET.PWDERR]
            else:
                mes['code'] = RET.USERERR
                mes['message'] = error_map[RET.USERERR]
            print('sdfsdfssdf')
        return HttpResponse(json.dumps(mes))


# 注册
def reg(request):
    password = make_password('123')
    admin = Sadmin(username='admin', password=password, is_admin=True)
    admin.save()
    return HttpResponse('ok')


# 展示首页
def index(request):
    admin_id = request.session.get('admin_id')
    if admin_id:
        admin = Sadmin.objects.get(id=admin_id)
    return render(request, 'admin/index.html', locals())


# 展示分类页面
def showCate(request):
    return render(request, "admin/cate_list.html")


# 展示新闻页面
def showNews(request):
    return render(request, "admin/news_list.html")


#展示焦点图页面
def bannersCate(request):
    return render(request, "admin/point_list.html")

#展示标签页面
def tagCate(request):
    return render(request, "admin/tag_list.html")

#展示商品页面
def goodsCate(request):
    return render(request, "admin/goods_list.html")

#展示商品页面
def newsCate(request):
    return render(request, "admin/news_list.html")

#展示焦点图页面
def bannersCate(request):
    return render(request, "admin/point_list.html")

# 分类列表
class CateList(APIView):
    def get(self, request):
        cate = Cate.objects.all()
        c = CateModelSerializer(cate, many=True)
        mes = {}
        mes['code'] = RET.OK
        mes['cateList'] = c.data
        return Response(mes)



#标签列表
class TagList(APIView):
    def get(self, request):
        tags = Tags.objects.all()
        c = TagModelSerializer(tags, many=True)
        mes = {}
        mes['code'] = RET.OK
        mes['tagList'] = c.data
        return Response(mes)


# 商品列表
class GoodsList(APIView):
    def get(self, request):
        goods = Goods.objects.all()

        g = GoodsModelSerializer(goods, many=True)
        mes = {}
        mes['code'] = RET.OK
        mes['goodsList'] = g.data
        return Response(mes)

#新闻列表
class NewsList(APIView):
    def get(self, request):
        news = News.objects.all()

        n=NewsModelSerializer(news,many=True)
        mes = {}
        mes['code'] = RET.OK
        mes['newsList'] = n.data
        return Response(mes)


#焦点图列表
class BannersList(APIView):
    def get(self, request):
        banners = Banners.objects.all()

        n=BannersModelSerializer(banners,many=True)
        mes = {}
        mes['code'] = RET.OK
        mes['bannersList'] = n.data
        return Response(mes)





# 添加分类页面
def addCate(request):
    # 获取一级分类
    cate = Cate.objects.filter(pid=0).all()
    id=request.GET.get('id')
    try:
        #修改
        one_cate=Cate.objects.get(id=id)
        print(one_cate)
    except:
        id=""
    return render(request, "admin/add_cate.html", locals())



# 添加标签页面
def addTag(request):
    # print('sdf')
    cate_list = Cate.objects.all()
    id=request.GET.get('id')
    try:
        #修改
        one_tag=Tags.objects.get(id=id)
    except:
        id=""
    return render(request, "admin/add_tag.html", locals())


# 添加商品页面
def addGoods(request):
    # print('ceshi')
    # 获取所有商品
    goods = Goods.objects.all()
    cates = Cate.objects.all()
    tag_list=Tags.objects.all()
    id=request.GET.get('id')
    print(id)
    try:
        one_goods=Goods.objects.get(id=id)
        # print(one_goods)
    except:
        id=""
    return render(request, "admin/add_goods.html", locals())


# 添加商品页面
def addNews(request):
    # print('ceshi')
    # 获取所有商品
    news = News.objects.all()
    #修改时需要传id
    id=request.GET.get('id')
    print(id)
    try:
        one_news=News.objects.get(id=id)
        # print(one_goods)
    except:
        id=""
    return render(request, "admin/add_news.html", locals())



# 添加焦点图页面
def addBanners(request):
    # print('ceshi')
    # 获取所有商品
    banners = Banners.objects.all()
    #修改时需要传id
    id=request.GET.get('id')
    print(id)
    try:
        one_banner=Banners.objects.get(id=id)
        # print(one_goods)
    except:
        id=""
    return render(request, "admin/add_banners.html", locals())




from day01.settings import UPLOADFILES
import os


# 上传图片方法
def upload_img(img):
    if img:
        f = open(os.path.join(UPLOADFILES, '', img.name),'wb')
        for chunk in img.chunks():
            f.write(chunk)
        f.close()
        img=datetime.now().strftime("%Y-%m-%d-%H-%M-%S")+img.name
        return 'http://127.0.0.1:8000/static/upload/'+img
    return ' '


#富文本上传图片
def addnews_upload(request):
    files = request.FILES.get('file')
    path = upload_img(files)
    mes = {
        'path': path,
        'error': False
    }
    return HttpResponse(json.dumps(mes))



# 增加分类接口
class SubmitAddCate(APIView):
    def post(self, request):
        content = request.data

        print(content)
        # 上传图片
        img = request.FILES.get('img')
        path=upload_img(img)
        content['picture']=path
        try:
            pid=int(content['pid'])
        except:
            pid=0
        # 通过pic构造top_id，type
        if pid == 0:
            type = 1
            top_id = 0
        else:
            cate = Cate.objects.get(id=pid)
            type = cate.type + 1
            if cate.top_id==0:
                top_id = cate.id
            else:
                top_id = cate.top_id

        print(top_id,pid,type)
        content['type'] = type
        content['top_id'] = top_id
        try:
            id=int(content['id'])
        except:
            id=0

        if id>0:
            cc=Cate.objects.get(id=id)
            c=CateSerializer(cc,data=content)
            #修改

        else:
            c = CateSerializer(data=content)
        mes={}
        if c.is_valid():
            try:
                c.save()
                mes['code'] = RET.OK
            except:
                mes['code'] = RET.DATAERR
        else:
            print(c.errors)
            mes['code'] = RET.DATAERR
        return Response(mes)

#删除分类
def deleteCate(request):
    id=request.GET.get('id')
    Cate.objects.get(id=id).delete()
    return render(request, "admin/cate_list.html")






# 增加标签接口
class SubmitAddTag(APIView):
    def post(self, request):
        content = request.data

        print(content)
        try:
            id = int(content['id']) # 取出id
            print(id)
            print('di 到这了')
        except:
            id = 0


        if id > 0:
            dd = Tags.objects.get(id=id)
            d = TagSerializer(dd, data=content)
            # 修改

        else:
            d = TagSerializer(data=content)

        mes = {}

        if d.is_valid():
            try:
                d.save()
                mes['code'] = RET.OK

            except:
                mes['code'] = RET.DATAERR
        else:

            mes['code'] = RET.DATAERR

        return Response(mes)




#删除标签
def deleteTag(request):
    id=request.GET.get('id')
    Cate.objects.get(id=id).delete()
    return render(request, "admin/tag_list.html")



# 增加商品接口

class SubmitAddGoods(APIView):
    def post(self, request):
        # print('eerw')
        content = request.data
        print(content)
        print(content['id'])
        print(content['cid_id'])
        # 上传图片
        img = request.FILES.get('img')
        path=upload_img(img)
        content['picture']=path
        one_cate=Cate.objects.get(id=int(content['cid_id']))
        print(one_cate)
        content['top_id'] = one_cate.top_id

        try:
            print('测试代码')
            id=int(content['id'])
            print(id)
        except:
            id=0

        if id>0:
            # 修改商品
            instance = Goods.objects.get(id=id)
            c = GoodsSerializer(instance, data=content)

        else:
            c = GoodsSerializer(data=content)
        mes={}
        if c.is_valid():
            c.save()
            mes['code'] = RET.OK

        else:
            print(c.errors)
            mes['code'] = RET.DATAERR
        return Response(mes)

#删除商品
def deleteGoods(request):
    id=request.GET.get('id')
    Goods.objects.get(id=id).delete()
    return render(request, "admin/goods_list.html")


#添加新闻接口
class SubmitAddNews(APIView):
    def post(self,request):
        content=request.data
        print(content)
        try:
            id = int(content['id']) # 取出id

        except:
            id = 0


        if id > 0:
            print(id)
            nn = News.objects.get(id=id)
            d = NewsSerializer(nn, data=content)
            # 修改

        else:
            d = NewsSerializer(data=content)
        mes = {}
        if d.is_valid():
            try:
                d.save()
                mes['code'] = RET.OK

            except:
                mes['code'] = RET.DATAERR
        else:

            mes['code'] = RET.DATAERR

        return Response(mes)

#删除新闻
def deleteNews(request):
    id=request.GET.get('id')
    News.objects.get(id=id).delete()
    return render(request,"admin/news_list.html")


#删除焦点图
def deleteBanners(request):
    id=request.GET.get('id')
    Banners.objects.get(id=id).delete()
    return render(request,"admin/point_list.html")





#添加焦点图接口
class SubmitAddBanner(APIView):
    def post(self,request):
        content=request.data
        print(content)
        try:
            id = int(content['id']) # 取出id

        except:
            id = 0


        if id > 0:
            print(id)
            nn = Banners.objects.get(id=id)
            d = BannersSerializer(nn, data=content)
            # 修改

        else:
            d = BannersSerializer(data=content)
        mes = {}
        if d.is_valid():
            try:
                d.save()
                mes['code'] = RET.OK

            except:
                mes['code'] = RET.DATAERR
        else:

            mes['code'] = RET.DATAERR

        return Response(mes)



def user_count(request):

    return render(request,'admin/user_count.html')




