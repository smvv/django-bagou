# -*- coding: utf-8 -*-
from django.conf.urls import url
from django.conf.urls import include
from django.conf.urls import patterns

from django.views.generic import TemplateView
from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns(
    '',
    url(r'^$', TemplateView.as_view(template_name='index.html')),
    url(r'^admin/', include(admin.site.urls)),
)
