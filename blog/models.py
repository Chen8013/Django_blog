from django.db import models
from datetime import datetime
from django.contrib.auth.models import User

from django.urls import reverse
from django.utils.six import python_2_unicode_compatible

from mdeditor.fields import MDTextField
import collections

from unidecode import unidecode
from django.template.defaultfilters import slugify

# Create your models here.
@python_2_unicode_compatible
class Category(models.Model):
    name = models.CharField(max_length=20)
    def __str__(self):
        return self.name

    #title link style
    slug = models.SlugField('slug', max_length=60, blank=True)
    def save(self, *args, **kwargs):
        if not self.id or not self.slug:
            # Newly created object, so set slug
            self.slug = slugify(unidecode(self.name))

        super(Category, self).save(*args, **kwargs)

@python_2_unicode_compatible
class Tag(models.Model):
    name =models.CharField(max_length=20)
    def __str__(self):
        return self.name

    #title link style
    slug = models.SlugField('slug', max_length=60, blank=True)
    def save(self, *args, **kwargs):
        if not self.id or not self.slug:
            # Newly created object, so set slug
            self.slug = slugify(unidecode(self.name))

        super(Tag, self).save(*args, **kwargs)

# @python_2_unicode_compatible
# class ArticleManage(models.Manager):
#     """
#     继承自默认的 Manager ，为其添加一个自定义的 archive 方法
#     """
#     def archive(self):
#         date_list = Post.objects.datetimes('created_time', 'month', order='DESC')
#         # 并把列表转为一个字典，字典的键为年份，值为该年份下对应的月份列表
#         date_dict = collections.defaultdict(list)
#         for d in date_list:
#             date_dict[d.year].append(d.month)
#         # 模板不支持defaultdict，因此我们把它转换成一个二级列表，由于字典转换后无序，重新降序排序
#         return sorted(date_dict.items(), reverse=True)


@python_2_unicode_compatible
class Post(models.Model):
    # objects = ArticleManage()
    #记录阅读量
    views = models.PositiveIntegerField(default=0)
    def inrease_views(self):
        self.views +=1
        self.save(update_fields=['views'])

    title = models.CharField('标题', max_length=200, unique=True)
    #文章内容
    body = MDTextField()
    #创建时间
    created_time = models.DateTimeField('创建时间', auto_now_add=True)
    #更新时间
    modified_time = models.DateTimeField('更新时间', auto_now=True)
    #文章摘要
    excerpt = models.CharField(max_length=200, blank=True)
    #外键关联分类：多对一
    category = models.ForeignKey(Category,on_delete=models.CASCADE)
    #文章关联标签：多对多
    tags = models.ManyToManyField(Tag)
    image = models.ImageField(upload_to="image/%Y/%m", blank=True)
    #title link style
    slug = models.SlugField('slug', max_length=60, blank=True)

    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        if not self.id or not self.slug:
            # Newly created object, so set slug
            self.slug = slugify(unidecode(self.title))

        super(Post, self).save(*args, **kwargs)

    def get_absolute_url(self):
        return reverse('blog:detail', kwargs={'slug': self.slug})

    class Meta:
        ordering = ['-created_time']


