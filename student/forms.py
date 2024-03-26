from django import forms

from .models import Student


class StudentForm(forms.ModelForm):
    def clean_qq(self):
        cleaned_data = self.cleaned_data['qq']
        if not cleaned_data.isdigit():
            raise forms.ValidationError('必须是数字！')
        return int(cleaned_data)

    def clean_name(self):
        cleaned_data = self.cleaned_data['name']
        if self.has_changed():
            name_count = Student.objects.filter(name=cleaned_data).count()
            if name_count > 0:
                raise forms.ValidationError('修改的姓名已经存在，不能重复！')
        return cleaned_data

    # your_field = forms.ModelChoiceField(queryset=Category.objects.all())

    class Meta:
        model = Student
        fields = (
            'name', 'sex', 'profession',
            'email', 'qq', 'phone', 'status'
        )
        labels = {
            'sex': '性别',
        }
        widgets = {
            'sex': forms.Select(choices=Student.SEX_ITEMS),
        }
