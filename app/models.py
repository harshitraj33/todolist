from django.db import models

class List(models.Model):
    name = models.CharField(max_length=100)
    due_date = models.DateTimeField(null=True, blank=True)

    def __str__(self):
        return self.name

class Item(models.Model):
    list = models.ForeignKey(List, on_delete=models.CASCADE)
    text = models.CharField(max_length=200)
    due_date = models.DateTimeField(null=True, blank=True)
    completed = models.BooleanField(default=False)

    def __str__(self):
        return self.text
