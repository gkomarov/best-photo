from django.contrib import admin
from .models import Voting


class VotingPerson(admin.ModelAdmin):
    list_display = 'name'


admin.site.register(Voting)