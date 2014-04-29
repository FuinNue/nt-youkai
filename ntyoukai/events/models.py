from django.db import models
from django.contrib.auth.models import User


"""
An entry post in an event aka notes
"""
class Entry(models.Model):
	author = models.ForeignKey(User, editable=False)
	content = models.TextField()
	creation_date = models.DateTimeField(auto_now=True, editable=False)

	def __unicode__(self):
		return 'Post by %s in %s, %s' % (self.author, self.event.get(), self.creation_date)

"""
An event
"""
class Event(models.Model):
	name = models.CharField(max_length=255)
	description = models.TextField(blank=True, null=True)
	owner = models.ForeignKey(User, editable=False, related_name='owner')
	creation_date = models.DateTimeField(auto_now=True, editable=False)
	start_of_event = models.DateTimeField(blank=True, null=True)
	end_of_event = models.DateTimeField(blank=True, null=True)
	invited = models.ManyToManyField(User, blank=True, null=True, related_name='invited')
	entries = models.ManyToManyField(Entry, blank=True, null=True, related_name='event')

	def __unicode__(self):
		return self.name