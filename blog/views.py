import markdown
from django.shortcuts import render,get_object_or_404
from .models import Post,Category
from django.http import HttpResponse
from comments.forms import CommentForm
from django.views.generic import ListView


#创建一个类视图
class IndexView(ListView):
    model=Post
    template_name = 'blog/index.html'
    context_object_name = 'post_list'


''' 被类视图取代
def index(request):
    post_list=Post.objects.all().order_by('-created_time')
    
    return render(request, 'blog/index.html',context={'post_list': post_list}) 
'''
# Create your views here.

def detail(request,pk):
    post=get_object_or_404(Post,pk=pk)
    
    #阅读量+1,引用这个方法。
    post.increase_views()
    
    post.body=markdown.markdown(post.body,
                                extensions=[
                                    'markdown.extensions.extra',
                                    'markdown.extensions.codehilite',
                                    'markdown.extensions.toc',
                                ])
    # 
    form = CommentForm()
    # 获取这篇 post 下的全部评论
    comment_list = post.comment_set.all()
    
    # 将文章、表单、以及文章下的评论列表作为模板变量传给 detail.html 模板，以便渲染相应数据。
    context = {'post': post,
               'form': form,
               'comment_list': comment_list
               }
    return render(request,'blog/detail.html', context=context)
        
def archives(request,year,month):
    '''post_list=Post.objects.all().order_by('-created_time')'''
    
    post_list=Post.objects.filter(created_time__year=year,
                                  created_time__month=month
                                  ).order_by('-created_time')
    
    return render(request, 'blog/index.html',context={'post_list': post_list})

def category(request, pk):
    # 记得在开始部分导入 Category 类
    cate = get_object_or_404(Category, pk=pk)
    post_list = Post.objects.filter(category=cate).order_by('-created_time')
    return render(request, 'blog/index.html', context={'post_list': post_list})    