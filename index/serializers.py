from rest_framework import serializers    #直接引入 必须记住
from apps.models import Cart,Address,Order_detail,Orders


class CartSerializer(serializers.Serializer):
    user_id = serializers.IntegerField()
    good_id = serializers.IntegerField()
    price = serializers.IntegerField()
    count = serializers.IntegerField()
    picture = serializers.CharField()
    good_name = serializers.CharField()

    def create(self,data):
        return  Cart.objects.create(**data)


class GoodSerializer(serializers.Serializer):
    name = serializers.CharField()  # 商品名
    describe = serializers.CharField()  # 描述
    content = serializers.CharField()  # 内容
    picture = serializers.CharField()  # 图片名称
    storage = serializers.IntegerField()  # 库存
    lock_storage = serializers.IntegerField()  # 锁定库存
    price = serializers.IntegerField()
    is_recommend = serializers.IntegerField()  # 推荐默认为1，不推荐为0
    cid = serializers.IntegerField() # 外键关联分类id
    top_id = serializers.IntegerField()  # 顶级分类
    tag_id = serializers.IntegerField()  # 外键关联标签id
    t_comment = serializers.IntegerField()  # 总评论数
    sales = serializers.IntegerField()  # 销量



class AddressSerializer(serializers.Serializer):
    name = serializers.CharField()
    adress = serializers.CharField()
    mobile = serializers.CharField()
    user_id = serializers.IntegerField()
    is_default = serializers.IntegerField()  # 0 未默认  1 默认

    def create(self, data):
        return Address.objects.create(**data)

class OrderDetailModelSerializer(serializers.ModelSerializer):
    class Meta:
        model=Order_detail
        fields="__all__"



#订单序列化
class OrderModelSerializer(serializers.ModelSerializer):
    orderdetail=serializers.SerializerMethodField()

    def get_orderdetail(self,row):
        orderdetail_list=Order_detail.objects.filter(order_sn=row).all()
        orderdetail=OrderDetailModelSerializer(orderdetail_list,many=True)
        return orderdetail.data

    class Meta:
        model=Orders
        fields="__all__"
