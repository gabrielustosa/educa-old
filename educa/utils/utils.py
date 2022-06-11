import requests
import pafy

from django.apps import apps
from urllib import parse


def get_model(model_name):
    if model_name in ['text', 'image', 'file', 'link']:
        return apps.get_model(app_label='content', model_name=model_name)
    return None


def content_is_instance(content, class_name):
    return isinstance(content.item, get_model(class_name))


def get_lesson_id(request):
    return request.GET.get('lesson_id') if request.GET.get('lesson_id') else request.POST.get('lesson_id')


def render_error(error_messages):
    new_list = []
    for error in error_messages:
        new_list.append(error)
        if error != error_messages[len(error_messages) - 1]:
            new_list.append('&')
    return new_list


def get_url_id(url):
    url_parsed = parse.urlparse(url)
    qsl = parse.parse_qs(url_parsed.query)
    if len(qsl) > 0:
        return qsl['v'][0]
    return ''


def check_video_url(url):
    video_id = get_url_id(url)
    checker_url = "https://www.youtube.com/oembed?url=http://www.youtube.com/watch?v="
    video_url = checker_url + video_id

    request = requests.get(video_url)

    return request.status_code != 200


def get_video_duration(url):
    video = pafy.new(url)
    return video.length


def format_time(seconds):
    h = round(seconds / 3600)
    m = round(seconds % 3600 / 60)
    s = seconds % 60

    result = ''
    if h > 0:
        result += f'{h} h '
    if m > 0:
        result += f'{m} m '
    if result == '':
        result = f'{s} s '
    return result
