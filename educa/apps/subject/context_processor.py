from .models import Subject


def subject_renderer(request):
    return {
        'subjects': Subject.objects.all(),
    }
