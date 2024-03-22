from django.shortcuts import render, HttpResponse, redirect, get_object_or_404
from django import forms
from hashlib import sha1
from django.utils import timezone
from django.http import JsonResponse
from main.models import *
from django.utils.safestring import mark_safe
from datetime import datetime, timedelta
import os
import uuid


class BaseImageForm(forms.ModelForm):
    additional_graphics = forms.ImageField(label="附加图片", required=False)

    def save(self, commit=True):
        instance = super().save(commit=False)
        if 'additional_graphics' in self.cleaned_data:
            image = self.cleaned_data['additional_graphics']
            if image:  # 检查是否有上传图片
                # 生成随机文件名
                filename = str(uuid.uuid4()) + os.path.splitext(image.name)[-1]
                instance.additional_graphics.save(filename, image, save=False)
        if commit:
            instance.save()
        return instance


class Pagination(object):
    def __init__(self, request, queryset,  page_size=10, page_param="page", plus=5):
        page = request.GET.get(page_param, '1')
        if page.isdigit():
            page = int(page)
            if page == 0:
                page = 1
        else:
            page = 1
        total_count = queryset.count()
        total_page_count, div = divmod(total_count, page_size)
        if div:
            total_page_count += 1
        if page > total_page_count:
            page = total_page_count

        self.total_page_count = total_page_count
        self.page = page
        self.page_size = page_size

        self.start = (page - 1) * page_size
        self.end = page * page_size

        self.page_queryset = queryset[self.start:self.end]

        self.plus = plus

    def html(self):

        if self.total_page_count <= 2 * self.plus + 1:
            start_page = 1
            end_page = self.total_page_count
        else:
            if self.page <= self.plus:
                start_page = 1
                end_page = 2 * self.plus + 1
            else:
                if (self.page + self.plus) > self.total_page_count:
                    start_page = self.total_page_count - 2 * self.plus
                    end_page = self.total_page_count
                else:
                    start_page = self.page - self.plus
                    end_page = self.page + self.plus

        page_str_list = [f'<li class="page-item"><a class="page-link" href="?page={1}" >首页</a></li>']

        # 上一页
        if self.page > 1:
            prev = f'<li class="page-item"><a class="page-link" href="?page={self.page - 1}">上一页</a></li>'
        else:
            prev = f'<li class="page-item"><a class="page-link" href="?page={1}">上一页</a></li>'
        page_str_list.append(prev)

        # 中间页
        for i in range(start_page, end_page + 1):
            if self.page == i:
                ele = f'<li class="active page-item"><a class="page-link" href="?page={i}">{i}</a></li>'
            else:
                ele = f'<li class="page-item"><a class="page-link" href="?page={i}">{i}</a></li>'
            page_str_list.append(ele)

        # 下一页
        if self.page < self.total_page_count:
            latter = f'<li class="page-item"><a class="page-link" href="?page={self.page + 1}">下一页</a></li>'
        else:
            latter = f'<li class="page-item"><a class="page-link" href="?page={self.total_page_count}">下一页</a></li>'
        page_str_list.append(latter)

        page_str_list.append(f'<li class="page-item"><a class="page-link" href="?page={self.total_page_count}">末页</a></li>')

        search_string = """
            <li>
                <form style="float: left;margin-left: -1px" method="get">
                    <input name="page" style="position: relative;float:left;display:inline-block;width: 80px;border-radius:0"
                    type="text" class="form-control" placeholder="页码">
                    <button style="border-radius: 0" class="btn btn-primary" type="submit">跳转</button>
                </form>
            </li>
        """

        page_str_list.append(search_string)
        page_string = mark_safe("".join(page_str_list))
        return page_string


def format_time(got_time):
    now = timezone.now()
    delta = now - got_time
    if delta.total_seconds() < 60:
        return "刚刚"
    if delta.total_seconds() < 3600:
        minutes = int(delta.total_seconds() / 60)
        return f"{minutes}分钟前"
    elif delta.total_seconds() < 3 * 24 * 3600:
        if got_time.date() == now.date():
            return got_time.strftime('%H:%M')
        elif got_time.date() == (now - timedelta(days=1)).date():
            return "昨天 " + got_time.strftime('%H:%M')
        else:
            return "前天 " + got_time.strftime('%H:%M')
    elif got_time.year == now.year:
        return got_time.strftime('%m月%d日')
    else:
        return got_time.strftime('%Y年%m月%d日')
