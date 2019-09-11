from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from apps.models import *
from apps.serializers import *
from index.serializers import *
from django.http import HttpResponse
# Create your views here.
from utils.response_code import RET,error_map

#获取一级列表下的所有数据，标签和商品

class GetCateGoods(APIView):
    def get(self,request):
        cate=Cate.objects.filter(pid=0)
        clist=[]
        for i in cate:
            dict={}
            dict['name']=i.name
            dict['id']=i.id
            dict['image']=i.picture
        #获取一级下面的二级
            cate2=Cate.objects.filter(pid=i.id).all()
            c2=CateModelSerializer(cate2,many=True)
            dict['sublist']=c2.data
            # print(c2.data)
        #获取一级下面对应的tag标签
            tags=Tags.objects.filter(cid=i.id).all()
            t=TagModelSerializer(tags,many=True)
            dict['tags']=t.data
        #获取一级下面的所有商品
            goods=Goods.objects.filter(cid=i.id).all()
            g=GoodsModelSerializer(goods,many=True)
            clist.append(dict)
            mes={}
            mes['code']=200
            mes['catelist']=clist
            mes['goods']=g.data

            return Response(mes)


from utils.captcha.captcha import captcha
#获取图片验证码
def getImageCode(request):
    name,text,image=captcha.generate_captcha()
    #存入session，用户提交时候进行对比
    request.session['image_code']=text

    return HttpResponse(image,'image/jpg')


from day01 import settings
import uuid
from django.core.mail import EmailMessage

# from .task import sendmail
#注册接口
#从前台传过来的json数据，通过data=request.data  接受，然后构造没有的数据 token ，最后放入反序列化，将j->p, 用 s
class Reg(APIView):
    def post(self,request):
        mes={}
        data=request.data.copy()
        print(data)
        #获取用户输入，
        # 验证用户名，密码，验证码是否填完整
        # 用户是否唯一，用唯一键
        #验证图片验证码是否一致
        #验证用户名密码是否输入正确

        #生成token值验证
        token=str(uuid.uuid1())
        data['token']=token
        u = UsersSerializer(data=data)
        # print(u)
        # 验证是否有效
        if u.is_valid():
            # 入库
            u.save()
            # 发邮件
            email=data['email']
            print(email)
            esend = EmailMessage('欢迎注册', '点击此链接<a href="http://localhost:8000/valid_email?code=' + token + '">验证</a>',settings.DEFAULT_FROM_EMAIL, [email])
            esend.content_subtype = 'html'
            esend.send()

            mes['code']=200
            mes['message']='ok'
            print(mes)

        else:
            print(u.errors)
            mes['code'] = 10010
            mes['message'] = 'ok'
            #返回
        return HttpResponse(mes)

from utils.response_code import error_map,RET
from rest_framework_jwt.settings import api_settings


class login(APIView):
    def post(self,request):
        mes={}
        data=request.data.copy()
        username=data['username']
        password=data['password']
        print(username,password)
        one_user=User.objects.filter(username=username).first()

        if not all([username,password]):
            mes['code']=RET.DATAERR
            mes['message'] =error_map[RET.DATAERR]
            return Response(mes)

        if  one_user.check_password(password):

            # 补充生成记录登录状态的token
            jwt_payload_handler = api_settings.JWT_PAYLOAD_HANDLER
            jwt_encode_handler = api_settings.JWT_ENCODE_HANDLER
            payload = jwt_payload_handler(one_user)
            token = jwt_encode_handler(payload)
            one_user.token = token


            dict={}
            dict['user_id']=one_user.id
            dict['username']=one_user.username
            dict['token']=one_user.token

            mes['code']=200
            mes['one_user']=dict
            print('测试一')
            return Response(mes)
        else:
            mes['code'] = 10020
            mes['message'] = '密码错误'
            print('测试2')
        return Response(mes)



class AddCart(APIView):
    def post(self,request):
        mes={}
        data=request.data.copy()  #此处要复制,不然会报错
        # print(data)
        #查询购物车是否存在
        cart=Cart.objects.filter(user_id=data['user_id'],good_id=data['good_id']).first()
        print(cart)
        #存在更新数量
        if cart:
            print('测试1')
            cart.count=data['count']  #一个更新不需要再反序列化了
            cart.save()
            mes['code'] = 200
        else:
            mes['code']=10010

            #不存在根据查询商品信息
            good=Goods.objects.get(id=data['good_id'])
            print(good.name)
            #组装添加购物车
            data['good_name']=good.name
            data['picture']=good.picture
            data['price']=good.price
            #加入购物车
            c=CartSerializer(data=data)
            if c.is_valid():
                c.save()
                mes['code'] = 200
                mes['message'] = 'ok'
            else:
                mes['code'] = RET.DATAERR
                mes['message'] = error_map[RET.DATAERR]
                print(c.errors)
            #返回结果

        return Response(mes)

#确认订单
class Commit_order(APIView):
    def post(self,request):
        mes = {}
        #获取数据
        try:
            data = request.data
            print(data)
            ids = data['ids'].split(',')
            print(ids)
            # 在更新数据之前需要把is_checked的数据更新为0,不然会出现重复选中的情况
            cart = Cart.objects.filter(user_id=data['user_id']).update(is_checked=0)
            # 筛选数据
            cart = Cart.objects.filter(user_id=data['user_id'], id__in=ids).update(is_checked=1)
            mes['code'] = 200
            mes['message'] = '成功'
        except:
            mes['code']=10010
            mes['message']='异常'
        return Response(mes)



import uuid,datetime,time
from django.db import transaction
#生成订单详情 和订单
class Create_order(APIView):
    @transaction.atomic
    def post(self, request):
        mes={}
        #获取用户输入
        data=request.data
        user_id=data['user_id']
        address_id=data['address_id']
        pay_type=data['pay_type']
        tmoney=data['tmoney']
        print(user_id, address_id, pay_type,tmoney)
        #生成唯一订单号

        #  order_code
        # code = str(time.strftime('%Y%m%d%H%M%S', time.localtime(time.time())))+ str(time.time()).replace('.', '')[-7:]
        # print(code)
        order_sn = str(uuid.uuid1())
        #建立事务开始起点
        sid=transaction.savepoint()
        #生成订单
        #根据 address_id 表里去查询地址详细信息
        address = Address.objects.filter(id=address_id).first()
        print(address)
        order=Orders(order_sn=order_sn,tmoney=float(tmoney),user_id=user_id,adress=address,status=0,pay_type=pay_type)
        order.save()
        print('通过')
        #订单详情
        cart=Cart.objects.filter(user_id=user_id,is_checked=1).all()
        for i in cart:
            #判断库存
            goods=Goods.objects.get(id=i.good_id)
            if i.count>goods.storage-goods.lock_storage:
                transaction.savepoint_rollback(sid)

            #构造详情表数据,进行添加id
            order_detail=Order_detail(order_sn=order,user_id=user_id,name=i.good_name,price=i.price,count=i.count,image=i.picture)
            order_detail.save()

            #更新商品表中锁定库存
            print("通过2")

            goods.lock_storage += i.count
            goods.save()

            print('通过3')
        #清空购物车
        Cart.objects.filter(is_checked=1).delete()
        print('通过4')
        transaction.savepoint_commit(sid)
        mes['code']=200
        return Response(mes)




#获取对应id的商品

class GetGoods(APIView):
    def get(self,request):
        mes={}
        id=request.GET.get('id')
        good=Goods.objects.filter(id=id).first()
        g=GoodsModelSerializer(good)
        print(g.data)
        mes['code']=200
        mes['goods']=g.data
        return Response(mes)



class Cartlist(APIView):
    def get(self,request):
        mes={}
        user_id=request.GET.get('user_id')
        c=Cart.objects.filter(user_id=user_id).all()
        cartlist=CartModelSerializer(c,many=True)
        mes['code']=200
        mes['cartlist']=cartlist.data
        return Response(mes)

    def post(self,request):
        mes={}
        data=request.data
        # print(data)
        user_id=data['user_id']
        c = Cart.objects.filter(user_id=user_id,is_checked=1).all()
        a = Address.objects.filter(user_id=user_id).first()
        cartlist = CartModelSerializer(c, many=True)
        addresses = AddressModelSerializer(a)

        print(addresses.data)
        mes['code'] = 200
        mes['cartlist'] = cartlist.data
        mes['addresses'] = addresses.data
        return Response(mes)


class Add_address(APIView):
    def post(self,request):
        mes={}
        data=request.data
        print(data)
        a=AddressSerializer(data=data)
        if a.is_valid():
            a.save()
        mes['code']=200
        mes['message']=a.data
        return Response(mes)



class GetOrder(APIView):
    def get(self,request):
        mes={}
        user_id=request.GET.get('user_id')
        o=Orders.objects.filter(user_id=user_id).all()

        orderlist=OrderModelSerializer(o,many=True)

        mes['code']=200
        mes['orderlist']=orderlist.data
        return Response(mes)








import json

from dwebsocket.decorators import accept_websocket

conn={}

@accept_websocket
def finish_order(request,name):
    if request.is_websocket:
        conn[name]=request.websocket

    for message in request.websocket:
        pass


def sendmes(request):
    #支付宝已经支付成功,回调接口
    #给商户发提醒
    name='admin'
    mes=json.dumps({'title':'您有新的订单了'},ensure_ascii=False).encode('utf-8')
    conn[name].send(mes)
    return HttpResponse('ok')