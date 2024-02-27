from django.db import models
from django.contrib.auth.models import User

class Progress(models.Model):
    subject = models.CharField(max_length=255)
    catatan = models.TextField()
    start_Study = models.CharField(max_length=10)
    progress = models.IntegerField()
    date_added = models.DateField(auto_now_add=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)