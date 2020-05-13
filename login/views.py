from django.http import HttpResponse,HttpResponseNotFound
from django.shortcuts import render,redirect
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm, PasswordChangeForm
from django.contrib.auth import authenticate, login, logout, update_session_auth_hash
from django.contrib import messages

from social import models

def login_view(request):
    """Serves lagin.djhtml from /e/macid/ (url name: login_view)
    Parameters
    ----------
      request: (HttpRequest) - POST with username and password or an empty GET
    Returns
    -------
      out: (HttpResponse)
                   POST - authenticate, login and redirect user to social app
                   GET - render login.djhtml with an authentication form
    """
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request,user)
            request.session['failed'] = False
            return redirect('social:messages_view')
        else:
            request.session['failed'] = True

    form = AuthenticationForm(request.POST)
    failed = request.session.get('failed',False)
    context = { 'login_form' : form,
                'failed' : failed }

    return render(request,'login.djhtml',context)

def logout_view(request):
    """Redirects to login_view from /e/macid/logout/ (url name: logout_view)
    Parameters
    ----------
      request: (HttpRequest) - expected to be an empty get request
    Returns
    -------
      out: (HttpResponse) - perform User logout and redirects to login_view
    """
    # TODO Objective 4 and 9: reset sessions variables
    request.session.get('counter',2) #initializes it back to 2
    request.session.get('secondcounter',2)
    # logout user
    logout(request)

    return redirect('login:login_view')

def signup_view(request):
    from social import models
    from django.http import HttpResponseRedirect
    from django.contrib import messages
    """Serves signup.djhtml from /e/macid/signup (url name: signup_view)
    Parameters
    ----------
      request : (HttpRequest) - expected to be an empty get request
    Returns
    -------
      out : (HttpRepsonse) - renders signup.djhtml
    """
    form = UserCreationForm(request.POST)
    # TODO Objective 1: implement signup view
    try:
        if request.method == 'POST':
            username = request.POST['username']
            password = request.POST['password1']
            models.UserInfo.objects.create_user_info(username=username,password=password)
            user = authenticate(request, username=username,password=password)
            if user is not None:
                login(request,user)
                request.session['failed'] = False
                return redirect('social:messages_view')
            else:
                request.session['failed'] = True
        failed = request.session.get('signup_failed',False)
        request.session['failed'] = True
        context = {'signup_form' : form}
        return render(request, 'signup.djhtml', context)
    except:
        context = {'signup_form' : form, 'message': True}
        return render(request,'signup.djhtml',context)
