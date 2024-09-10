from django.db import models

# Create your models here.
class DocumentData(models.Model):
    name = models.CharField(max_length=100)
    data = models.JSONField()
    created_at = models.DateTimeField(auto_now_add=True)
    description = models.TextField(blank=True)
    def __str__(self):
        return self.name