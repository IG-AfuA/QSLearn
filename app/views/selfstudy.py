from django.contrib.auth.decorators import login_required
from ..models import *
from django.shortcuts import render

@login_required
def selfstudy_start(request, pool):
    categories = Category.objects.all()
    return render(request, 'app/selfstudy_start.html', {'pool':pool, 'categories': categories})

def selfstudy_run(request, pool, category, subcategory=None):
    pass
