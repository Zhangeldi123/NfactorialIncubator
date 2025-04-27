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

    def get_unicode_character(self):
        """Convert Unicode code point to actual character"""
        if not self.unicode:
            return ""

        # Remove 'U+' prefix and split by space if there are multiple code points
        code_points = self.unicode.replace('U+', '')
        if ' ' in code_points:
            code_points = code_points.split(' ')
        else:
            code_points = [code_points]

        # Convert each code point to character and join
        try:
            return ''.join([chr(int(cp, 16)) for cp in code_points])
        except ValueError:
            return self.unicode  # Return original if conversion fails


class Favorite(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    emoji = models.ForeignKey(Emoji, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('user', 'emoji')

    def __str__(self):
        return f"{self.user.username} - {self.emoji.name}"
