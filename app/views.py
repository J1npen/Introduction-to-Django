import os
import json
from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse
from django.conf import settings
from django.http import JsonResponse
from django.db import connections
from django.db.models import Q
from .models import Bookmarks, Tags, BookmarkTags
from django.utils import timezone
from django.core.paginator import Paginator
from rest_framework import viewsets
from rest_framework.response import Response
from .serializers import BookmarkSerializer, TagSerializer

def index(request):
    context = {
        'name': 'Jinpen',
        'age': 22,
    }
    return render(request, 'app/index.html', context)

def picrotate(request):
    # 扫描 app/static/app/img 目录下的所有图片
    img_dir = os.path.join(settings.BASE_DIR, 'app', 'static', 'app', 'img')
    
    # 👇 加这几行调试
    print("BASE_DIR:", settings.BASE_DIR)
    print("img_dir:", img_dir)
    print("目录存在:", os.path.isdir(img_dir))
    if os.path.isdir(img_dir):
        print("目录内容:", os.listdir(img_dir))

    extensions = {'.jpg', '.jpeg', '.png', '.gif', '.webp', '.svg'}
    images = []
    
    if os.path.isdir(img_dir):
        for fname in os.listdir(img_dir):
            if os.path.splitext(fname)[1].lower() in extensions:
                images.append(fname)
    
    return render(request, 'app/picrotate.html', {
        'images_json': json.dumps(images),
    })

def get_bookmarks(request):
    # 查询全部
    bookmarks = Bookmarks.objects.all()

    # 转成列表返回
    data = list(bookmarks.values())
    return JsonResponse(data, safe=False)

def test(request):
    queryset = Bookmarks.objects.prefetch_related('bookmarktags_set__tag').order_by('id')

    data = []
    for bm in queryset:
        data.append({
            'id': bm.id,
            'title': bm.title,
            'url': bm.url,
            # 利用预取结果，不触发额外 SQL
            'tags': [bt.tag.name for bt in bm.bookmarktags_set.all()]
        })

    return JsonResponse(data, safe=False)

def bookmark(request):
    filter_keyword = request.GET.get('keyword', '').strip()
    tag_slug      = request.GET.get('tag', '').strip()
    search_in     = request.GET.get('search_in', 'title')  # title | description | all

    queryset = Bookmarks.objects.prefetch_related(
        'bookmarktags_set__tag'
    ).order_by('-id')

    if filter_keyword:
        if search_in == 'description':
            queryset = queryset.filter(description__icontains=filter_keyword)
        elif search_in == 'all':
            queryset = queryset.filter(
                Q(title__icontains=filter_keyword) |
                Q(description__icontains=filter_keyword)
            )
        else:  # title (默认)
            queryset = queryset.filter(title__icontains=filter_keyword)

    if tag_slug:
        queryset = queryset.filter(bookmarktags__tag__slug=tag_slug)

    paginator  = Paginator(queryset, 15)
    page_obj   = paginator.get_page(request.GET.get('page', 1))
    all_tags   = Tags.objects.all().order_by('name')

    return render(request, 'app/bookmark.html', {
        'page_obj' : page_obj,
        'keyword'  : filter_keyword,
        'tag_slug' : tag_slug,
        'search_in': search_in,
        'all_tags' : all_tags,
    })


def bookmark_visit(request, pk):
    """记录点击次数并跳转"""
    bookmark = get_object_or_404(Bookmarks, pk=pk)
    Bookmarks.objects.filter(pk=pk).update(
        visit_count=bookmark.visit_count + 1,
        last_visit=timezone.now()
    )
    return redirect(bookmark.url)

class BookmarkViewSet(viewsets.ModelViewSet):
    """
    书签 CRUD API

    列表过滤参数：
      ?favorite=1       — 只看收藏
      ?is_active=0|1    — 按可访问状态
      ?tag=<slug>       — 按标签 slug
      ?keyword=<text>   — 关键词搜索
      ?search_in=title|description|all  — 搜索范围（默认 title）
    """
    serializer_class = BookmarkSerializer

    # get_queryset 就是钩子（父类预留的、子类可覆盖的方法）。
    # 父类流程不变，get_queryset 只替换"取数据"这一步。
    def get_queryset(self):
        qs = Bookmarks.objects.order_by('-created_at')
        p = self.request.query_params

        if (favorite := p.get('favorite')) is not None:
            qs = qs.filter(is_favorite=favorite)

        if (is_active := p.get('is_active')) is not None:
            qs = qs.filter(is_active=is_active)

        if tag_slug := p.get('tag'):
            qs = qs.filter(bookmarktags__tag__slug=tag_slug)

        if keyword := p.get('keyword', '').strip():
            search_in = p.get('search_in', 'title')
            if search_in == 'description':
                qs = qs.filter(description__icontains=keyword)
            elif search_in == 'all':
                qs = qs.filter(
                    Q(title__icontains=keyword) | Q(description__icontains=keyword)
                )
            else:
                qs = qs.filter(title__icontains=keyword)

        return qs.distinct()


class TagViewSet(viewsets.ModelViewSet):
    """标签 CRUD API"""
    # ModelViewSet = 帮你把"操作一张数据库表"的所有标准接口（CURD）都写好了，
    # 你只需要告诉它用哪个 Model（queryset） 和用哪个 Serializer，其余按需覆盖即可。
    serializer_class = TagSerializer
    queryset = Tags.objects.all().order_by('name')