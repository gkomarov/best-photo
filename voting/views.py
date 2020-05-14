from django.db import transaction
from django.db.models import F, Func
from django.http import JsonResponse
from django.views import generic
from django.views.generic.base import View

from person.models import Person
from .models import Voting, Vote


class IndexView(generic.ListView):

    template_name = 'voting/votings.html'
    context_object_name = 'all_voting_list'

    def get_queryset(self):
        return Voting.objects.all()


class VoteUpdate(View):

    def post(self, request):
        voting = Voting.objects.get(pk=request.POST['voting_id'])
        person = Person.objects.get(pk=request.POST['person_id'])

        try:
            vote = Vote.objects.get(voting=voting, person=person)
            if vote.number_of_votes < voting.limit_votes_for_win:
                with transaction.atomic():
                    vote.number_of_votes = F('number_of_votes') + 1
                    vote.save()
            else:
                return JsonResponse({'limit_was_reached': True})
        except Vote.DoesNotExist:
            vote = Vote(voting=voting, person=person, number_of_votes=1)
            vote.save()

        return JsonResponse({'success': True})


class DetailView(generic.DetailView):
    model = Voting
    template_name = 'voting/active.html'

    def get_object(self, queryset=None):
        voting = super().get_object()
        if not voting.is_active:
            voting.persons.all = voting.persons.all()[:5]
            self.template_name = 'voting/finished.html'

        return voting
