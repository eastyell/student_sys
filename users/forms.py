from django import forms


class TitleSearch(forms.Form):
    name = forms.CharField(label='学生姓名：', label_suffix='',
                           error_messages={'required': '请输入正确的name'})