from django.apps import apps


def get_model(model_name):
    if model_name in ['text', 'video', 'image', 'file']:
        return apps.get_model(app_label='content', model_name=model_name)
    return None


def content_is_instance(content, class_name):
    return isinstance(content.item, get_model(class_name))
