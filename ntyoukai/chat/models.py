from django.db import models
from django.auth.contrib.models import User


class Room(models.Model):
	

class Post(models.Model):
	author = models.ForeignKey(User)
	content = models.TextField()
