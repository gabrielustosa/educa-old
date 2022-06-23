from django import template

from educa.apps.course.models import CourseRelation
from educa.apps.lesson.models import LessonRelation
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
def get_module_lessons(lessons, module):
    module_lessons = []
    for lesson in lessons:
        if lesson.module == module:
            module_lessons.append(lesson)
    return module_lessons


@register.filter()
def user_liked(user, question):
    return question.user_likes.filter(id=user.id).exists()


@register.filter()
def get_rating_stars(avg):
    stars = []
    if not avg:
        avg = 0
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
    return course.instructors.filter(id=user.id).exists()


@register.filter()
def get_only_hour(seconds):
    if not seconds:
        seconds = 1
    return round(seconds / 3600)


@register.filter()
def format_time(seconds):
    if not seconds:
        seconds = 1
    h = round(seconds / 3600)
    m = round(seconds % 3600 / 60)
    s = seconds % 60

    result = ''
    if h > 0:
        result += f'{h} h '
    if m > 0:
        result += f'{m} m '
    if result == '' and s > 0:
        result = f'{s} s '
    return result


@register.filter()
def format_time_counter(seconds):
    seconds = int(seconds)

    def pad(x):
        return int(f'0{x}') if x < 10 else x

    h = pad(round(seconds / 3600))
    m = pad(round(seconds % 3600 / 60))
    s = pad(seconds % 60)

    result = ''
    if h > 0:
        result += f'{+h}:'
    i = m if h > 0 else +m
    result += f'{i}'
    if s > 0:
        result += f':{s}'

    return result.split('.')[0]


@register.filter()
def user_done_lesson(user, lesson):
    return LessonRelation.objects.filter(user=user, lesson__id=lesson.id, done=True).exists()


@register.filter()
def get_total_lessons_done_by_module(relations, module):
    count = 0
    for relation in relations:
        if relation.lesson.module == module and relation.done:
            count += 1
    return count


@register.filter()
def lesson_is_done(relations, lesson):
    for relation in relations:
        if relation.lesson == lesson:
            return relation.done
    return False


@register.filter()
def get_total_lessons_done_by_course(relations):
    count = 0
    for relation in relations:
        if relation.done:
            count += 1
    return count


@register.filter()
def replace_dot(replace):
    return replace.replace(',', '.')


@register.filter()
def get_rating_bars(course):
    ratings = course.ratings

    ranting_dict = {5: 0, 4: 0, 3: 0, 2: 0, 1: 0}
    numbers_rating = [1, 2, 3, 4, 5]
    for number in numbers_rating:
        for rating in ratings.all():
            if int(rating.rating) == number:
                ranting_dict[int(rating.rating)] = ranting_dict.get(int(rating.rating)) + 1

    result = {}

    for k, v in ranting_dict.items():
        try:
            operation = v / len(ratings.all()) * 100
        except ZeroDivisionError:
            operation = 0
        result[k] = "{:.2f}".format(operation)

    return result.items()
