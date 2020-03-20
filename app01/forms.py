from django.core.exceptions import ValidationError
from django.forms import Form, fields, widgets

from app01.models import User


class RegisterForm(Form):
    """
    注册form
    """
    username = fields.CharField(
        widget=widgets.TextInput(attrs={'placeholder': u'用户名',"class": "form-control"}),
        max_length=18,
        min_length=6,
        required=True,
        error_messages={
            'required': "用户名不能为空",
            'max_length': "用户名长度不能超过18位",
            'min_length': "用户名长度不能少于6位",
        }
    )
    email = fields.EmailField(
        widget=widgets.EmailInput(attrs={'placeholder': u'邮箱',"class": "form-control"}),
        required=True,
        error_messages={
            'required': "邮箱不能为空",
        }
    )
    url = fields.URLField(
        widget=widgets.URLInput(attrs={'placeholder': u'个人博客地址',"class": "form-control"}),
        initial="http://",
        required=True,
        error_messages={
            'required': "个人博客地址不能为空"
        }

    )
    password = fields.CharField(
        widget=widgets.TextInput(attrs={'placeholder': u'密码',"class": "form-control"}),
        max_length=16,
        min_length=8,
        required=True,
        error_messages={
            'required': "密码不能为空",
            'max_length': "密码长度不能超过18位",
            'min_length': "密码长度不能少于8位",
        }
    )
    check_password = fields.CharField(
        widget=widgets.TextInput(attrs={'placeholder': u'请再次输入密码',"class": "form-control"}),
        max_length=16,
        min_length=8,
        required=True,
        error_messages={
            'required': "密码不能为空",
            'max_length': "密码长度不能超过18位",
            'min_length': "密码长度不能少于8位",
        }
    )

    def clean_username(self):
        val = self.cleaned_data.get("username")
        ret = User.objects.filter(username=val)
        if not ret:
            return val
        else:
            raise ValidationError("该用户已注册")

    def clean_email(self):
        val = self.cleaned_data.get("email")
        ret = User.objects.filter(email=val)
        if not ret:
            return val
        else:
            raise ValidationError("该邮箱已被注册")

    def clean_check_password(self):
        pwd = self.cleaned_data.get("password")
        ck_pwd = self.cleaned_data.get("check_password")
        if pwd and ck_pwd:
            if pwd == ck_pwd:
                return ck_pwd
            else:
                raise ValidationError('两次密码不一致')
        else:
            raise ValidationError("请填写密码")


class LoginForm(Form):
    """
    登录form
    """
    username = fields.CharField(
        widget=widgets.TextInput(attrs={'placeholder': u'用户名'}),
        max_length=18,
        min_length=6,
        required=True,
        error_messages={
            'required': "用户名不能为空"
        }
    )
    password = fields.CharField(
        widget=widgets.PasswordInput(attrs={'placeholder': u'密码'}),
        max_length=16,
        min_length=8,
        required=True,
        error_messages={
            'required': "密码不能为空"
        }
    )


class UserInfoFrom(Form):
    """
    用户信息form
    """
    avatar = fields.ImageField(
        label="头像",
        required=False,
        widget=widgets.FileInput(attrs={"id":"avatar","style": "display:none"})
    )
    nickname = fields.CharField(
        label="昵称:",
        widget=widgets.TextInput(attrs={"class": "form-control"}),
        max_length=18,
        min_length=1,
        required=False,
        error_messages={
            'max_length': "用户名长度不能超过18位",
            'min_length': "用户名长度不能少于6位",
        }
    )
    sex = fields.CharField(
        initial=1,
        label="性别:",
        required=False,
        widget=widgets.RadioSelect(choices=[(1, "男"), (2, "女")]),
    )
    mobile = fields.IntegerField(
        label="电话号码",
        required=False,
        widget=widgets.TextInput(attrs={"class": "form-control"})
    )
    intro = fields.CharField(
        label="个人介绍",
        required=False,
        max_length=200,
        widget=widgets.Textarea(attrs={"placeholder": "快些点简介介绍下自己吧......", "class": "form-control"})
    )

    def setvalue(self, avatar, nickname, sex, mobile, intro):
        self.fields['avatar'].widget.attrs.update({'value': avatar if avatar is not None else ""})
        self.fields['nickname'].widget.attrs.update({'value': nickname if nickname is not None else ""})
        self.initial["sex"] = sex
        self.fields['mobile'].widget.attrs.update({'value': mobile if mobile is not None else ""})
        self.initial["intro"] = intro

class PubArticleForm(Form):
    title = fields.CharField(
        widget=widgets.TextInput(attrs={"placeholder": "标题"}),
        label="标题",
        required=True,
        max_length=30
    )
    article_content = fields.CharField(
        widget=widgets.Textarea(attrs={"placeholder": "写点什么吧", 'cols': '80', 'rows': '30',"class":"form-control"}),
        label="文章内容",
        required=True,
    )
    def setvalue(self,title,article_content):
        self.fields['title'].widget.attrs.update({'value':title })
        self.initial["article_content"] = article_content
