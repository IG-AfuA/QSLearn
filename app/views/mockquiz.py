from ..models import *
from django.shortcuts import render
from django.urls import reverse
from django.http import HttpResponseRedirect

import random

# FIXME: Put these in a configuration file
QUESTIONS_PER_QUIZ = 20
QUIZ_DURATION_MINUTES = 90

# Here, we compile quiz questions and prepare everything for the quiz.
# However, we do not open the quiz just yet.
def mockquiz_start(request, pool):
    session_key = request.session.session_key
    if session_key is None:
        # FIXME: Catch case where session cookie could not be stored
        request.session.create()
        session_key = request.session.session_key

    if MockQuiz.objects.filter(session=session_key, pool__pool_name=pool).exists():
        # We already have a quiz for this pool, so we redirect there
        # instead of setting up a new quiz.
        return HttpResponseRedirect(reverse('app:mockquiz_run', args=(pool,)))

    _mockquiz_compile(pool, session_key)
    return render(request, 'app/mockquiz_start.html', {'pool':pool, 'questions_count':QUESTIONS_PER_QUIZ, 'quiz_duration':QUIZ_DURATION_MINUTES})

def mockquiz_run(request, pool):
    session_key = request.session.session_key
    quiz = _mockquiz_get_current_quiz(pool, session_key)

    if quiz.closed:
        # Go to results
        return HttpResponseRedirect(reverse('app:mockquiz_results', args=(pool,)))

    if not quiz.started:
        quiz.start_quiz(QUIZ_DURATION_MINUTES)

    return render(request, 'app/mockquiz.html', {'pool':pool, 'quiz':quiz, 'countdown':quiz.seconds_left})

def mockquiz_submit(request, pool):
    session_key = request.session.session_key
    quiz = _mockquiz_get_current_quiz(pool, session_key)

    # Quiz should be running while we submit
    if not quiz.started or quiz.closed:
        return # Catch this properly

    quiz.end_quiz()

    if quiz.ended_before_due:
        for item in quiz.mockquiz_item_set.order_by('question_number'):
            if 'q'+str(item.question_number) in request.POST:
                item.submitted_answer = int(request.POST['q'+str(item.question_number)])
                item.save()

    # Always return an HttpResponseRedirect after successfully dealing
    # with POST data. This prevents data from being posted twice if a
    # user hits the Back button.
    return HttpResponseRedirect(reverse('app:mockquiz_results', args=(pool,)))


def mockquiz_results(request, pool):
    pass

def _mockquiz_compile(pool, session_key):
    pool_instance = Pool.objects.get(pool_name=pool)
    session = Session.objects.get(pk=session_key)
    quiz = MockQuiz(pool=pool_instance, session = session)
    quiz.save()
    all_pool_questions = pool_instance.question_set.all().values_list('pk', flat=True)
    # TODO: Here we can make a better selection. For example, we could first select N categories and then
    # sample from these. This would shift the selection process from "random questions from the pool" to
    # "questions from random categories within the pool". In the former case, a category with many quesitons
    # will contribute a lot to the question set (this may or may not be desired), while in the latter case,
    # we are trying to provide questions from all categories with equal probability.
    # then sample from these categories
    selection = random.sample(list(all_pool_questions), QUESTIONS_PER_QUIZ)
    for i,q in enumerate(selection):
        question = Question.objects.get(pk=q)
        permutation, _ = question.answers_permutation()
        quiz.mockquiz_item_set.create(
            question_number = i,
            question = question,
            correct_answer = question.solution_permutation(permutation),
            permutation = permutation
        )

# A user can have one open quiz per pool
def _mockquiz_get_current_quiz(pool, session_key):
    return MockQuiz.objects.get(session=session_key, pool__pool_name=pool)
