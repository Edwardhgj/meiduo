from django.db import models


# Create your models here.

# 更新时间表
class Base(models.Model):
    create_time = models.DateTimeField(auto_now_add=True)  # 开始创表时间
    update_time = models.DateTimeField(auto_now=True)  # 更新表时间

    class Meta:
        abstract = True  # 创建抽象类


# 管理员表
class Sadmin(Base, models.Model):
    username = models.CharField(max_length=255)  # 管理员登陆账户
    password = models.CharField(max_length=128)  # 管理员登陆密码
    is_admin = models.IntegerField(default=0)  # 1超级管理员权限

    class Meta:
        db_table = "sadmin"


# 分类表
class Cate(Base, models.Model):
    name = models.CharField(max_length=50)  # 分类名称
    pid = models.IntegerField(default=0)  # 顶级分类默认0
    type = models.IntegerField(default=1)  # 标示几级分类
    picture = models.CharField(max_length=255, default='')  # 图片名称
    top_id = models.IntegerField(default=1)  #
    is_recommend = models.IntegerField(default=1)  # 是否首页推荐(1:是，0：否)

    class Meta:
        db_table = "cate"
        """
        1 手机        第一级 pid=0  type=1  top_id=0
        2 华为手机     第二级 pid=1  type=2  top_id=1
        3 华为note    第三极  pid=2 type=3  top_id=1
         """


# 标签表
class Tags(Base, models.Model):
    name = models.CharField(max_length=50)  # 分类名称
    cid = models.ForeignKey('Cate', on_delete=models.CASCADE)  # 外键关联分类表
    is_recommend = models.IntegerField(default=1)  # 是否首页推荐(1:是，0：否)

    class Meta:
        db_table = "tags"


# 焦点图表
class Banners(Base, models.Model):
    name = models.CharField(max_length=255)
    is_show = models.IntegerField(default=1)  # 焦点图是否展示(1:是，0：否)
    sort = models.IntegerField(default=1)
    type = models.IntegerField(default=1)  # 1 焦点图 ，2 广告图

    class Meta:
        db_table = "banners"


# 新闻表
class News(Base, models.Model):
    title = models.CharField(max_length=255)
    is_show = models.IntegerField(default=1)  # 焦点图是否展示(1:是，0：否)
    content = models.TextField()  # 内容

    class Meta:
        db_table = "news"


# 商品表
class Goods(Base, models.Model):
    name = models.CharField(max_length=255)  # 商品名
    describe = models.TextField()  # 描述
    content = models.TextField()  # 内容
    picture = models.CharField(max_length=255)  # 图片名称
    storage = models.IntegerField(default=0)  # 库存
    lock_storage = models.IntegerField(default=0)  # 锁定库存
    price = models.DecimalField(max_digits=10, decimal_places=2)
    is_recommend = models.IntegerField(default=1)  # 推荐默认为1，不推荐为0
    cid = models.ForeignKey("Cate", on_delete=models.CASCADE)  # 外键关联分类id
    top_id = models.IntegerField()  # 顶级分类
    tag_id = models.ForeignKey("Tags", on_delete=models.CASCADE)  # 外键关联标签id
    t_comment = models.IntegerField(default=0)  # 总评论数
    sales = models.IntegerField(default=0)  # 销量

    class Meta:
        db_table = "goods"


from django.contrib.auth.models import AbstractUser
# 用户表
class User(AbstractUser):
    username = models.CharField(max_length=50,unique=True)  # 用户名
    password = models.CharField(max_length=255)  # 密码
    mobile = models.CharField(max_length=11)  # 电话
    email = models.CharField(max_length=50)  # 邮件
    image = models.CharField(max_length=255, default="")  # 图片
    signator = models.CharField(max_length=255, default="")  # 个性签名
    is_valid = models.IntegerField(default=0)  # 验证是否有效  0未验证 1验证成功 2验证失败
    token=models.CharField(max_length=100,default='') #用于注册验证生成token值

    class Meta:
        db_table = "user"



#购物车
class Cart(Base,models.Model):
    user_id=models.IntegerField()
    good_id=models.IntegerField()
    price=models.DecimalField(max_digits=7,decimal_places=2)
    count=models.IntegerField()
    picture=models.CharField(max_length=255)
    good_name=models.CharField(max_length=100)
    is_checked=models.IntegerField(default=0)  # 0未支付 1已支付 2未评价 3 已评价
    class Meta:
        db_table="cart"


#订单表
class Orders(Base,models.Model):
    order_sn=models.CharField(max_length=180,unique=True)
    user=models.ForeignKey('User',on_delete=models.CASCADE)
    tmoney=models.DecimalField(max_digits=10,decimal_places=2)
    adress=models.ForeignKey('Address',on_delete=models.CASCADE)
    status=models.IntegerField(default=0) # 0代表未支付 1 代表已经支付
    pay_type=models.IntegerField(default=1) #1 代表自由支付 2 支付宝  3 微信
    code=models.CharField(max_length=100,default='') # 流水号
    class Meta:
        db_table="orders"


#订单详情表
class Order_detail(models.Model):
    order_sn = models.ForeignKey('Orders',to_field='order_sn',on_delete=models.CASCADE)
    user = models.ForeignKey('User', on_delete=models.CASCADE)
    name=models.CharField(max_length=50, default='')  #商品名称
    price = models.DecimalField(max_digits=6, decimal_places=2)
    count=models.IntegerField(default=0)
    image=models.CharField(max_length=255)
    class Meta:
        db_table="order_detail"


#地址表
class Address(models.Model):
    name=models.CharField(max_length=50)
    adress=models.CharField(max_length=255,default='')
    mobile=models.CharField(max_length=11)
    user=models.ForeignKey('User',on_delete=models.CASCADE)
    is_default=models.IntegerField(default=0) #0 未默认  1 默认

    class Meta:
        db_table = "address"