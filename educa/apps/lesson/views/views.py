import json

from braces.views import CsrfExemptMixin
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import JsonResponse
from django.views.generic import TemplateView

from educa.apps.lesson.models import Lesson, LessonRelation
from educa.mixin import InstructorRequiredMixin, CacheMixin, HTMXRequireMixin


class LessonOrderView(
    HTMXRequireMixin,
    LoginRequiredMixin,
    InstructorRequiredMixin,
    CacheMixin,
    TemplateView,
):
    template_name = 'hx/lesson/sortable.html'
    http_method_names = ['post']

    def post(self, request, *args, **kwargs):
        context = super().get_context_data(**kwargs)

        lessons_list = request.POST.getlist('lesson')

        order_list = [Lesson.objects.get(id=lesson).order for lesson in lessons_list]

        lesson_start = int(min(order_list))

        for order, lesson_id in enumerate(lessons_list, start=lesson_start):
            Lesson.objects.filter(id=lesson_id).update(order=order)

        context['lessons'] = Lesson.objects.filter(module=self.get_module()).order_by('order').all()

        return self.render_to_response(context)

    def get_course(self):
        return self.get_module().course


class LessonCheckView(
    CsrfExemptMixin,
    LoginRequiredMixin,
    TemplateView,
):
    http_method_names = ['post']

    def post(self, request, *args, **kwargs):
        response_json = json.load(self.request)
        check = response_json.get('check')
        lesson_id = response_json.get('lesson_id')
        lesson = Lesson.objects.get(id=lesson_id)

        if LessonRelation.objects.filter(user=self.request.user, lesson=lesson).exists():
            LessonRelation.objects.filter(user=self.request.user, lesson=lesson).update(done=check)
        else:
            LessonRelation.objects.create(lesson=lesson, user=request.user, done=check)

        total = LessonRelation.objects.filter(user=request.user, lesson__course=lesson.course, done=True).count()
        return JsonResponse({'total': total})
