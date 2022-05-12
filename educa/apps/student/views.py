from django.contrib.auth import authenticate, login
from django.urls import reverse_lazy
from django.views.generic import CreateView, TemplateView

from educa.apps.course.models import Course
from educa.apps.student.forms import UserCreateForm


class StudentRegisterView(CreateView):
    template_name = 'registration/register.html'
    form_class = UserCreateForm
    success_url = reverse_lazy('student:list')

    def form_valid(self, form):
        result = super().form_valid(form)
        cd = form.cleaned_data
        user = authenticate(
            username=cd['username'],
            password=cd['password1']
        )
        login(user)
        return result


class StudentCoursesView(TemplateView):
    template_name = 'student/course_list.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        context['courses'] = Course.objects.filter(students=self.request.user)

        return context
