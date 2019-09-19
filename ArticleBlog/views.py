from django.http import HttpResponse
from django.shortcuts import render
from Article.models import *

def hello(request):
    return HttpResponse('hello')

# 登录拦截装饰器
def loginVaild(fun):
    def inner(request,*args,**kwargs):
        username = request.COOKIES.get('name')
        password = request.COOKIES.get('password')
        if username and password:
            return fun(request, *args, **kwargs)
        else:
            return HttpResponseRedirect('/login/')
    return inner

@loginVaild
def about(request):
    return render(request,'about.html')

@loginVaild
def index(request):
    article = Article.objects.order_by('-date')[:6]
    recommend_article = Article.objects.filter(recommend=1)[:7]
    click_article = Article.objects.order_by('-click')[:12]

    return render(request,'index.html',locals())

def listpic(request):
    return render(request,'listpic.html')

def newslistpic(request,type='个人日记',page=1):
    # article = Article.objects.order_by('-date')
    article=Type.objects.get(name=type).article_set.order_by('-date')
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
        print(one.title)

    print(page.number)    # 5，当前页
    print(page.has_next())    # 是否有下一页
    print(page.has_previous())    # 是否有上一页
    print(page.has_other_pages())    # 是否有其他页
    print(page.next_page_number())    # 下一页的页码，如果没有，抛异常
    print(page.previous_page_number())    # 上一页的页码，如果没有，抛异常

    author = Author.objects.all().first()
    print(author.gender)    # 1
    print(author.get_gender_display())    # 男

    return HttpResponse('分页功能测试')

def reqtest(request):
    # 获取get请求的请求参数
    # data = request.GET
    # print(data)
    # return HttpResponse('姓名：%s,年龄：%s'%(data.get('name'),data.get('age')))

    # 获取post请求的请求参数
    data = request.POST
    print(data)
    return HttpResponse('姓名：%s,年龄：%s' % (data.get('name'), data.get('age')))

    # request--一个包含请求信息的请求对象
    # print(request)    # <WSGIRequest: GET '/reqtest/'>
    # # print(dir(request))
    # print(request.COOKIES)
    # print(request.FILES)
    # print(request.GET)
    # print(request.POST)
    # print(request.scheme)
    # print(request.method)
    # print(request.path)
    # print(request.body)
    # meta = request.META    # 字典
    # for key in meta:
    #     print(key)
    # print('-------------------------------')
    # print(request.META['OS'])
    # print(request.META['HTTP_USER_AGENT'])
    # print(request.META['HTTP_HOST'])
    # print(request.META.get('HTTP_REFERER'))
    # return HttpResponse('请求测试')

def formtest(request):
    # data = request.GET
    # search = data.get('search')
    # print(search)
    # print(type(search))    # <class 'str'>
    #
    # # 通过form表单提交的数据，判断数据库中是否存在某个文章，模糊查询
    # if search:
    #     article= Article.objects.filter(title__contains=search)

    data = request.POST
    print(data.get('username'))
    print(data.get('password'))

    return render(request,'formtest.html',locals())

import hashlib
def setPassword(password):
    # 实现密码加密
    md5 = hashlib.md5()    # 创建一个md5的实例对象
    md5.update(password.encode())    # 进行加密
    result = md5.hexdigest()
    return result

from Article.forms import Register
# 使用form表单进行后端验证
def register(request):
    register_form = Register()
    print(register_form)
    for one in register_form:
        print(one.label)
        print(one)
    # print(request.body)    # b'csrfmiddlewaretoken=qm8Epoc7Q6fW34bsSUYIOpTcIv4huQI7tEfdgt9KCH3HgRTh6eiK5NUVYj2pfS20&name=123&password=123456'
    if request.method == 'POST':
        # 获取数据
        data = Register(request.POST)
        # 校验是否通过 通过True，否则False
        if data.is_valid():
            # 返回一个字典类型，通过校验的数据
            clean_data=data.cleaned_data
            print(clean_data)
            # 获取到数据，写库
            username=clean_data.get('name')
            password=clean_data.get('password')
            user = User()
            user.name=username
            user.password=setPassword(password)
            user.save()
            result = '注册成功'
        else:
            result=data.errors
            # print(result)

    return render(request,'register.html',locals())

# 登录，重定向
from django.http import HttpResponseRedirect
def login(request):
    if request.method == 'POST':
        username=request.POST.get('username')
        password=setPassword(request.POST.get('password'))
        if username:
            user = User.objects.filter(name=username).first()
            if user:    # 用户存在
                if user.password==password:    # 密码正确
                    # 跳转首页
                    response = HttpResponseRedirect('/index/')
                    response.set_cookie('name',username)
                    response.set_cookie('password',password)
                    request.session['username']=username
                    return response
                else:
                    error_msg = '密码错误'
            else:
                error_msg = '该用户不存在，请先注册'
        else:
            error_msg = '用户名不可为空'
    return render(request,'login.html',locals())

# 登出，删除cookie
def logout(request):
    response=HttpResponseRedirect('/login/')
    response.delete_cookie('name')
    response.delete_cookie('password')
    # 删除指定session，删除的session是保存在服务器上面session的值
    # 目的是，用户再次使用相同的sessionid进行访问时，拿到的session值是不同的
    del request.session['username']
    # 删除所有的session
    # request.session.flush()

    return response

def ajax_get(request):
    return render(request,'ajax_get.html')

from django.http import JsonResponse
# 查找数据库，判断是否可登录
def ajax_get_data(request):
    result = {'code':10000,'content':''}
    data = request.GET
    username = data.get('username')
    password = data.get('password')
    if username=='' or password=='':
        result['code'] = 10001
        result['content'] = '请求参数为空'
    else:
        user = User.objects.filter(name=username,password=setPassword(password)).first()
        if user:
            result['code'] = 10000
            result['content'] = '用户可登录'
        else:
            result['code'] = 10002
            result['content'] = '用户名或密码错误'

    # 返回一个json对象
    return JsonResponse(result)    # 默认情况下，JsonResponse的传入参数是个字典类型
    # return HttpResponse('这是ajax提交数据')

def ajax_post(request):
    return render(request,'ajax_post.html')

# 注册
def ajax_post_data(request):
    result={'code':10000,'content':''}
    username=request.POST.get('name')
    password=request.POST.get('pwd')
    if username=='' or password=='':
        result['code'] = 10001
        result['content'] = '请补全数据'
    else:
        user = User()
        user.name = username
        user.password = setPassword(password)
        try:
            user.save()
            result['content'] = '注册成功'
        except:
            result['code'] = 10002
            result['content'] = '注册失败'

    return JsonResponse(result)

def checkusername(request):
    result={'code':10000,'content':''}
    username=request.GET.get('name')
    user=User.objects.filter(name=username).exists()
    if user:    # 存在
        result['code']=10001
        result['content']='用户名已存在'
    else:
        result['content']='该用户名可用'

    return JsonResponse(result)