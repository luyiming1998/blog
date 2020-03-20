"""blog URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.2/topics/http/urls/
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
from django.urls import path, re_path
from django.views.static import serve
from .settings import MEDIA_ROOT
from app01 import views

urlpatterns = [
    path('admin/', admin.site.urls),
    re_path(r'^upload/(?P<path>.*)$', serve, {'document_root': MEDIA_ROOT}),
    path('index.html/',views.index),
    path('', views.index),
    path('login.html', views.login),
    path('regist.html', views.regist),
    path('logout/', views.logout),
    path('update_user/', views.update_user),
    path('upload_avatar/', views.upload_avatar),
    path('pub_article/', views.pub_article),
    path('show_my_article/', views.show_my_article),
    path('article/<int:article_id>', views.article_details),
    path('update_article/<int:article_id>', views.update_article),
    path('del_article/<int:article_id>', views.del_article),
    path('post_comment/',views.post_coment),
    path('uindex/<int:user_id>',views.userindex)
]
