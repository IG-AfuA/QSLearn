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

        # Here we update the score
        score, created = Question_Score.objects.get_or_create(user=request.user, question=question)
        if submitted_answer == correct_answer:
            score.increase_score()
        else:
            score.decrease_score()

        return render(request, 'app/selfstudy_card_result.html', {'question':question, 'question_id':question.question_id, 'answers':answers, 'submitted_answer':submitted_answer, 'correct_answer':correct_answer,'answers':answers})

    else:
        # ... otherwise we display a regular card
        questions = Question.objects.filter_questions(pool, category, subcategory, until)
        if 'previous_question' in request.GET and request.GET['previous_question'] != '':
            # FIXME: Ensure no category contains one single question...
            questions = questions.exclude(id=request.GET['previous_question'])

        question = questions.order_by("?").first()

        permutation, answers = question.answers_permutation()
        return render(request, 'app/selfstudy_card.html', {'question':question, 'question_id':question.question_id, 'answers':answers, 'permutation':permutation})


