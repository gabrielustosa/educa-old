from django.forms import modelform_factory
from django.shortcuts import render, get_object_or_404
from django.views.decorators.http import require_POST

from educa.apps.course.models import Course
from educa.apps.notice.models import Notice


def notice_view(request, course_id):
    course = get_object_or_404(Course, id=course_id)
    notices = Notice.objects.filter(course=course)
    return render(request, 'hx/notice/view.html', context={'notices': notices, 'course': course})


def notice_render_create_form_view(request, course_id):
    course = get_object_or_404(Course, id=course_id)
    form = modelform_factory(Notice, fields=('title', 'content'))
    return render(request, 'hx/notice/render/create.html', context={'form': form, 'course': course})


@require_POST
def notice_create_view(request, course_id):
    course = get_object_or_404(Course, id=course_id)

    title = request.POST.get('title')
    content = request.POST.get('content')

    Notice.objects.create(course=course, title=title, content=content)

    return notice_view(request, course_id)


def notice_render_update_form_view(request, notice_id):
    notice = get_object_or_404(Notice, id=notice_id)

    form = modelform_factory(Notice, fields=('title', 'content'))
    form = form(instance=notice)

    return render(request, 'hx/notice/render/update.html', context={'form': form, 'notice': notice})


def notice_update_view(request, notice_id):
    notice = get_object_or_404(Notice, id=notice_id)

    title = request.POST.get('title')
    content = request.POST.get('content')

    notice.title = title
    notice.content = content
    notice.save()

    return notice_view(request, notice.course.id)


def notice_confirm_view(request, notice_id):
    notice = get_object_or_404(Notice, id=notice_id)

    return render(request, 'hx/modal.html',
                  context={'title': 'Confirmação',
                           'content': 'Você tem certeza que deseja deletar seu aviso?',
                           'confirm': True,
                           'notice': notice})


def notice_delete_view(request, notice_id):
    notice = get_object_or_404(Notice, id=notice_id)

    notice.delete()

    return notice_view(request, notice.course.id)
