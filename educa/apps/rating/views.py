from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.cache import cache
from django.forms import modelform_factory
from django.http import HttpResponse
from django.shortcuts import get_object_or_404, render
from django.views.generic import TemplateView

from educa.apps.course.models import Course
from educa.apps.rating.models import Rating
from educa.utils import render_error


def rating_view(request, course_id):
    course = cache.get(f'course-{course_id}')
    if not course:
        course = Course.objects.filter(id=course_id).first()
        cache.set(f'course-{course_id}', course)
    ratings = Rating.objects.filter(course=course)
    return render(request, 'hx/rating/rating.html', context={'ratings': ratings, 'course': course})


class RatingRenderCreateView(
    LoginRequiredMixin,
    TemplateView,
):
    template_name = 'hx/rating/render/create.html'

    def get_course(self):
        course_id = self.kwargs.get('course_id')
        course = cache.get(f'course-{course_id}')
        if course:
            return course
        else:
            course = Course.objects.filter(id=course_id).first()
            cache.set(f'course-{course_id}', course)
            return course

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['course'] = self.get_course()
        context['form'] = modelform_factory(Rating, fields=('rating', 'comment'))
        return context


class RatingCreateView(
    LoginRequiredMixin,
    TemplateView,
):
    http_method_names = ['post']

    def get_course(self):
        course_id = self.kwargs.get('course_id')
        course = cache.get(f'course-{course_id}')
        if course:
            return course
        else:
            course = Course.objects.filter(id=course_id).first()
            cache.set(f'course-{course_id}', course)
            return course

    def post(self, request, *args, **kwargs):
        course = self.get_course()

        rating = request.POST.get('rating')
        comment = request.POST.get('comment')

        error_messages = []
        if not rating:
            error_messages.append('Você precisa escolher um número de 1 a 5 a sua avaliação.')
        if rating:
            if int(rating) > 5 or int(rating) < 1:
                error_messages.append('Você deve escolher um número de 1 a 5.')

        if len(comment) == 0:
            error_messages.append('O comentário da sua avaliação não pode estar vazio.')

        if error_messages:
            return HttpResponse(render_error(error_messages), status=400)

        Rating.objects.create(rating=rating, comment=comment, user=request.user, course=course)

        return rating_view(request, course.id)
