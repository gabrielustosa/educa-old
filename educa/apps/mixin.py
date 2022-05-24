from django.core.exceptions import PermissionDenied


class CourseOwnerMixin:
    def dispatch(self, request, *args, **kwargs):
        course = self.get_course()
        if course.owner != request.user:
            raise PermissionDenied()
        return super().dispatch(request, *args, **kwargs)
