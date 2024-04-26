from django.shortcuts import render


def index(request):
    return render(request, 'app/index.html', {'authenticated':request.user.is_authenticated})
