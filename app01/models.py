from django.db import models


# Create your models here.
class User(models.Model):
    """
    用户表
    """
    user_id = models.AutoField(verbose_name="用户ID", primary_key=True)
    username = models.CharField(max_length=32, unique=True, verbose_name="用户名")  # 用户名
    password = models.CharField(max_length=32, verbose_name="密码")  # 密码
    email = models.EmailField(verbose_name="邮箱")  # 邮箱
    url = models.URLField(max_length=100, blank=True, null=True, verbose_name='个人博客地址')
    # uinfo_id = models.ForeignKey("UserInfo", on_delete=models.CASCADE, null=True)  # 用户详细信息


class UserInfo(models.Model):
    """
    用户详情表
    """
    user_info_id = models.AutoField(primary_key=True,verbose_name="用户ID")
    nickname = models.CharField(max_length=32, verbose_name='昵称',null=True)  # 昵称
    sex = models.IntegerField(verbose_name="性别",default=1)  # 性别
    mobile = models.CharField(max_length=11, blank=True, null=True, unique=True, verbose_name='手机号码')
    intro = models.CharField(max_length=200, blank=True, null=False)  # 个人简介，限制200个字符
    avatar = models.ImageField(upload_to='avatar/', max_length=200, default="avatar/default.png", blank=True, verbose_name="头像")  # 头像，未设置即为默认
    uid=models.ForeignKey("User",on_delete=models.CASCADE)

class Article(models.Model):
    """
    文章表
    """
    article_id = models.AutoField(verbose_name="文章ID", primary_key=True)
    uid = models.ForeignKey("User", on_delete=models.CASCADE)
    title = models.CharField(max_length=30, verbose_name="标题")
    article_content = models.TextField(verbose_name="文章内容")
    create_date = models.DateTimeField(auto_now_add=True, verbose_name="发布时间")
    last_updatetime = models.DateTimeField(auto_now=True, verbose_name="上次更新时间", null=True, blank=True)
    state=models.IntegerField(default=1,verbose_name="状态")

class Comment(models.Model):
    """评论表"""
    comment_id = models.AutoField(verbose_name="评论ID", primary_key=True)
    article_id = models.ForeignKey("Article", on_delete=models.CASCADE, verbose_name="文章ID")
    comment_content = models.CharField(max_length=400, verbose_name="评论内容")
    user_id = models.ForeignKey("User", on_delete=models.CASCADE, verbose_name="评论者ID")
    reply_id = models.ForeignKey('Comment', on_delete=models.CASCADE, null=True, blank=True, verbose_name="评论的ID")
    comment_date = models.DateTimeField(auto_now_add=True, verbose_name="评论时间")
