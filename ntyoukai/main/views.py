from django.shortcuts import redirect

def home(request):
	if request.user.is_authenticated():
		return redirect('/events/')
	else:
		return redirect('/user/login/')