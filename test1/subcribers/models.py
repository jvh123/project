from django.db import models
from django.contrib.auth.models import User
from django.conf import settings
# Create your models here.
class Subscrpber(models.Model):
    USERNAME_FIELD = 'username'
    user_rec = models.ForeignKey(User)
    call_number=models.CharField(max_length=100)
    event1=models.CharField(max_length=20)
    event2 = models.CharField(max_length=20)
    event3 = models.CharField(max_length=20)
    email_check=models.IntegerField()
    class Meta:
        verbose_name_plural='subscribers'
    def __str__(self):
        return u"%s's Subscription Info"%self.user_rec
