from django.http import HttpResponse
from django.shortcuts import render
from Article.models import *

def hello(request):
    return HttpResponse('hello')

def about(request):
    return render(request,'about.html')

def index(request):
    article = Article.objects.order_by('-date')[:6]
    recommend_article = Article.objects.filter(recommend=1)[:7]
    click_article = Article.objects.filter(recommend=1)[:12]

    return render(request,'index.html',locals())

def listpic(request):
    return render(request,'listpic.html')

def newslistpic(request,page=1):
    article = Article.objects.order_by('-date')
    paginator = Paginator(article,6)    # 每页显示6条数据
    page_obj = paginator.page(int(page))
    # 获取当前页
    current_page = page_obj.number
    start = current_page-3
    end = current_page + 2
    if start < 1:
        start = 0
        end = 5
    if end > paginator.num_pages:
        start = paginator.num_pages-5
        end = paginator.num_pages
    page_range = paginator.page_range[start:end]

    return render(request,'newslistpic.html',locals())

def base(request):
    return render(request,'base.html')

def articledetails(request,id):
    article = Article.objects.get(id=int(id))
    return render(request,'articledetails.html',locals())

def addarticle(request):
    # for x in range(100):
    #     article = Article()
    #     article.title='title_%s' % x
    #     article.content='content_%s' % x
    #     article.description='description_%s' % x
    #     article.author=Author.objects.get(id=1)
    #     article.save()
    #     article.type.add(Type.objects.get(id=1))
    #     article.save()

    return HttpResponse('增加数据')

from django.core.paginator import Paginator

def pagetest(request):
    # 使用django自带分页Paginator的时候，源数据需要增加排序属性，否则会报异常
    article = Article.objects.all().order_by('-date')
    # 每次显示5条数据
    paginator = Paginator(article,5)    # 设置每页显示的数据条数，返回一个对象
    print(paginator.count)    # 返回内容总条数
    print(paginator.page_range)    # 可迭代页数范围
    print(paginator.num_pages)    # 返回最大页数
    page = paginator.page(5)
    print(page)    # <Page 5 of 21>，表示当前对象
    for one in page:
        print(one.content)

    print(page.number)    # 5，当前页
    print(page.has_next())    # 是否有下一页
    print(page.has_previous())    # 是否有上一页
    print(page.has_other_pages())    # 是否有其他页
    print(page.next_page_number())    # 下一页的页码，如果没有，抛异常
    print(page.previous_page_number())    # 上一页的页码，如果没有，抛异常

    return HttpResponse('分页功能测试')