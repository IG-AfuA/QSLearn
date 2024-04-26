from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login, logout
from django.http import HttpResponseRedirect
from django.urls import reverse


def user_login(request):
    # We use this both for displaying the login page as well as
    # processing the POST request after filling out the form.

    # This is for processing the post request ...
    if 'username' in request.POST and 'password' in request.POST:
        user = authenticate(request, username=request.POST['username'], password=request.POST['password'])
        if user is not None:
            login(request, user)
            if 'next' in request.POST and request.POST['next'] != '':
                # This is how the login-required-decorator informs us where to go
                # after forced login. FIXME: Do we have to sanitize this?
                return HttpResponseRedirect(request.POST['next'])
            else:
                return HttpResponseRedirect(reverse('app:index'))

        # else redisplay login page, but with error
    # ... and this is for displaying the form ...
    else:
        return render(request, 'app/login.html')

@login_required
def user_logout(request):
    logout(request)
    return HttpResponseRedirect(reverse("app:index"))
