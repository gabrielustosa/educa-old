from django import template

from educa.apps.course.models import Course
from educa.apps.rating.models import Rating
from educa.utils import content_is_instance, get_model

register = template.Library()


@register.filter
def model_name(obj):
    try:
        return obj._meta.model_name
    except AttributeError:
        return None


@register.filter
def model_verbose(obj):
    try:
        return obj._meta.verbose_name
    except AttributeError:
        return None


@register.filter
def student_is_enrolled(user, course_id):
    if user.is_anonymous:
        return False
    return Course.objects.filter(id=course_id).filter(students=user).exists()


@register.filter
def item_is_instance(item, class_name):
    return isinstance(item, get_model(class_name))


@register.filter()
def hasnt_rating(user, course):
    return not Rating.objects.filter(user=user, course=course).exists()


@register.filter()
def range_list(value):
    return [v for v in range(value)]
