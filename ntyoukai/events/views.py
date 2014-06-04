from django.shortcuts import render_to_response, get_object_or_404, redirect
from django.contrib.auth.models import User
from django.template import RequestContext
from django.contrib.auth.decorators import login_required
from django.db.models import Q
from django.http import Http404

from ntyoukai.events.models import Event, Entry, Invite
from ntyoukai.events.forms import EventForm, EntryForm, InvitationForm


"""
Listing all events
"""
@login_required(login_url='/user/login/')
def list(request):
	events = Event.objects.filter(attendants=request.user)
	invites = Invite.objects.filter(user=request.user)

	return render_to_response("list.html", 
		{'events': events, 'invites': invites}, 
		context_instance=RequestContext(request))


"""
View an event in detail
"""
@login_required(login_url='/user/login/')
def details(request, event_pk):
	event = get_object_or_404(Event, pk=event_pk)

	invited_users = []

	for invite in event.invited.all():
		invited_users.append(invite.user)

	if request.user in event.attendants.all() or \
	request.user in invited_users:
		return render_to_response("details.html", 
			{'event': event}, 
			context_instance=RequestContext(request))

	raise Http404


"""
View an event in detail invited
"""
@login_required(login_url='/user/login/')
def details_invited(request, event_pk, invite_pk):
	event = get_object_or_404(Event, pk=event_pk)
	invite = get_object_or_404(Invite, pk=invite_pk)

	invited_users = []

	for invite in event.invited.all():
		invited_users.append(invite.user)

	if request.user in event.attendants.all() or \
	request.user in invited_users:
		return render_to_response("details.html", 
			{'event': event, 'invite':invite}, 
			context_instance=RequestContext(request))

	raise Http404


"""
Create a new event
"""
@login_required(login_url='/user/login/')
def new(request):
	f = EventForm()

	if request.method == 'POST':
		f = EventForm(request.POST)

		if f.is_valid():
			e = f.save(commit=False)
			e.owner = request.user
			e.save()
			e.attendants.add(request.user)
			e.save()
			return redirect("/events/event/%i/" % e.pk)

	return render_to_response("edit.html", 
		{'form': f}, 
		context_instance=RequestContext(request))


"""
Edit an event
"""
@login_required(login_url='/user/login/')
def edit(request, event_pk):
	event = get_object_or_404(Event, pk=event_pk)
	if request.user not in event.moderators.all() or \
	request.user != event.owner:
		raise Http404

	f = EventForm(event)

	if request.method == 'POST':
		f = EventForm(request.POST)

		if f.is_valid():
			e = f.save()
			return redirect("/events/event/%i/" % e.pk)

	return render_to_response("edit.html", 
		{'form': f}, 
		context_instance=RequestContext(request))


"""
Invite users to event
"""
@login_required(login_url='/user/login/')
def invite(request, event_pk):
	event = get_object_or_404(Event, pk=event_pk)
	if request.user != event.owner:
		return redirect('/')
	form = InvitationForm()

	if request.method == 'POST':
		form = InvitationForm(request.POST)
		if form.is_valid():
			event.invite(form.cleaned_data['invite_list'], 
				form.cleaned_data['message'])
		
		return redirect("/events/event/%i/" % event.pk)

	return render_to_response("invite.html", 
		{'event': event, 'form': form},
		context_instance=RequestContext(request))


"""
Post an entry
"""
@login_required(login_url='/user/login/')
def post_entry(request, event_pk):
	event = get_object_or_404(Event, pk=event_pk)
	if request.user not in event.moderators.all() or \
	request.user != event.owner:
		print("FAG")
		raise Http404

	form = EntryForm()

	if request.method == 'POST':
		form = EntryForm(request.POST)
		if form.is_valid():
			entry = form.save(commit=False)
			entry.author = request.user
			entry.save()
			event.entries.add(entry)
			return redirect("/events/event/%i/" % event.pk)

	return render_to_response("entry.html", 
		{'event': event, 'form': form},
		context_instance=RequestContext(request))



"""
Attend to the event
"""
@login_required(login_url='/user/login/')
def accept_invite(request, event_pk, invite_pk):
	event = get_object_or_404(Event, pk=event_pk)
	invite = get_object_or_404(Invite, pk=invite_pk)

	if invite.user == request.user:
		event.attendants.add(invite.user)
		invite.delete()
		return redirect("/events/event/%i/" % event.pk)


"""
Reject or take back an invite
"""
@login_required(login_url='/user/login/')
def reject_invite(request, event_pk, invite_pk):
	event = get_object_or_404(Event, pk=event_pk)
	invite = get_object_or_404(Invite, pk=invite_pk)

	if request.user in event.moderators.all() or \
	request.user == event.owner:
		invite.delete()
		return redirect("/events/event/%i/" % event.pk)

	if invite.user == request.user:
		invite.delete()
		raise Http404


"""
Remove user from an event
"""
@login_required(login_url='/user/login/')
def remove_user(request, event_pk, user_pk):
	event = get_object_or_404(Event, pk=event_pk)

	if request.user not in event.moderators.all() or \
	request.user != event.owner:
		if request.user != event.owner:
			event.attendants.remove(user_pk)
			return redirect("/events/event/%i/" % event.pk)

	raise Http404


"""
Leave an event
"""
@login_required(login_url='/user/login/')
def leave(request, event_pk):
	event = get_object_or_404(Event, pk=event_pk)

	if request.user in event.attendants.all():
		if request.user != event.owner:
			event.attendants.remove(request.user)
			return redirect("/events/")

	raise Http404