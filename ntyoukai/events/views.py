from django.shortcuts import render_to_response, get_object_or_404, redirect
from django.contrib.auth.models import User
from django.template import RequestContext
from django.contrib.auth.decorators import login_required

from ntyoukai.events.models import Event, Entry
from ntyoukai.events.forms import EventForm, EntryForm


"""
Listing all events
"""
@login_required(login_url='/user/login/')
def list(request):
	events = Event.objects.filter(invited__in=request.user)
	return render_to_response("list.html", 
		{'events': events}, 
		context_instance=RequestContext(request))


"""
View an event in detail
"""
@login_required(login_url='/user/login/')
def details(request, event_pk):
	event = get_object_or_404(Event, pk=event_pk)

	if request.user in event.invited:
		return render_to_response("details.html", 
			{'event': event}, 
			context_instance=RequestContext(request))

	return redirect('/events/')


"""
Create a new event
"""
@login_required(login_url='/user/login/')
def new(request):
	f = EventForm()
	if request.method == 'POST':
		f = EventForm(request.POST)
		if f.is_valid():
			e = f.save()
			return redirect("/events/event/%i/edit/" % e.pk)

	return render_to_response("edit.html", 
		{'form': f}, 
		context_instance=RequestContext(request))


"""
Edit an event
"""
@login_required(login_url='/user/login/')
def edit(request, event_pk):
	f = EventForm(get_object_or_404(Event, pk=event_pk))
	if request.method == 'POST':
		f = EventForm(request.POST)
		if f.is_valid():
			e = f.save()
			return redirect("/events/event/%i/" % e.pk)

	return render_to_response("edit.html", 
		{'form': f}, 
		context_instance=RequestContext(request))