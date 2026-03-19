import os
import json
from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse
from django.conf import settings
from django.http import JsonResponse
from django.db import connections, models
from .models import Bookmarks, Tags, BookmarkTags
from django.utils import timezone
from django.core.paginator import Paginator

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
                models.Q(title__icontains=filter_keyword) |
                models.Q(description__icontains=filter_keyword)
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