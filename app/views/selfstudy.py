from django.contrib.auth.decorators import login_required
from ..models import *
from django.shortcuts import render

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
        pass # FIXME: TODO
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


