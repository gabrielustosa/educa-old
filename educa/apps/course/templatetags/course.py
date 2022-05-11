from django import template

from educa.apps.course.models import Course

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
