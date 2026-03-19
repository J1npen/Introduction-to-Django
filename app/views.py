import os
import json
from django.shortcuts import render, redirect 
from django.http import HttpResponse
from django.conf import settings
from django.http import JsonResponse
from django.db import connections
from .models import Bookmarks

def test(request):
    try:
        conn = connections['mysql_db']
        conn.ensure_connection()
        return JsonResponse({'status': 'ok', 'message': '✅ MySQL 连接成功！'})
    except Exception as e:
        return JsonResponse({'status': 'error', 'message': str(e)}, status=500)

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

def bookmark(request):
    result = []
    filter_keyword = ''

    if request.method == 'POST':
        filter_keyword = request.POST.get('filter_keyword', '').strip()
        if filter_keyword:
            result = Bookmarks.objects.filter(
                title__icontains=filter_keyword
            ).order_by('-id')[:20]

    return render(request, 'app/bookmark.html', {
        'result': result,
        'keyword': filter_keyword
    })