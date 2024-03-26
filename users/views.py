import hashlib

from django.shortcuts import render
from django.http import HttpResponseRedirect, HttpResponse
from users.models import User
from users.signal import login_signal


# def hello_my_signal(request):
#     # 注意要和回调函数中的**kwargs的参数保持一致
#     # 参数 sender（信号发送者指函数） **named（**kwargs参数相同）
#     login_signal.send(hello_my_signal, request=request, user=User.objects.get(username="admin"))
#     print("注册成功已经发送邮件")
#     return HttpResponse('Hello signal')


# Create your views here.
# 用户的登录逻辑处理
def login_view(request):
    #处理GET请求
    if request.method == 'GET':
        #1, 首先检查session，判断用户是否第一次登录，如果不是，则直接重定向到首页
        if 'username' in request.session:  #request.session 类字典对象
            return HttpResponseRedirect('/show_stu')
        #2, 然后检查cookie，是否保存了用户登录信息
        if 'username' in request.COOKIES:
            #若存在则赋值回session，并重定向到首页
            request.session['username'] = request.COOKIES['username']
            return HttpResponseRedirect('/show_stu')
        #不存在则重定向登录页，让用户登录
        return render(request, 'user/login.html')
    # 处理POST请求
    elif request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        m = hashlib.md5()
        m.update(password.encode())
        password_m = m.hexdigest()
        #判断输入是否其中一项为空或者格式不正确
        if not username or not password:
            error = '你输入的用户名或者密码错误 !'
            return render(request, 'user/login.html', locals())
        #若输入没有问题则进入数据比对阶段，看看已经注册的用户中是否存在该用户
        users = User.objects.filter(userName=username, passWord=password_m)
        print(username,password_m)
        # 由于使用了filter, 所以返回值user是一个数组，但是也要考虑其为空的状态，即没有查到该用户
        if not users:
            error = '用户不存在或用户密码输入错误!!'
            return render(request, 'user/login.html', locals())
        # 返回值是个数组，并且用户名具备唯一索引，当前用户是该数组中第一个元素
        users = users[0]
        request.session['username'] = username
        # 参数 sender（信号发送者指函数） **named（**kwargs参数相同）
        login_signal.send(login_view, request=request, user=User.objects.get(userName=username))
        response = HttpResponseRedirect('/show_stu')
        #检查post 提交的所有键中是否存在 isSaved 键
        if 'isSaved' in request.POST.keys():
            #若存在则说明用户选择了记住用户名功能，执行以下语句设置cookie的过期时间
            response.set_cookie('username', username, 60*60*24*7)
        return response


def logout_view(request):
    #实现退出功能
    #删除session
    if 'username' in request.session:
        del request.session['username']
    resp = HttpResponseRedirect('/login')
    #删除cookie
    if 'username' in request.COOKIES:
        resp.delete_cookie('username')
    return resp


def reg_view(request):
    #用户注册逻辑代码
    if request.method == 'GET':
        return render(request, 'user/register.html')
    elif request.method == 'POST':
        #处理提交数据
        username = request.POST.get('username')
        print(username)
        if not username:
            username_error = '请输入正确的用户名'
            return render(request, 'user/register.html', locals())
        password_1 = request.POST.get('password_1')
        #1 生成hash算法对象对密码进行加密
        m = hashlib.md5()
        #2 对待加密明文使用update方法！要求输入明文为字节串root
        m.update(password_1.encode())
        #3 调用对象的 hexdigest[16进制],通常存16进制
        password_m1 = m.hexdigest()
        print(password_m1)#加密后的密文会显示在终端上
        password_2 = request.POST.get('password_2')
        #对password_2执行MD5加密处理
        m = hashlib.md5()
        m.update(password_2.encode())
        password_m2 = m.hexdigest()
        print(password_m2)
        #可以设定密码格式，判断是都符合
        if not password_m1 or not password_m2:
            password_1_error = '请输入正确的密码'
            return render(request, 'user/register.html', locals())
         #判断两次密码输入是否一致
        if password_m1 != password_m2:
            password_2_error = '两次密码不一致'
            return render(request, 'user/register.html', locals())
        #查询用户名是否已注册过
        try:
            old_user = User.objects.get(userName=username)
            print(old_user)
            #当前用户名已被注册
            username_error = '用户已经被注册 !'
            return render(request, 'user/register.html', locals())
        except Exception as e:
            # 若没查到的情况下进行报错，则证明当前用户名可用
            print('%s是可用用户名--%s'%(username, e))
            try:
                user = User.objects.create(userName=username, passWord=password_m1)
                #注册成功后
                html = '''
                注册成功 点击<a href='/'>进入首页</a>
                '''
                #存session
                request.session['username'] = username
                return HttpResponse(html)
            #若创建不成功会抛出异常
            except Exception as e:
                # 还可能存在用户名被重复使用的情况
                print(e)
                username_error = '该用户名已经被占用 '
                return render(request, 'user/register.html', locals())