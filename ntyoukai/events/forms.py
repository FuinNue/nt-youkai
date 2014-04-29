from django import forms

from ntyoukai.events.models import Event, Entry

"""
Form for creating and editing events
"""
class EventForm(forms.ModelForm):
	class Meta:
		model = Event
		fields = [
			'name', 
			'description', 
			'start_of_event', 
			'end_of_event', 
			'invited']


"""
A comment or note in an event
"""
class EntryForm(forms.ModelForm):
	class Meta:
		model = Entry
		field = ['content']