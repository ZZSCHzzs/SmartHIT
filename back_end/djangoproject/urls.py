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

from django.urls import path, include
from rest_framework.routers import DefaultRouter
from main.views import *
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)

router = DefaultRouter()
router.register(r'auth', UserViewSet, basename='auth')
router.register(r'notifications', NotificationViewSet, basename='notification')
router.register(r'posts', PostViewSet, basename='post')
router.register(r'categories', CategoryViewSet, basename='category')
router.register(r'account', UserCenterViewSet, basename='account')
router.register(r'departments', DepartmentViewset, basename='department')
router.register(r'subscriptions', UserCategoryFollowViewSet, basename='subscription')
router.register(r'assistants', AssistantViewSet, basename='assistant')

urlpatterns = [
    path('', include(router.urls)),
    path('index_api/', index_api, name='index_api'),
    path('token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('admin/', admin.site.urls),
]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
