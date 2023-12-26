import re
from collections import Counter

import jieba
from django.shortcuts import render, get_object_or_404
from django.utils import timezone
from django.views import generic

from common.utils import extract_keywords
from .models import Link


def index(request):
    return render(request, "ims/index.html")


def add(request):
    return render(request, "ims/add.html")


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

        text = link.name+link.description
        keywords = extract_keywords(text)
        context['keywords'] = ','.join(keywords)

        context['description'] = link.description
        return context
