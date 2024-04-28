from django.contrib.auth.decorators import login_required
from ..models import *
from django.shortcuts import render

import json

@login_required
def selfstudy_start(request, pool):
    categories = Category.objects.all()
    return render(request, 'app/selfstudy_start.html', {'pool':pool, 'categories': categories})

@login_required
def selfstudy_run(request, pool, category, subcategory=None):
    return render(request, 'app/selfstudy_static.html', {'pool':pool, 'selfpath':request.path})

@login_required
def selfstudy_card(request, pool, category, subcategory=None, until=False):
    if request.method =='POST':
        # Answer was submitted --> display solution ...
        data = json.loads(request.body)
        question = Question.objects.get(pk=data['question_id'])
        permutation = int(data['permutation'])
        _, answers = question.answers_permutation(permutation)
        if 'q' in data:
            submitted_answer = int(data['q'])
        else:
            submitted_answer = None

        correct_answer = question.solution_permutation(permutation)

        return render(request, 'app/selfstudy_card_result.html', {'question':question, 'question_id':question.question_id, 'answers':answers, 'submitted_answer':submitted_answer, 'correct_answer':correct_answer,'answers':answers})

    else:
        # ... otherwise we display a regular card
        questions = Question.objects.filter(pool__pool_name=pool).select_related('subcategory', 'subcategory__parent')
        if 'previous_question' in request.GET and request.GET['previous_question'] != '':
            questions = questions.exclude(id=request.GET['previous_question'])

        if subcategory is not None:
            questions = questions.filter(subcategory=subcategory)

        if until:
            # FIXME: Use order_number here to ensure independence on PK order
            question = questions.filter(subcategory__parent__pk__lte=category).order_by("?").first()
        else:
            question = questions.filter(subcategory__parent__pk = category).order_by("?").first()

        permutation, answers = question.answers_permutation()
        return render(request, 'app/selfstudy_card.html', {'question':question, 'question_id':question.question_id, 'answers':answers, 'permutation':permutation})


