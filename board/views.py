from django.shortcuts import render, redirect
from .models import Message


def index(request):
    if request.method == 'POST':
        content = request.POST.get('content', '').strip()
        if content:
            Message.objects.create(content=content)
        return redirect('board:index')  # PRG 模式，防止刷新重复提交

    messages = Message.objects.all()
    return render(request, 'board/index.html', {'messages': messages})
