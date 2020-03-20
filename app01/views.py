import json
from django.shortcuts import render, redirect, HttpResponse
from django.utils import timezone
from .forms import *
from .models import *
from utils.pager import PageInfo


# Create your views here.
def login(request):
    """
    登录模块
    :param request:
    :return:
    """
    if request.method == "GET":
        if request.session.get("userinfo"):
            return redirect('/index.html')
        loginform = LoginForm()
        return render(request, "login.html", {"loginform": loginform})
    else:
        loginform = LoginForm(request.POST)
        if loginform.is_valid():
            # 进行登录验证
            username = loginform.cleaned_data['username']
            paasword = loginform.cleaned_data['password']
            user = User.objects.filter(username=username, password=paasword).values("user_id", "username", "password")
            print(list(user))
            if user:
                request.session["userinfo"] = list(user)
                return redirect("/index.html")
            else:
                print(loginform.errors)
                return render(request, "login.html", {"loginform": loginform, "errormsg": "用户名或密码错误"})
        else:
            return render(request, 'login.html', {"loginform": loginform})


def regist(request):
    """
    注册模块
    :param request:
    :return:
    """
    if request.method == "GET":
        regform = RegisterForm()
        return render(request, "regist.html", {"form": regform})
    else:
        regform = RegisterForm(request.POST)
        if regform.is_valid():
            username = regform.cleaned_data['username']
            email = regform.cleaned_data['email']
            url = regform.cleaned_data['url']
            password = regform.cleaned_data['password']

            uid = User.objects.create(username=username, email=email, url=url, password=password)
            UserInfo.objects.create(uid=uid)
            return redirect('login.html')
        else:
            return render(request, "regist.html", {"form": regform})


def logout(request):
    """
    用户退出登录
    :param request:
    :return:
    """
    if request.session.get("userinfo"):
        del request.session['userinfo']
    return redirect("/index.html")


def update_user(request):
    if request.method == "GET":
        user = request.session.get("userinfo")
        uid = user[0].get("user_id")
        userinfo = UserInfo.objects.filter(uid=uid).first()
        avatar = "static/avatar/default.png"
        if userinfo:
            avatar = userinfo.avatar
            nickname = userinfo.nickname
            sex = userinfo.sex
            mobile = userinfo.mobile
            intro = userinfo.intro
            userinfo_form = UserInfoFrom()
            userinfo_form.setvalue(avatar=avatar, nickname=nickname, sex=sex, mobile=mobile, intro=intro)
        else:
            userinfo_form = UserInfoFrom(None, None, None, None, None)
        return render(request, "update_user.html", {"form": userinfo_form, "avatarpath": avatar})
    else:
        userinfo_form = UserInfoFrom(data=request.POST, files=request.FILES)

        if userinfo_form.is_valid():  # 更新用户信息
            user = request.session.get("userinfo")
            uid = user[0].get("user_id")
            userinfo = UserInfo.objects.filter(uid=uid)  # 数据库中查找该用户是否填写用户信息
            u = User.objects.filter(user_id=uid).first()
            nickname = userinfo_form.cleaned_data.get("nickname")
            sex = userinfo_form.cleaned_data.get("sex")
            mobile = userinfo_form.cleaned_data.get("mobile")
            intro = userinfo_form.cleaned_data.get("intro")
            if userinfo:
                userinfo.update(nickname=nickname, sex=sex, mobile=mobile, intro=intro, uid=u)
            else:
                avatar = userinfo_form.cleaned_data.get("avatar")
                UserInfo.objects.create(avatar=avatar, nickname=nickname, sex=sex, mobile=mobile, intro=intro, uid=u)
            return redirect("/index.html")
        else:
            return render(request, "update_user.html", {"form": userinfo_form})


def pub_article(request):
    if request.method == "GET":
        pub_article_form = PubArticleForm()
        return render(request, "pub_article.html", {"form": pub_article_form})
    else:
        pub_article_form = PubArticleForm(request.POST)
        if pub_article_form.is_valid():
            title = pub_article_form.cleaned_data['title']
            article_content = pub_article_form.cleaned_data['article_content']
            u = User.objects.filter(user_id=request.session.get("userinfo")[0].get('user_id')).first()
            Article.objects.create(uid=u, title=title, article_content=article_content)
            return redirect("/show_my_article/")
        else:
            return render(request, "pub_article.html", {"form": pub_article_form})


def show_my_article(request):
    userinfo = request.session.get("userinfo")
    if userinfo:
        all_count = Article.objects.all().count()
        page_info = PageInfo(request.GET.get("page"), all_count, 10, '/show_my_article')
        user_id = userinfo[0].get('user_id')
        article_list = Article.objects.filter(state=1, uid=user_id).all().values_list("article_id", "title",
                                                                                      "create_date",
                                                                                      "last_updatetime")[
                       page_info.start():page_info.end()]
        print(article_list, type(article_list))
        for i in article_list:
            print(i)
        return render(request, "show_my_article.html", {"article_list": list(article_list),"page_info": page_info})
    else:
        return redirect("/login.html")

def article_details(request, article_id):
    article = Article.objects.filter(article_id=article_id).values("article_id", "title", "uid__username",
                                                                   "article_content",
                                                                   "create_date", "last_updatetime")
    comment_list = Comment.objects.filter(article_id=article_id,reply_id__isnull=True).order_by("-comment_date").values_list("comment_id","user_id", "user_id__username",
                                                                             "comment_content", "comment_date",
                                                                             "reply_id","user_id__userinfo__avatar")
    print(comment_list)
    reply_list=Comment.objects.filter(article_id=article_id,reply_id__isnull=False).order_by("-comment_date").values_list("comment_id","user_id", "user_id__username",
                                                                             "comment_content", "comment_date",
                                                                             "reply_id")
    print(reply_list)
    return render(request, "article.html", {"article": article[0], "comment_list": comment_list,"reply_list":reply_list})


def upload_avatar(request):
    avatar = request.FILES.get('avatar_img')
    print(request.FILES)
    user = request.session.get("userinfo")
    uid = user[0].get("user_id")
    userinfo = UserInfo.objects.filter(uid=uid).first()  # 数据库中查找该用户是否填写用户信息
    u = User.objects.filter(user_id=uid).first()
    if userinfo:
        userinfo.avatar = avatar
        userinfo.save()
    else:
        UserInfo.objects.create(avatar=avatar, uid=u)
    print(userinfo.avatar)
    avatar = UserInfo.objects.filter(uid=uid).values("avatar")
    data = {"avatar": avatar[0]}
    return HttpResponse(json.dumps(data))


def update_article(request, article_id):
    if request.method == "GET":
        uinfo = request.session.get("userinfo")
        if uinfo:#如果用户登录
            user_id = uinfo[0]["user_id"]
            article_list = Article.objects.filter(state=1, uid=user_id).all().values_list("article_id")
            article_list=[x[0] for x in article_list]
            if article_id not in article_list:
                return redirect("/show_my_article/")
        article = Article.objects.filter(article_id=article_id).first()
        update_article_form = PubArticleForm()
        update_article_form.setvalue(article.title, article.article_content)
        return render(request, "update_article.html", {"form": update_article_form, "article_id": article_id})
    else:
        update_article_form = PubArticleForm(request.POST)
        if update_article_form.is_valid():
            title = update_article_form.cleaned_data.get("title")
            article_content = update_article_form.cleaned_data.get("article_content")
            article_last_updatetime = timezone.now()
            Article.objects.filter(article_id=article_id).update(title=title, article_content=article_content,
                                                                 last_updatetime=article_last_updatetime)
            return redirect('show_my_article')
        else:
            return render(request, "update_article.html", {"form": update_article_form})


def del_article(request, article_id):
    uinfo=request.session.get("userinfo")
    if uinfo:
        user_id=uinfo.user_id
        article_list = Article.objects.filter(state=1, uid=user_id).all().values_list("article_id")
        if article_id not in article_list:
            return redirect("/show_my_article/")
        ret = {'status': True, 'message': None}
        try:
            Article.objects.filter(article_id=article_id).update(state=0)
        except Exception as e:
            ret["status"] = False
            ret["message"] = "删除失败"
        return HttpResponse(json.dumps(ret))


def index(request):
    # 表示用户想要访问的页
    # 每页显示数据
    all_count = Article.objects.all().count()

    page_info = PageInfo(request.GET.get("page"), all_count, 5, '/index.html')
    article_list = Article.objects.all().order_by("-create_date").values("article_id", "title", "article_content",
                                                                         "uid__username", "create_date", "uid")[
                   page_info.start():page_info.end()]
    return render(request, "index.html", {"article_list": article_list, "page_info": page_info})


def post_coment(request):
    ret = {'status': True, 'message': None}
    user_id = int(request.POST.get("user_id"))
    content = request.POST.get("content")
    reply_id=request.POST.get("reply_id")
    article_id = request.POST.get("article_id")
    print(reply_id)
    try:
        article = Article.objects.filter(article_id=article_id).first()
        user = User.objects.filter(user_id=user_id).first()
        if not reply_id:
            reply_id=None
        else:
            reply_id=Comment.objects.filter(comment_id=reply_id).first()
        Comment.objects.create(article_id=article, comment_content=content, user_id=user,reply_id=reply_id)
    except Exception as e:
        print(e)
        ret["status"] = False
        ret["message"] = "评论失败"
    return HttpResponse(json.dumps(ret))


def userindex(request, user_id):
    if request.method == "GET":
        # print(request.session.get("userinfo"))
        u = UserInfo.objects.filter(uid=user_id)
        # print("1",u)
        # print(list(u) == [])
        # print(not list(u))
        if list(u):
            uinfo = u.values("user_info_id", "nickname", "sex", "mobile", "intro", "avatar", "uid")
            return render(request, "userinfo.html", {"uinfo": uinfo[0]})
        else:
            return redirect("/index.html")
