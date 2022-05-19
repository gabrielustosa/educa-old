from django.forms import modelform_factory
from django.shortcuts import get_object_or_404, render

from educa.apps.question.models import Answer, Question


def create_answer_view(request, question_id):
    question = get_object_or_404(Question, id=question_id)

    content = request.POST.get('content')

    Answer.objects.create(user=request.user, question=question, content=content)
    answers = Answer.objects.filter(question=question)
    form = modelform_factory(Answer, fields=('content',))

    return render(request, 'hx/question/answer/answer.html',
                  context={'answers': answers, 'form': form, 'question': question})


def update_answer_view(request, answer_id):
    answer = get_object_or_404(Answer, id=answer_id)

    form = modelform_factory(Answer, fields=('content',))
    form = form(instance=answer)

    return render(request, 'hx/question/answer/update.html',
                  context={'form': form, 'answer': answer})


def save_answer_view(request, answer_id):
    answer = get_object_or_404(Answer, id=answer_id)

    answer.content = request.POST.get('content')
    answer.save()

    return render(request, 'hx/question/answer/view.html',
                  context={'answer': answer})
