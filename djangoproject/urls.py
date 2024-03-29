"""
URL configuration for djangoproject project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.0/topics/http/urls/
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
from django.urls import path, include
from main import views
from django.conf import settings
from django.conf.urls.static import static


urlpatterns = [
    path('admin/', admin.site.urls),
    path('index/', views.index),
    path('', views.index),

    path('regis/', views.regis),
    path('login/', views.login),
    path('logout/', views.logout),

    path('notice/list', views.notice_list),
    path('notice/launch', views.launch),
    path('n/<int:nid>', views.n),
    path('notice/', views.notice),

    path('post/', views.create_post),
    path('post/list', views.post_list),
    path('p/<int:pk>', views.post_detail),
    path('add_comment/<int:pk>', views.add_comment),
    path('delete_comment/<int:pk>', views.delete_comment),
    path('delete_post/<int:pk>', views.delete_post),
    path('category', views.category),
    path('c/<int:cid>', views.category_detail),

    path('account/', views.view_info),
    path('account/info', views.view_info),
    path('account/edit', views.edit_info),
    path('account/posts', views.my_posts),
    path('account/comments', views.my_comments),
    path('account/subscription', views.subscription),

]
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
