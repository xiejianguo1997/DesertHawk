import datetime
import decimal
import hashlib
import json
import os
import pymysql
from django.http import HttpResponse
from django.shortcuts import render

from DesertHawk.settings import BLOG_ROOT, DATABASES, JsonCustomEncoder
from django.views.decorators.csrf import csrf_exempt

from apps.articles.models import ContentImage, Article
from apps.statistic.models import SiteStatistic


def index(request):
    return render(request, 'index.html')  # 只返回页面，数据全部通过ajax获取

def content_image(request):
    md5 = request.GET.get('md5')

    record = ContentImage.objects.filter(md5=md5).values("image").first()
    response = dict()

    if record:
        image = record['image']
        response["status"] = "success"
        response["image"] = image
    else:
        response["status"] = "error"

    return HttpResponse(response["image"])


def home(request):
    if 'page_id' not in request.GET:
        return render(request, 'index.html')

    page_id = request.GET.get("page_id", "1")
    page_id = int(page_id)

    articles = Article.objects.values("title", "description", "date").order_by("date")

    page_size = 7
    total_pages = int(len(articles) / page_size) + 1

    from_idx = page_size * (page_id - 1)
    end_idx = page_size * (page_id - 1) + page_size

    articles = articles[from_idx: end_idx]

    context = dict()
    context["code"] = 200
    context["result"] = articles
    context['page_id'] = page_id,  # 当前页面
    context['total_pages'] = total_pages  # 页面总数

    return HttpResponse(json.dumps(context, cls=JsonCustomEncoder), content_type="application/json")

def page_not_found(request, exception):
    return render(request, '404.html')

# 500
def page_error(request):
    return render(request, '500.html')
