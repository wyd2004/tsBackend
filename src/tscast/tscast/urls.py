"""tscast URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.10/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import url
from django.conf.urls import include
from django.contrib import admin


from wechat.views import wechat_message

admin.site.site_url = None
admin.site.site_header = 'Podcast Data Console'
admin.site.index_title = 'Podcast Data Console'


from member.views import admin_bulk_add_member_invitation, mp_home


urlpatterns = [
    url(r'^admin/jet', include('jet.urls', 'jet')),
    url(r'^admin/jet/dashboard/', include('jet.dashboard.urls', 'jet-dashboard')),
    url(r'^admin/member/trialmember/bulk_add/', admin_bulk_add_member_invitation, name='bulk_add_member_invitation'),
    url(r'^admin/', admin.site.urls),

    url(r'^api/', include('wechat.urls')),
    url(r'^api/', include('member.urls')),
    url(r'^api/', include('podcast.urls')),
    url(r'^api/', include('term.urls')),

    # url(r'^mp', mp_home, name='mp_home'),
    url(r'^/$', mp_home, name='mp_home'),
    url(r'^search', mp_home, name='mp_home'),
    url(r'^profile', mp_home, name='mp_home'),
    url(r'^people', mp_home, name='mp_home'),
    url(r'^play', mp_home, name='mp_home'),
    url(r'^special', mp_home, name='mp_home'),
    url(r'^buy', mp_home, name='mp_home'),
    url(r'^pay', mp_home, name='mp_home'),
    url(r'^test/pay', mp_home, name='mp_home'),
    url(r'^project', mp_home, name='mp_home'),
    url(r'^subscription', mp_home, name='mp_home'),
    url(r'^vip', mp_home, name='mp_home'),

]
