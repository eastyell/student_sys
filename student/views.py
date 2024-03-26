import csv
import os
import time

from django.db import connection
from django.http import HttpResponseRedirect, HttpResponse
from django.urls import reverse
from django.views import View
from django.core.paginator import Paginator

from student_sys import settings
from users.forms import TitleSearch
from .forms import StudentForm
from .models import Student


# Create your views here.
def get_context(request, name=None):
    if name:
        students = Student.objects.filter(name__icontains=name)
    else:
        students = Student.get_all()
    paginator = Paginator(students, 3)
    num_p = request.GET.get('page', 1)
    page = paginator.page(int(num_p))
    context = {
        'students': students,
        'paginator': paginator,
        'page': page,
    }
    return context


class IndexView(View):
    template_name = 'index.html'

    def get(self, request):
        context = get_context(request)
        form_search = TitleSearch()
        context.update({
            'form_search': form_search,
        })
        return render(request, self.template_name, context=context)

    def post(self, request):
        name = ''
        form_search = TitleSearch(request.POST)
        if form_search.is_valid():  # 第一步验证成功
            name = form_search.cleaned_data["name"]
        context = get_context(request, name)
        context.update({
            'form_search': form_search,
        })
        # print(form_search)
        return render(request, self.template_name, context=context)


def add_stu_view(request):
    template_name = 'student/add.html'
    if request.method == 'GET':
        context = get_context(request)
        form = StudentForm()
        context.update({
            'form': form,
        })
        return render(request, template_name, context=context)
    elif request.method == 'POST':
        form = StudentForm(request.POST)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect('/show_stu')
        else:
            return render(request, 'student/add.html', locals())
    return HttpResponse("学生条目信息增加功能")


def update_stu_view(request, student_id):
    student_id = int(student_id)
    try:
        student = Student.objects.get(id=student_id)
        # 通过 form 参数 instance 方法能够实例化该 form
        form = StudentForm(instance=student)
    except Exception as e:
        return HttpResponse('--没有找到任何学生信息---')
    if request.method == 'GET':
        return render(request, 'student/update.html', locals())
    elif request.method == 'POST':
        # name = request.POST.get('name')
        # sex = request.POST.get('sex')
        # profession = request.POST.get('profession')
        # email = request.POST.get('email')
        # qq = request.POST.get('qq')
        # phone = request.POST.get('phone')
        # name_count = Student.objects.filter(name=name).count()
        # print(name_count)
        # if name_count > 1:
        #     return HttpResponse('修改的姓名已经存在，不能重复！')
        # # 存储更新后的状态
        # student.name = name
        # student.sex = sex
        # student.profession = profession
        # student.email = email
        # student.phone = phone
        # 修改具体的信息
        form = StudentForm(request.POST, instance=student)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect('/show_stu')
        else:
            return render(request, 'student/update.html', locals())
    return HttpResponse("学生条目信息修改功能")


def delete_stu_view(request, student_id):
    student_id = int(student_id)
    try:
        student = Student.objects.get(id=student_id)
        form = StudentForm(instance=student)
    except Exception as e:
        print('get查询出现了异常没找到数据', e)
        return HttpResponse('这里没有任何书籍可以被删除')
    if request.method == "GET":
        return render(request, 'student/delete.html', locals())
    elif request.method == "POST":
        student.delete()
        return HttpResponseRedirect("/show_stu")
    return HttpResponse("学生条目信息删除功能")


def uplod_view(request):
    if request.method == 'POST':
        #使用request.FILES['myfile']获得文件流对象file
        # file = request.FILES['myfile']
        files = request.FILES.getlist('myfiles')
        #文件储存路径，应用settings中的配置，file.name获取文件名
        print([file.name for file in files])
        for file in files:
            filename = os.path.join(settings.MEDIA_ROOT, file.name)
             #写文件
            with open(filename, 'wb') as f:
                #file.file 获取文件字节流数据
                data = file.file.read()
                f.write(data)
            # return render(request, 'index.html', locals())
        return HttpResponse('成功保存了 %s 文件'%([file.name for file in files]))


def down_csv_view(request):
    # 生v成csv文本
    # 生成response的content-type头
    res = HttpResponse(content_type='text/csv')
    # 固定格式,添加 content-Disposition头，设置以附件方式下载，并给文件添加默认文件名
    res['Content-Disposition'] = 'attachment;filename="students.csv"'
    # 获取数据库中数据
    students = Student.objects.all()
    # 生成writer的写对象
    writer = csv.writer(res)
    # 写csv表头，即想要展示字段名
    writer.writerow(['name', 'sex', 'profession'])
    # 写具体数据
    for student in students:
        writer.writerow([student.name, student.sex, student.profession])
    return res


def page_student(request):
    student = Student.objects.all()
    paginator = Paginator(student, 3)
    num_p = request.GET.get('page', 1)
    page = paginator.page(int(num_p))
    return render(request, 'index.html', locals())


# #方式一
# from django.template import loader # 导入loader方法
# from django.shortcuts import render #导入render 方法
#
# def test_html(request):
#     t=loader.get_template('test.html')
#     html=t.render({'name':'c语言中文网'})#以字典形式传递数据并生成html
#     return HttpResponse(html) #以 HttpResponse方式响应html


# 方式二
from django.shortcuts import render  # 导入reder方法


def test_html(request):
    test = {'name': 'c语言中文网'}
    return render(request, 'test.html', test)  # 根据字典数据生成动态模板


from django.template import Template, Context  # 调用template、以及上下文处理器方法


def Hello_MyWeb(request):
    # 调用template()方法生成模板
    t = Template("""
                    {% for k,v in test.items %}
                          {{k}}
                    {% endfor %}          
                    <p>列表长度:{{list|length}}</p>
                    {% for item in list|dictsort:'age' %}                         
                         <p><b>{{ forloop.counter }}: {{ item.name }} — {{ item.age }}</b></p>
                    {% empty %}
                        <h1>如果找不到你想要，可以来C语言中文网(网址：http://c.biancheng.net/)</h1>
                    {% endfor %}
                                      """)
    # 调用 Context()方法
    test = {'list': [{'name': 'Peter', 'age': 35}, {'name': 'Marry', 'age': 22},
                     {'name': 'Rose', 'age': 28}]}
    c = Context(test)  # Context必须是字典类型的对象，用来给模板传递数据
    html = t.render(c)
    return HttpResponse(html)


def test_tag(request):
    t = Template("""
                {% load index_tags%}
                {% mytag 'Django' as test %}
                {{test}}
                {% for name in webnames %}
                  {% ifchanged %}          
                  {{name.1|add:'ioe'}}
                  {% endifchanged %}
                {% endfor %}  
                
                {% for i in some_list %}
                  <tr class = "{%  cycle rowvalue1 rowvalue2%}">
                     <p> {{ i }} </p>
                {% endfor %}
                
                {% load index_tags %}
                <h1>{{ web|hello_my_filter }} </h1>
                
                <p>  {{ num|prefix }}</p>
                
                
                  """)
    # c = {'webnames':[['python', 'flask'], 'java', 'C']}
    # c = {'some_list': ['Python', 'Flask'], 'rowvalue1': 'row1', 'rowvalue2': 'row2'}
    # c = {'web': 'web django Django'}
    c = {'num': [2, 53, 23, 57, 28]}
    html = t.render(Context(c))
    return HttpResponse(html)


def self_tag(request):
    t = Template("""
                {% load index_tags%}
                {% add_webname_tag ' Django 测试' %}
                  """)
    c = Context({'varible': 'Hello'})
    html = t.render(c)
    return HttpResponse(html)


# 定义父模板视图函数
def base_html(request):
    return render(request, 'index/base.html')


# 定义子模板视图函数
def index_html(request):
    name = 'xiaoming'
    course = ['python', 'django', 'flask']
    students = Student.objects.raw('select * from student_student')
    with connection.cursor() as cur:
        cur.execute('delete from student_student where name="a"')

    return render(request, 'index/test.html', locals())


def redict_url(request):
    return render(request, 'index/newtest.html')


# reverse函数实现反向解析重定向到我们想要的有页面
def test_to_reverse(request):
    return HttpResponseRedirect(reverse('index:detail_hello'))
