from django.db import models
from django.contrib.auth.models import User


# Create your models here.
class Recipe(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    title = models.CharField(max_length=150)
    comments = models.TextField(null=True, blank=True)
    description = models.TextField(null=True, blank=True)
    time_needed = models.FloatField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    picture_url = models.CharField(max_length=200, null=True)
    def __str__(self):
        return self.title

    class Meta:
        ordering = ['id']
        db_table = 'recipe_list_base_recipe'
