from django.shortcuts import render

# Create your views here.
from django.http.response import HttpResponseRedirect
from django.urls import reverse
from django.contrib import messages
from django.utils.translation import ugettext_lazy
from member.models import MemberInvitation


def admin_bulk_add_member_invitation(request):
    bulk = [MemberInvitation() for i in range(50)]
    MemberInvitation.objects.bulk_create(bulk)
    url = reverse('admin:member_memberinvitation_changelist')
    messages.add_message(request, messages.INFO, ugettext_lazy('success created'))
    return HttpResponseRedirect(url)
