from django.contrib.auth import authenticate, login
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import Http404
from django.shortcuts import get_object_or_404
from django.urls import reverse_lazy
from django.views.generic import CreateView, TemplateView

from educa.apps.student.forms import UserCreateForm, UserEditForm
from educa.apps.student.models import User


class StudentRegisterView(CreateView):
    template_name = 'registration/register.html'
    form_class = UserCreateForm
    success_url = reverse_lazy('home')

    def form_valid(self, form):
        result = super().form_valid(form)
        cd = form.cleaned_data
        user = authenticate(
            username=cd['username'],
            password=cd['password1']
        )
        login(request=self.request, user=user)
        return result


class StudentEditProfileView(
    LoginRequiredMixin,
    TemplateView
):
    template_name = 'student/profile/edit.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        context['form'] = UserEditForm(instance=self.request.user)

        return context

    def post(self, request, *args, **kwargs):
        context = super().get_context_data(**kwargs)

        form = UserEditForm(request.POST, instance=request.user)
        if form.is_valid():
            form.save()

        context['form'] = form

        return self.render_to_response(context)


class StudentProfileView(TemplateView):
    template_name = 'student/profile/view.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        user = User.objects.filter(id=self.kwargs.get('user_id')).prefetch_related('courses_created').first()

        if not user:
            raise Http404()

        context['user'] = user

        return context
