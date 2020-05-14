from django.db import models


class Person(models.Model):
    name = models.CharField(max_length=100)
    image_source = models.ImageField()
    age = models.IntegerField()

    def __str__(self):
        return self.name

    class Meta:
        ordering = ('name',)
