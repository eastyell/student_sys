from django.http import HttpResponseRedirect
from django.urls import reverse
from django.shortcuts import render
from django.views import View

from .forms import StudentForm
from .models import Student


# Create your views here.
def get_context():
    students = Student.get_all()
    context = {
        'students': students,
    }
    return context


class IndexView(View):
    template_name = 'index.html'

    def get(self, request):
        context = get_context()
        form = StudentForm()
        context.update({
            'form': form
        })
        return render(request, self.template_name, context=context)

    def post(self, request):
        form = StudentForm(request.POST)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect(reverse('index'))
        context = self.get_content()
        context.update({
            'form': form
        })
        return render(request, self.template_name, context=context)
