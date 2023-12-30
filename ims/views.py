import re
from collections import Counter

import jieba
from django.contrib import messages
from django.core.exceptions import ValidationError
from django.core.validators import URLValidator
from django.shortcuts import render, get_object_or_404, redirect
from django.utils import timezone
from django.views import generic

from common.utils import extract_keywords
from .forms import AddForm, MultiURLForm
from .models import Link


def index(request):
    return render(request, "ims/index.html")


def add(request):
    return render(request, "ims/add.html")


def add_v22(request):
    saved_object = None
    if request.method == 'POST':
        form = AddForm(request.POST)
        if form.is_valid():
            # 处理表单数据
            saved_object = form.save()
            messages.success(request, '表单提交成功！')
    else:
        form = AddForm()

    return render(request, 'ims/add_v2.html', {'form': form, 'saved_object': saved_object})


def add_v2(request):
    form = MultiURLForm(request.POST or None)
    saved_links = []  # 用于存储成功保存的Link实例
    if request.method == 'POST' and form.is_valid():
        urls_field = form.cleaned_data['urls']
        urls = urls_field.splitlines()
        for url in urls:
            url = url.strip()
            if url:
                validate = URLValidator()
                try:
                    validate(url)
                    link = Link.objects.create(url=url)
                    saved_links.append(link)  # 添加到列表中
                except ValidationError:
                    messages.error(request, f"'{url}' 不是一个有效的URL。")
                    return redirect('ims:add_v2')
        if saved_links:
            messages.success(request, '所有有效URL已添加！')
            return redirect('ims:add_v2')
        # form = MultiURLForm()  # 重置表单

    return render(request, 'ims/add_v2.html', {'form': form, 'saved_links': saved_links})


class DetailView(generic.DetailView):
    model = Link
    template_name = "ims/detail.html"

    def get_queryset(self):
        """
        Excludes any questions that aren't published yet.
        """
        return Link.objects.filter(pub_date__lte=timezone.now())

    def get_object(self):
        uuid = self.kwargs.get('uuid')
        return get_object_or_404(Link, uuid=uuid)

    def get_context_data(self, **kwargs):
        context = super(DetailView, self).get_context_data(**kwargs)
        link = self.get_object()

        context['title'] = link.name

        text = link.name + link.description
        keywords = extract_keywords(text)
        context['keywords'] = ','.join(keywords)

        context['description'] = link.description
        return context
