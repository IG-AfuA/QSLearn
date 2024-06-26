from django.db import models
from django.db.models import F
from django.contrib.auth.models import User
from django.contrib.sessions.models import Session
from django.utils import timezone


import itertools, random
import datetime

ANSWERS_PER_QUESTION = 4 # If you change this, you also have to change the Quesiton class below
# Enumerate all permutations
PERMUTATIONS = [i for i in itertools.permutations(range(ANSWERS_PER_QUESTION))]


class Category(models.Model):
    category_id = models.CharField(max_length=20, unique=True)
    category_name = models.CharField(max_length=200)
    category_order = models.IntegerField() # Used for sorting, but we currently rely on PK for this

    @property
    def category(self):
        return self.category_id + ': ' + self.category_name

    def __str__(self):
        return self.category

class Subcategory(models.Model):
    parent = models.ForeignKey(Category, on_delete=models.CASCADE)
    subcategory_id = models.CharField(max_length=20, unique=True)
    subcategory_name = models.CharField(max_length=200)
    subcategory_order = models.IntegerField() # Used for sorting, but we currently rely on PK for this

    @property
    def subcategory(self):
        return self.subcategory_id + ': ' + self.subcategory_name

    def __str__(self):
        return self.subcategory

class Pool(models.Model):
    pool_name = models.CharField(max_length=20, unique=True)

    def __str__(self):
        return self.pool_name

# This is a custom manager to retrieve questions from a given pool, category and
# optional subcategory. All subcategories within the category are considered if
# none is given. If until==True we also include questions from categories that
# precede the given one. If until==True, subcategory must be None.
# See https://stackoverflow.com/questions/4541780/where-to-put-common-queries-in-django
class QuestionManager(models.Manager):
    # Usage: Question.objects.filter_questions(pool, category, subcategory, until)
    def filter_questions(self, pool, category, subcategory=None, until=False):
        ret = super(QuestionManager, self).get_queryset().filter(pool__pool_name=pool)
        if subcategory is not None:
            ret = ret.filter(subcategory=subcategory)

        if until:
            # FIXME: Use order_number here to ensure independence on PK order
            ret = ret.filter(subcategory__parent__pk__lte=category)
        else:
            ret = ret.filter(subcategory__parent__pk = category)

        return ret

class Question(models.Model):
    objects = QuestionManager()
    pool = models.ForeignKey(Pool, on_delete=models.CASCADE)
    subcategory = models.ForeignKey(Subcategory, on_delete=models.CASCADE)
    question_id = models.CharField(max_length=20)
    question_text = models.CharField(max_length=200)
    answer_0 = models.CharField(max_length=200)
    answer_1 = models.CharField(max_length=200)
    answer_2 = models.CharField(max_length=200)
    answer_3 = models.CharField(max_length=200)
    solution = models.IntegerField()
    outdated = models.BooleanField()

    def answers(self):
        return (self.answer_0, self.answer_1, self.answer_2, self.answer_3)

    # Return a permutation of the answer set along with an integer identifying
    # the permutation (as enumerted in PERMUTATIONS). If this identifyer is
    # zero, we randomly generate one.

    # The function can be used to generate a random permutation of ansers
    # (using permutation=None) or to reproduce the answer set for a given
    # permutation.
    def answers_permutation(self, permutation=None):
        if permutation is None:
            permutation = random.randrange(len(PERMUTATIONS))
        answers = self.answers()
        return permutation, tuple(answers[p] for p in PERMUTATIONS[permutation])

    # Return the solution number of this question for a given permutation
    def solution_permutation(self, permutation):
        return PERMUTATIONS[permutation].index(self.solution)

    def __str__(self):
        return self.pool.pool_name+'/'+self.question_id

# Use this to track user progress. A user masters a particular question if that
# question was answered MASTER_THRESHOLD times correctly. Wrong answers are
# penalized by reducing the score accordingly.
MASTER_THRESHOLD = 3 # FIXME: Put this in a config file or something
class Question_Score(models.Model):
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    correct_answers = models.IntegerField(default=0)

    # score is 1 iff user masters question.
    @property
    def score(self):
        return self.correct_answers / MASTER_THRESHOLD

    def increase_score(self):
        if self.correct_answers < MASTER_THRESHOLD:
            self.correct_answers += 1
            self.save()

    def decrease_score(self):
        if self.correct_answers > 0:
            self.correct_answers -= 1
            self.save()

    def __str__(self):
        return(f'{self.question}: {self.score*100}%')


class MockQuiz(models.Model):
    # FIXME: (session, pool) is unique
    session = models.ForeignKey(Session, on_delete=models.CASCADE)
    pool = models.ForeignKey(Pool, on_delete=models.CASCADE)
    start_time = models.DateTimeField('When did user start the quiz?', blank=True, null=True)
    due_time = models.DateTimeField('When is the quiz due?', blank=True, null=True)
    end_time = models.DateTimeField('When did the user hand in quiz?', blank=True, null=True)

    @property
    def started(self):
        return self.start_time is not None

    @property
    def closed(self):
        return self.end_time is not None

    @property
    def ended_before_due(self):
        # False if not yet closed
        return self.end_time < self.due_time

    @property
    def seconds_left(self):
        ret = self.due_time - timezone.now()
        return max(0, ret.total_seconds())

    @property
    def duration(self):
        return self.end_time - self.start_time

    @property
    def duration_string(self):
        delta = self.duration
        return f'{int(delta.total_seconds()//60):02d}:{int(round(delta.total_seconds()%60)):02d}'

    @property
    def total_items(self):
        return self.mockquiz_item_set.count()

    @property
    def correct_items(self):
        return self.mockquiz_item_set.filter(submitted_answer=F('correct_answer')).count()

    @property
    def incorrect_items(self):
        return self.total_items-self.mockquiz_item_set.filter(submitted_answer=F('correct_answer')).count()

    def start_quiz(self, duration_minutes):
        # Prevent resetting due time by re-opening quiz
        if not self.started:
            self.start_time = timezone.now()
            self.due_time = self.start_time + datetime.timedelta(minutes=duration_minutes)
            self.save()

    def end_quiz(self):
        if not self.closed:
            self.end_time = timezone.now()
            self.save()


# A question in a mock quiz
# FIXME: Check if we can use order_with_respect_to for this
class MockQuiz_Item(models.Model):
    quiz = models.ForeignKey(MockQuiz, on_delete=models.CASCADE)
    question_number = models.IntegerField() # Used for sorting
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    submitted_answer = models.IntegerField(default=None, null=True)
    correct_answer = models.IntegerField()
    permutation = models.IntegerField()

    # Here, we return the possible answers according to the permutation stored
    # in the "permutation" field. We do not return the permutation index
    # (unlike Question.answers_permutation())
    @property
    def answers_permutation(self):
        _, answers = self.question.answers_permutation(self.permutation)
        return answers
