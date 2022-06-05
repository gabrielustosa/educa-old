from django.contrib.auth import authenticate, login
from django.urls import reverse_lazy
from django.views.generic import CreateView, TemplateView

from educa.apps.student.forms import UserCreateForm, UserEditForm


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


class StudentEditProfileView(TemplateView):
    template_name = 'student/edit_profile.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        context['form'] = UserEditForm(instance=self.request.user)

        return context

    def post(self, request, *args, **kwargs):
        context = super().get_context_data(**kwargs)

        context['form'] = UserEditForm(instance=self.request.user)

        form = UserEditForm(request.POST, instance=request.user)
        if form.is_valid():
            form.save()

        return self.render_to_response(context)
