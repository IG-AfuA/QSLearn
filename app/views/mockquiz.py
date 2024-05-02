from ..models import *
from django.shortcuts import render

import random

# FIXME: Put these in a configuration file
QUESTIONS_PER_QUIZ = 20
QUIZ_DURATION_MINUTES = 90

# Here, we compile quiz questions and prepare everything for the quiz.
# However, we do not open the quiz just yet.
def mockquiz_start(request, pool):
    session_key = request.session.session_key
    if session_key is None or not MockQuiz.objects.filter(session=session_key, pool__pool_name=pool).exists():
        # FIXME: Catch case where session cookie could not be stored
        request.session.create()
        session_key = request.session.session_key

    # FIXME: Check if we already have set up a quiz
    _mockquiz_compile(pool, session_key)
    return render(request, 'app/mockquiz_start.html', {'pool':pool, 'questions_count':QUESTIONS_PER_QUIZ, 'quiz_duration':QUIZ_DURATION_MINUTES})

def mockquiz_run(request, pool):
    pass

def mockquiz_submit(request, pool):
    pass

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
