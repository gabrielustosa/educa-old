from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.views.generic import TemplateView, CreateView


class ContentCreateView(
    LoginRequiredMixin,
    PermissionRequiredMixin,
    CreateView
):
    ...
    # template_name = 'content/create.html'
    # model = Content
    # fields = ['subject', 'title', 'description', 'image']
    # success_url = reverse_lazy('course:mine')
    # permission_required = 'content.add_content'
    #
    # def get_module(self):
    #     module = get_object_or_404(Module, id=self.kwargs.get('module_id'))
    #     return module
    #
    # def form_valid(self, form):
    #     form.instance.module = self.get_module()
    #     return super().form_valid(form)
