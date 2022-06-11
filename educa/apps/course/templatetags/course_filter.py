from django import template

from educa.apps.course.models import CourseRelation
from educa.apps.rating.models import Rating
from educa.utils.utils import get_model

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
    return CourseRelation.objects.filter(course__id=course_id, user=user).exists()


@register.filter
def item_is_instance(item, class_name):
    return isinstance(item, get_model(class_name))


@register.filter()
def hasnt_rating(user, course):
    return not Rating.objects.filter(user=user, course=course).exists()


@register.filter()
def range_list(value):
    return [v for v in range(value)]


@register.filter()
def get_current_lesson(user, course):
    return CourseRelation.objects.filter(user=user, course=course).first().current_lesson


@register.filter()
def sort_order(query):
    return query.order_by('order')


@register.filter()
def user_liked(user, question):
    return question.user_likes.filter(id=user.id).exists()


@register.filter()
def get_rating_stars(avg):
    stars = []
    avg = float(avg)
    avg_int = int(avg)
    for n in range(avg_int):
        stars.append('i')
    if avg - avg_int >= .5:
        stars.append('m')
    return stars


@register.filter()
def get_rating_stars_empty(value):
    stars = []
    for n in range(1, 6):
        if value >= n:
            stars.append('i')
        else:
            stars.append('v')
    return stars


@register.filter()
def get_social_url(user, social):
    return getattr(user, social.lower())


@register.filter()
def get_rating_course(user, course):
    return Rating.objects.filter(user=user, course=course).first().rating


@register.filter()
def cut_word(word, size):
    if len(word) > size:
        return f'{word[:size]}...'
    return word


@register.filter()
def is_instructor(user, course):
    return user in course.instructors.all()
