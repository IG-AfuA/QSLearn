from django.db import models

import itertools, random

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

class Question(models.Model):
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

    # Return a random permutation of the answer set along with an integer identifying
    # the permutation (as enumerted in PERMUTATIONS).
    def answers_permutation(self):
        permutation = random.randrange(len(PERMUTATIONS))
        answers = self.answers()
        return permutation, tuple(answers[p] for p in PERMUTATIONS[permutation])

    def __str__(self):
        return self.pool.pool_name+'/'+self.question_id
