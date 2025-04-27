from django.db import models
from django.contrib.auth.models import User

class Emoji(models.Model):
    name = models.CharField(max_length=100)
    category = models.CharField(max_length=100)
    group = models.CharField(max_length=100)
    html_code = models.CharField(max_length=100)
    unicode = models.CharField(max_length=100)
    
    def __str__(self):
        return self.name

class Favorite(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    emoji = models.ForeignKey(Emoji, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        unique_together = ('user', 'emoji')
    
    def __str__(self):
        return f"{self.user.username} - {self.emoji.name}"
