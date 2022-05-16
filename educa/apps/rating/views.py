from django.urls import reverse_lazy
from django.views.generic import CreateView

from educa.apps.course.models import Course
from educa.apps.rating.models import Rating


class RatingCreateView(CreateView):
    template_name = 'rating/create.html'
    model = Rating
    fields = ('rating', 'comment')
    success_url = reverse_lazy('student:courses')

    def form_valid(self, form):
        form.instance.user = self.request.user
        form.instance.course = Course.objects.get(pk=self.kwargs.get('course_id'))
        return super().form_valid(form)
