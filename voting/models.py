from datetime import datetime
from django.db import models
from django.db.models import Max
from person.models import Person


class Voting(models.Model):
    name = models.CharField(max_length=100)
    start_date = models.DateTimeField()
    end_date = models.DateTimeField()
    limit_votes_for_win = models.IntegerField(default=5)
    persons = models.ManyToManyField(Person)
    objects = models.Manager()

    @property
    def is_active(self):
        max_vote = self._get_max_vote()
        if self.limit_votes_for_win > max_vote and self.end_date.replace(tzinfo=None) >= datetime.now():
            return True
        return False

    @property
    def leader_id(self):
        return self.vote_set.filter(number_of_votes=self._get_max_vote()).first().person_id

    def _get_max_vote(self):
        # Выбирает максимальный из набора голосов в голосовании.
        return self.vote_set.all().aggregate(value=Max('number_of_votes'))['value'] or 0

    def __str__(self):
        return self.name


class Vote(models.Model):
    # Голоса отданные за персонажей к конкретному голосованию
    person = models.ForeignKey(Person, on_delete=models.CASCADE)
    voting = models.ForeignKey(Voting, on_delete=models.CASCADE)
    number_of_votes = models.IntegerField()

    class Meta:
        ordering = ['-number_of_votes']

