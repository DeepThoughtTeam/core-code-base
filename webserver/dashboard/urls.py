"""dashboard URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.8/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Add an import:  from blog import urls as blog_urls
    2. Add a URL to urlpatterns:  url(r'^blog/', include(blog_urls))
"""

from django.conf.urls import url

urlpatterns = [
    # url(r'^uidemo/', include('user_interface_demo.urls')),
    url(r'^$', 'dashboard.views.index', name='index'),
    url(r'^app-server/', 'dashboard.views.app_server', name='app_server'),
    url(r'^send-net-info/', 'dashboard.views.proc_net_info', name='send_net_info'),
    url(r'^about/', 'dashboard.views.about', name='about'),
]
