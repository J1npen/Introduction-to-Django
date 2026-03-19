from django.db import models

class Message(models.Model):
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_at']  # 最新的留言显示在最前面

    def __str__(self):
        return f"{self.content[:30]}... ({self.created_at.strftime('%Y-%m-%d %H:%M')})"
