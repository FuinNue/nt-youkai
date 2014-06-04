from django.db import models
from django.contrib.auth.models import User
from django.db.models import Q
from django.core.exceptions import ObjectDoesNotExist


"""
An entry post in an event aka notes
"""
class Entry(models.Model):
	author = models.ForeignKey(User, editable=False)
	content = models.TextField()
	creation_date = models.DateTimeField(auto_now=True, editable=False)

	def __unicode__(self):
		return 'Update by %s (%s)' % (self.author, self.creation_date)

"""
An invite to an event
"""
class Invite(models.Model):
	user = models.ForeignKey(User, null=True, blank=True)
	email = models.CharField(max_length=255, blank=True, null=True)
	message = models.TextField()

	def accept(self):
		self.event.get().attendants.add(self.user)
		self.delete()

	def reject(self):
		self.delete()

	def __str__(self):
		if self.user:
			return self.user.username
		else:
			return self.email

"""
An event
"""
class Event(models.Model):
	name = models.CharField(max_length=255)
	description = models.TextField(blank=True, null=True)
	owner = models.ForeignKey(User, editable=False, related_name='event')
	moderators = models.ManyToManyField(User, related_name='events', null=True, blank=True)
	creation_date = models.DateTimeField(auto_now=True, editable=False)
	start = models.DateTimeField(blank=True, null=True)
	end = models.DateTimeField(blank=True, null=True)
	invited = models.ManyToManyField(Invite, blank=True, null=True, related_name='event')
	attendants = models.ManyToManyField(User, blank=True, null=True, related_name='attendants')
	entries = models.ManyToManyField(Entry, blank=True, null=True, related_name='event')

	def __unicode__(self):
		return self.name

	def invite(self, invitation_list, message):
		invitation_list = invitation_list.split(',')
		for invite in invitation_list:
			invite = invite.strip(' ').strip('\n')
			user = None
			try:
				user = User.objects.get(Q(username=invite) | Q(email=invite))
			except ObjectDoesNotExist:
				pass

			if user not in self.attendants.all():
				if user:
					try:
						i = Invite.objects.create(user=user, email=user.email, message=message)
						self.invited.add(i)
					except:
						pass
				else:
					if "@" in invite:
						i = Invite.objects.create(email=invite, message=message)
						self.invited.add(i)
						# Create magic emailing function here!