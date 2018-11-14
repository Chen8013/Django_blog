from django.shortcuts import render, get_object_or_404

# Create your views here.
from .models import Post, Category, Tag
import markdown
from django.views.generic import ListView, DetailView

from django.db.models.aggregates import Count

def detail(request, slug):
    post = get_object_or_404(Post,slug=slug)
    post.inrease_views()
    post.body = markdown.markdown(post.body,extensions=['markdown.extensions.extra','markdown.extensions.codehilite','markdown.extensions.toc',])
    return render(request, 'blog/detail.html', context={'post':post})

class TagView(ListView):
    model = Post
    template_name = 'blog/columns.html'
    context_object_name = "post_list"

    def get_queryset(self):
        slug = self.kwargs.get('slug')
        cate = get_object_or_404(Tag, slug=slug)
        return super(TagView, self).get_queryset().filter(tags=cate)

class IndexView(ListView):
    model = Post
    template_name = 'blog/index.html'
    context_object_name = 'post_list'
    paginate_by = 15

    # def get_queryset(self):
    #     post_list = Post.objects.all()
    #     for post in post_list:
    #         post.body = markdown.markdown(post.body, extras=['fenced-code-blocks'], )
    #     return post_list
    #
    # def get_context_data(self, **kwargs):
    #     kwargs['category_list'] = Category.objects.all().order_by('name')
    #     # 调用 archive 方法，把获取的时间列表插入到 context 上下文中以便在模板中渲染
    #     kwargs['date_archive'] = Post.objects.archive()
    #     kwargs['tag_list'] = Tag.objects.all().order_by('name')
    #     return super(IndexView, self).get_context_data(**kwargs)


class DetailView(ListView):
    model = Post
    template_name = 'blog/detail.html'
    context_object_name = 'post'

    def get_object(self, queryset=None):
        obj = super().get_object(queryset=queryset)
        obj.viewed()
        return obj

class CategoryView(ListView):
    model = Post
    template_name = 'blog/columns.html'
    context_object_name = 'post_list'

    def get_queryset(self):
        slug = self.kwargs.get('slug')
        cate = get_object_or_404(Category, slug=slug)
        return super(CategoryView, self).get_queryset().filter(category=cate)

class PostDetailView(DetailView):
    # 这些属性的含义和 ListView 是一样的
    model = Post
    template_name = 'blog/detail.html'
    context_object_name = 'post_list'

    def get(self, request, *args, **kwargs):
        # 覆写 get 方法的目的是因为每当文章被访问一次，就得将文章阅读量 +1
        # get 方法返回的是一个 HttpResponse 实例
        # 之所以需要先调用父类的 get 方法，是因为只有当 get 方法被调用后，
        # 才有 self.object 属性，其值为 Post 模型实例，即被访问的文章 post
        response = super(PostDetailView, self).get(request, *args, **kwargs)

        # 将文章阅读量 +1
        # 注意 self.object 的值就是被访问的文章 post
        self.object.increase_views()

        # 视图必须返回一个 HttpResponse 对象
        return response

    def get_object(self, queryset=None):
        # 覆写 get_object 方法的目的是因为需要对 post 的 body 值进行渲染
        post = super(PostDetailView, self).get_object(queryset=None)
        post.body = markdown.markdown(post.body,
                                      extensions=[
                                          'markdown.extensions.extra',
                                          'markdown.extensions.codehilite',
                                          'markdown.extensions.toc',
                                      ])
        return post

def search(request):
    q = request.GET.get('q')
    error_msg = ''

    if not q:
        error_msg = '请输入关键词'
        return render(request, 'blog/errors.html', {'error_msg': error_msg})

    post_list = Post.objects.filter(title__icontains=q)
    return render(request, 'blog/index.html', {'error_msg': error_msg,
                                               'post_list': post_list})


class ArchiveView(ListView):
    template_name = "blog/index.html"
    context_object_name = "post_list"
    # context_object_name = "article_list"
    def get_queryset(self):
        # 接收从url传递的year和month参数，转为int类型
        year = int(self.kwargs['year'])
        if self.kwargs['month']:
            month = int(self.kwargs['month'])
        # 按照year和month过滤文章
            article_list = Post.objects.filter(created_time__year=year, created_time__month=month)
        else:
            article_list = Post.objects.filter(created_time__year=year)
        # print(Post.objects.filter(created_time__year=2018, created_time__month=11))
        return article_list

    def get_context_data(self, **kwargs):
        # kwargs['date_archive'] = Post.objects.archive()
        return super(ArchiveView, self).get_context_data(**kwargs)

def page_not_found(request):
    return render_to_response('404.html')

