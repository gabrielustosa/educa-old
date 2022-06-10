from django.db import models
from django.core.exceptions import ObjectDoesNotExist


class OrderField(models.PositiveIntegerField):
    def __init__(self, for_fields=None, *args, **kwargs):
        self.for_fields = for_fields
        super().__init__(*args, **kwargs)

    def pre_save(self, model_instance, add):
        if getattr(model_instance, self.attname) is None:
            try:
                qs = self.model.objects.all()
                if self.for_fields:
                    query = {field: getattr(model_instance, field) for field in self.for_fields}
                    qs = qs.filter(**query)
                last_item = qs.latest(self.attname)
                value = last_item.order + 1
            except ObjectDoesNotExist:
                value = 1
            setattr(model_instance, self.attname, value)
            return value
        else:
            return super().pre_save(model_instance, add)


class LessonOrderField(models.PositiveIntegerField):
    def __init__(self, for_fields=None, *args, **kwargs):
        self.for_fields = for_fields
        super().__init__(*args, **kwargs)

    def pre_save(self, model_instance, add):
        if getattr(model_instance, self.attname) is None:
            current_module = getattr(model_instance, 'module')
            course = getattr(model_instance, 'course')

            qs = self.model.objects.all()
            if self.for_fields:
                query = {field: getattr(model_instance, field) for field in self.for_fields}
                qs = qs.filter(**query)

            if qs.exists():
                last_item = qs.latest(self.attname)
                value = last_item.order + 1
            else:
                try:
                    last_item = course.lesson_set.latest(self.attname)
                    value = last_item.order + 1
                except ObjectDoesNotExist:
                    value = 1

            for next_module in course.modules.filter(order__gt=current_module.order).order_by('order').all():
                for lesson in next_module.lessons.all():
                    lesson.order = lesson.order + 1
                    lesson.save()

            setattr(model_instance, self.attname, value)
            return value
        else:
            return super().pre_save(model_instance, add)
