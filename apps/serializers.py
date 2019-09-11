from rest_framework import serializers
from .models import *
from django.contrib.auth.hashers import check_password,make_password


# 获取分类列表
class CateModelSerializer(serializers.ModelSerializer):  # 序列化 python 变json
    class Meta:
        model = Cate
        fields = '__all__'


# 添加分类

class CateSerializer(serializers.Serializer):  # 反序列化 json 变 python语句
    name = serializers.CharField(max_length=50)  # 分类名称
    pid = serializers.IntegerField(default=0)  # 顶级分类默认0
    type = serializers.IntegerField(default=1)  # 标示几级分类
    picture = serializers.CharField(max_length=255, default='')  # 图片名称
    top_id = serializers.IntegerField(default=1)  #
    is_recommend = serializers.IntegerField(default=1)  # 是否首页推荐(1:是，0：否)

    # 添加
    def create(self, data):  # data为前台页面传递的参数
        cate = Cate.objects.create(**data)
        return cate

    # 修改参数
    def update(self, instance, validated_data):
        instance.name = validated_data['name']
        instance.pid = validated_data['pid']
        instance.type = validated_data['type']
        instance.top_id = validated_data['top_id']
        instance.is_recommend = validated_data['is_recommend']
        instance.picture = validated_data['picture']
        instance.save()
        return instance


# 添加标签


# 获取标签列表
class TagModelSerializer(serializers.ModelSerializer):  # 序列化 python 变json
    class Meta:
        model = Tags
        fields = '__all__'


class TagSerializer(serializers.Serializer):  # 反序列化 json 变 python语句
    name = serializers.CharField(max_length=50)  # 分类名称
    cid = serializers.IntegerField()  # 外键关联分类表
    is_recommend = serializers.IntegerField(default=1)  # 是否首页推荐(1:是，0：否)

    # 添加
    def create(self, data):  # data为前台页面传递的参数
        cid = int(data['cid'])
        one_tag = Cate.objects.get(id=cid)
        tag = Tags.objects.create(name=data['name'], cid=one_tag, is_recommend=data['is_recommend'])
        return tag

    # 修改参数
    def update(self, instance, validated_data):
        instance.name = validated_data['name']
        instance.cid_id = int(validated_data.get('cid'))
        instance.is_recommend = validated_data.get('is_recommend')
        instance.save()
        return instance


# 获取商品列表
class GoodsModelSerializer(serializers.ModelSerializer):  # 序列化 python 变json
    class Meta:
        model = Goods
        fields = '__all__'


# 序列化商品

class GoodsSerializer(serializers.Serializer):  # 反序列化 json 变 python语句
    name = serializers.CharField(max_length=255)  # 商品名
    describe = serializers.CharField()  # 描述
    content = serializers.CharField()  # 内容
    picture = serializers.CharField(max_length=255)  # 图片名称
    storage = serializers.IntegerField(default=0)  # 库存
    lock_storage = serializers.IntegerField(default=0)  # 锁定库存
    price = serializers.DecimalField(max_digits=10, decimal_places=2)
    is_recommend = serializers.IntegerField(default=1)  # 推荐默认为1，不推荐为0
    cid_id = serializers.IntegerField()  # 外键关联分类id
    top_id = serializers.IntegerField()  # 顶级分类
    tag_id_id = serializers.IntegerField()  # 外键关联标签id
    t_comment = serializers.IntegerField(default=0)  # 总评论数
    sales = serializers.IntegerField(default=0)  # 销量

    # 添加商品
    def create(self, data):  # data为前台页面传递的参数
        goods=Goods.objects.create(**data)
        return goods

    # 修改商品
    def update(self, instance, validated_data):
        instance.name = validated_data.get('name', instance.name)
        instance.describe = validated_data.get('describe', instance.describe)
        instance.content = validated_data.get('content', instance.content)
        instance.picture = validated_data.get('picture', instance.picture)
        instance.storage = validated_data.get('storage', instance.storage)
        instance.lock_storage = validated_data.get('lock_storage', instance.lock_storage)
        instance.price = validated_data.get('price', instance.price)
        instance.is_recommend = validated_data.get('is_recommend', instance.is_recommend)
        instance.cid_id = validated_data.get('cid_id', instance.cid_id)
        instance.top_id = validated_data.get('top_id', instance.top_id)
        instance.tag_id_id = validated_data.get('tag_id_id', instance.tag_id_id)
        instance.t_comment = validated_data.get('t_comment', instance.t_comment)
        instance.sales = validated_data.get('sales', instance.sales)
        instance.save()
        return instance




# 获取新闻列表
class NewsModelSerializer(serializers.ModelSerializer):  # 序列化 python 变json
    class Meta:
        model = News
        fields = '__all__'

#反序列化将页面
class NewsSerializer(serializers.Serializer):  # 反序列化 json 变 python语句（页面->后端）
    title = serializers.CharField(max_length=50)  # 分类名称
    content = serializers.CharField(default='')  # 外键关联分类表
    is_show = serializers.IntegerField(default=1)  # 是否首页推荐(1:是，0：否)


    # 添加新闻 序列化 传给前台  （此处如果忘写则不会报错）
    def create(self, data):  # data为前台页面传递的参数
        news=News.objects.create(**data)
        return news

    def update(self, instance, validated_data):
        instance.title=validated_data.get('title',instance.title)
        instance.content=validated_data.get('content',instance.content)
        instance.is_show=validated_data.get('is_show',instance.is_show)
        instance.save()
        return instance




# 获取焦点图列表
class BannersModelSerializer(serializers.ModelSerializer):  # 序列化 python 变json
    class Meta:
        model = Banners
        fields = '__all__'


class BannersSerializer(serializers.Serializer):
    name=serializers.CharField()
    is_show=serializers.IntegerField()
    type=serializers.IntegerField()
    sort=serializers.IntegerField()


# 添加焦点图 序列化 传给前台  （此处如果忘写则不会报错）
    def create(self, data):  # data为前台页面传递的参数
        banners=Banners.objects.create(**data)
        return banners

    def update(self, instance, validated_data):
        instance.name=validated_data.get('name',instance.name)
        instance.is_show=validated_data.get('is_show',instance.is_show)
        instance.type=validated_data.get('type',instance.type)
        instance.sort=validated_data.get('sort',instance.sort)
        instance.save()
        return instance




#添加user 反序列化

class UsersSerializer(serializers.Serializer):
    username = serializers.CharField()  # 用户名
    password = serializers.CharField()  # 密码
    email = models.CharField()  # 邮件
    token = models.CharField()  # 图片

    def create(self, data):
        data['password'] = make_password(data['password'])
        users=User.objects.create(**data)
        return users




#购物车序列化
class CartModelSerializer(serializers.ModelSerializer):
    class Meta:
        model=Cart
        fields="__all__"

#地址序列化
class AddressModelSerializer(serializers.ModelSerializer):
    class Meta:
        model=Address
        fields="__all__"
