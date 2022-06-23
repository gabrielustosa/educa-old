from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.exceptions import ObjectDoesNotExist
from django.db.models import Q, Count, Avg, Sum, Subquery, F
from django.http import HttpResponse, Http404
from django.views.generic import ListView, TemplateView

from educa.apps.course.models import Course
from educa.apps.student.models import User
from educa.mixin import InstructorRequiredMixin, CacheMixin, HTMXRequireMixin
from educa.utils.utils import render_error


class CourseListView(ListView):
    template_name = 'course/list.html'
    model = Course
    paginate_by = 6
    context_object_name = 'courses'

    def get_queryset(self):
        return Course.objects.annotate(rating_avg=Avg('ratings__rating')).all()


class CourseOwnerListView(
    LoginRequiredMixin,
    CourseListView,
):
    template_name = 'course/mine.html'

    def get_queryset(self):
        return self.request.user.courses_created.all()


class CourseDetailView(TemplateView):
    template_name = 'course/detail.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        course_id = self.kwargs.get('course_id')

        course_query = Course.objects.filter(id=course_id).annotate(
            rating_avg=Avg('ratings__rating'),
            total_video_duration=Subquery(
                Course.objects.filter(id=course_id).annotate(
                    total=Sum('lesson__video_duration')).values('total'),
            ),
        ).select_related('subject').prefetch_related('ratings', 'modules', 'lesson_set')

        course = course_query.first()

        if not course:
            raise Http404()

        modules = course.modules.prefetch_related('lessons').all()

        context['course'] = course
        context['ratings'] = course.ratings
        context['modules'] = modules

        context['instructors'] = course.instructors.annotate(
            total_courses=Subquery(
                User.objects.filter(id=F('id')).annotate(
                    total=Count('courses_created')).values('total'),
            ),
            total_rating=Subquery(
                User.objects.filter(id=F('id')).annotate(
                    total=Count('courses_created__ratings__rating')).values('total'),
            ),
            total_students=Subquery(
                User.objects.filter(id=F('id')).annotate(
                    total=Count('courses_created__students')).values('total'),
            ),
        ).all()

        return context


class CourseSearchView(CourseListView):

    def get_queryset(self):
        search = self.request.GET.get('q')

        queryset = super().get_queryset()

        if not search:
            return queryset

        queryset = queryset.filter(Q(title__icontains=search) | Q(description__icontains=search))

        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        context['search_term'] = self.request.GET.get('q')

        return context


class CourseModulesView(
    HTMXRequireMixin,
    LoginRequiredMixin,
    InstructorRequiredMixin,
    CacheMixin,
    TemplateView,
):
    template_name = 'hx/course/modules.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        context['course'] = self.get_course()
        context['modules'] = self.get_course().modules.all()

        return context


class InstructorAddView(
    HTMXRequireMixin,
    LoginRequiredMixin,
    InstructorRequiredMixin,
    CacheMixin,
    TemplateView,
):
    template_name = 'hx/course/instructor_list.html'
    http_method_names = ['post']

    def post(self, request, *args, **kwargs):
        context = super().get_context_data(**kwargs)

        course = self.get_course()
        context['course'] = course

        instructor_email = self.request.POST.get('instructor')

        error_messages = []
        if course.instructors.filter(email=instructor_email).exists():
            error_messages.append('Esse usuário já é um instrutor do curso.')

        if self.request.user != course.owner:
            error_messages.append('Apenas o dono do curso pode adicionar instrutores.')

        user = None

        try:
            user = User.objects.get(email=instructor_email)
        except ObjectDoesNotExist:
            error_messages.append('Este usuário com esse e-mail não existe.')

        if error_messages:
            return HttpResponse(render_error(error_messages), status=400)

        course.instructors.add(user)

        user.is_instructor = True
        user.save()

        return self.render_to_response(context)


class InstructorRemoveView(
    HTMXRequireMixin,
    LoginRequiredMixin,
    InstructorRequiredMixin,
    CacheMixin,
    TemplateView,
):
    template_name = 'hx/course/instructor_list.html'
    http_method_names = ['post']

    def post(self, request, *args, **kwargs):
        context = super().get_context_data(**kwargs)

        course = self.get_course()
        context['course'] = course

        instructor_id = self.kwargs.get('instructor_id')

        error_messages = []

        if instructor_id == self.request.user.id:
            error_messages.append('Você não pode se remover.')

        if self.request.user != course.owner:
            error_messages.append('Apenas o dono do curso pode remover instrutores.')

        if error_messages:
            return HttpResponse(render_error(error_messages), status=400)

        course.instructors.remove(instructor_id)

        user = User.objects.get(id=instructor_id)

        if len(user.courses_created.all()) == 0:
            user.is_instructor = False
            user.save()

        return self.render_to_response(context)
