from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.shortcuts import get_object_or_404, render
from django.urls import reverse_lazy
from django.utils.functional import cached_property
from django.views.decorators.csrf import csrf_exempt
from django.views.generic import TemplateView, CreateView, DeleteView, UpdateView

from educa.apps.content.models import Content
from educa.apps.lesson.models import Lesson
from educa.apps.mixin import CourseOwnerMixin
from educa.apps.module.models import Module
from educa.utils import content_is_instance



@csrf_exempt
def lesson_order_view(request, module_id):
    module = Module.objects.get(id=module_id)
    lessons = request.POST.getlist('lesson')
    for order, lesson_id in enumerate(lessons, start=1):
        Lesson.objects.filter(id=lesson_id).update(order=order)
    return render(request, 'hx/lesson/sortable.html',
                  context={'lessons': Lesson.objects.filter(module=module).order_by('order').all()})


def lesson_content_view(request, lesson_id, class_name):
    lesson = Lesson.objects.get(id=lesson_id)
    contents = []
    for content in lesson.contents.all():
        if content_is_instance(content, class_name):
            contents.append(content)
    return render(request, 'hx/lesson/dynamic_content.html', context={'contents': contents, 'lesson': lesson})
