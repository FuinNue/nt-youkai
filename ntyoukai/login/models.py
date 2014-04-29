from django.db import models
from django.contrib.auth.hashers import check_password, make_password

class User(models.Model):
    username = models.CharField(max_length=20)
    password = models.CharField(max_length=128)
    
    def __unicode__(self):
        return self.username
    
    def set_password(self, r_password):
        p = make_password(r_password)
        
        if check_password(r_password, p):
            self.password = p
            return True
        else:
            return False

def authenticate(self, username, password):
    user = User.objects.get(username=username)
    if check_password(password, user.password):
        return user
    else:
        return None        
