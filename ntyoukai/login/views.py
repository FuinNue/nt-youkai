from django.shortcuts import redirect, render_to_response, get_object_or_404
from django.template import RequestContext
from django.contrib.auth import login as user_login
from django.contrib.auth import logout as user_logout
from django.contrib.auth import authenticate
from django.contrib.auth.models import User

from ntyoukai.login.forms import LoginForm, RegistrationForm

"""
login function
"""
def login(request):
    if request.user.is_authenticated():
        return redirect("/")
    f = LoginForm()
    failed = False
    if request.method == "POST":
        user = authenticate(username=request.POST['username'], 
            password=request.POST['password'])
        if user:
            user_login(request, user)
            return redirect("/")
        else:
            f = LoginForm(initial={'username': request.POST['username']})
            failed = True
    
    return render_to_response("login.html", {'form': f, 'failed': failed}, 
        context_instance=RequestContext(request))


"""
logout function
"""
def logout(request):
    if request.user.is_authenticated():
        user_logout(request)
    return redirect("/")


"""
register page and function
"""
def register(request):
    if request.user.is_authenticated():
        redirect("/")

    f = RegistrationForm()
    if request.method == "POST":
        f = RegistrationForm(request.POST)

        if f.is_valid():
            #f.validate_alpha_maximum_users()
            user = User.objects.create_user(
                username=f.cleaned_data['username'],
                email=f.cleaned_data['email'],
                password=f.cleaned_data['password'])
            return redirect("/")
            
    return render_to_response("register.html", {'form': f}, 
        context_instance=RequestContext(request))
