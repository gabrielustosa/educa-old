from django.forms import modelform_factory
from django.shortcuts import get_object_or_404, render
from django.urls import reverse_lazy
from django.views.decorators.http import require_POST
from django.views.generic import CreateView

from educa.apps.course.models import Course
from educa.apps.rating.models import Rating


def rating_view(request, course_id):
    course = get_object_or_404(Course, id=course_id)
    ratings = Rating.objects.filter(course=course)
    return render(request, 'hx/rating/rating.html', context={'ratings': ratings, 'course': course})


def rating_render_create_view(request, course_id):
    course = get_object_or_404(Course, id=course_id)
    form = modelform_factory(Rating, fields=('rating', 'comment'))
    return render(request, 'hx/rating/render/create.html', context={'form': form, 'course': course})


@require_POST
def rating_create_view(request, course_id):
    course = get_object_or_404(Course, id=course_id)

    rating = request.POST.get('rating')
    comment = request.POST.get('comment')
    Rating.objects.create(rating=rating, comment=comment, user=request.user, course=course)

    return rating_view(request, course_id)
