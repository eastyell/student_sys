"""student_sys URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the incluide function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, re_path, include

from student import views as stu_views
from users import views as user_view

urlpatterns = [
    path('admin/', admin.site.urls),
    # re_path(r'^$', stu_views.IndexView.as_view(), name='index'),
    re_path(r'^$', user_view.login_view, name='login'),
    path('test/', stu_views.test_html),
    path('Hello_MyWeb/', stu_views.Hello_MyWeb, name='hello'),
    path('test_tag/', stu_views.test_tag, name='my_tag'),
    path('self_tag/', stu_views.self_tag, name='self_tag'),
    path('index/', include('student.urls')),
    path('redict/', stu_views.redict_url),
    path('reverse/', stu_views.test_to_reverse),
    path('reg/', user_view.reg_view),
    path('login/', user_view.login_view),
    path('logout/', user_view.logout_view),
    path('show_stu/', stu_views.IndexView.as_view(), name='index'),
    path('add_stu/', stu_views.add_stu_view),
    path('update_stu/<int:student_id>', stu_views.update_stu_view),
    path('delete_stu/<int:student_id>', stu_views.delete_stu_view),
    path('upload/', stu_views.uplod_view),
    path('down_csv_view/', stu_views.down_csv_view),

]
