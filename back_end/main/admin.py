from django.contrib import admin
from django.apps import apps

# 获取所有应用程序
app_models = apps.get_models()

# 为每个模型注册到 Admin 界面
for model in app_models:
    if not admin.site.is_registered(model):
        admin.site.register(model)