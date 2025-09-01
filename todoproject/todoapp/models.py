from django.db import models
from django.contrib.auth.models import User

class Task(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=200)
    description=models.TextField()
    due_date=models.DateField()
    priority=models.CharField(
        max_length=100,
        choices=[('Low','Low'),('Medium','Medium'),('High','High')],
        default='Low')
    completed = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title
