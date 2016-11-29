from django.shortcuts import render

# Create your views here.
from django.http.response import HttpResponseRedirect
from django.urls import reverse
from django.contrib import messages
from django.utils.translation import ugettext_lazy


def admin_bulk_add_trial_member(request):
    from member.models import TrialMember
    bulk = [TrialMember() for i in range(50)]
    TrialMember.objects.bulk_create(bulk)
    url = reverse('admin:member_trialmember_changelist')
    messages.add_message(request, messages.INFO, ugettext_lazy('success created'))
    return HttpResponseRedirect(url)
