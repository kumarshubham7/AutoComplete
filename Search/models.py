from django.db import models

# Create your models here.
class WordsData(models.Model):
    word = models.CharField(max_length=100)
    word_rank = models.IntegerField(max_length=20)

