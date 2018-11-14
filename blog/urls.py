from django.conf.urls import re_path
from . import views
# from blog.views import page_not_found
from django.views.static import serve
from firstsite import settings

app_name = 'blog'
urlpatterns = [
    re_path(r'^$', views.IndexView.as_view(), name='index'),
    re_path(r'^post/(?P<slug>(.*))$', views.detail, name='detail'),
    re_path(r'^archives/(?P<year>[0-9]{4})?/(?P<month>[0-9]{1,2})?$', views.ArchiveView.as_view(), name='archives'),
    re_path(r'^category/(?P<slug>(.*))/$', views.CategoryView.as_view(), name='category'),
    re_path(r'^tag/(?P<slug>(.*))/$', views.TagView.as_view(), name='tag'),
    re_path(r'^media/(?P<path>.*)$', serve, {'document_root': settings.MEDIA_ROOT})
    # re_path(r'^search/$', views.search, name='search'),
]

# handler404 = page_not_found