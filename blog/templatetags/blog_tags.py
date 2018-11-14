from django import template
from ..models import Post, Category, Tag

register = template.Library()

#从数据库获取前num=篇文章
@register.simple_tag
def get_recent_posts(num=8):
    return Post.objects.all().order_by('-views')[:num]

#按时间归档模板标签
@register.simple_tag
def archives():
    return Post.objects.all().order_by('-created_time')
    # return Post.objects.archive()
    # return Post.objects.datetimes('created_time', 'month', order='DESC')

#分类模板标签
@register.simple_tag
def get_categories():
    return Category.objects.all()

from django.db.models.aggregates import Count
# Count 计算分类下的文章数，其接受的参数为需要计数的模型的名称
#标签模板标签
@register.simple_tag
def get_tags():
    return Tag.objects.annotate(num_posts=Count('post'))


