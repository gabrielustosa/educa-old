from django.core.exceptions import PermissionDenied


class CourseOwnerMixin:
    def dispatch(self, request, *args, **kwargs):
        course = self.get_course()
        if course.owner != request.user:
            raise PermissionDenied()
        return super().dispatch(request, *args, **kwargs)


class QuestionOwnerMixin:
    def dispatch(self, request, *args, **kwargs):
        question = self.get_question
        if question.user != request.user:
            raise PermissionDenied()
        return super().dispatch(request, *args, **kwargs)
