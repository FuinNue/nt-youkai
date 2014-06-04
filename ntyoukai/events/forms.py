from django import forms
from django.core.exceptions import ValidationError

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
			'start', 
			'end']


"""
A comment or note in an event
"""
class EntryForm(forms.ModelForm):
	class Meta:
		model = Entry
		field = ['content']


class InvitationForm(forms.Form):
	invite_list = forms.CharField(widget=forms.Textarea, required=True, 
		help_text="Type usernames or email-addresses in the textbox. Seperate with commas. Do not use breaks because I have not fixed it yet lol")
	message = forms.CharField(widget=forms.Textarea, required=False, 
		help_text="Create a message to send to all invited if they are not already registerd on the page.")

	def validate_nobreaks(self):
		if self.invite_list("\\"):
			raise ValidationError("No breaks allowed!")