from django.db import models

# Create your models here.
class C_id(models.Model):
  content = models.CharField(max_length=200)

  def __str__(self):
    return self.content

class Comment(models.Model):
  name = models.CharField(max_length=200, null = True)
  content = models.CharField(max_length=200)

  def __str__(self):
    return self.content