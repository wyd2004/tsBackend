from django.shortcuts import render

# Create your views here.
from django.http.response import HttpResponseRedirect
from django.urls import reverse
from django.contrib import messages
from django.utils.translation import ugettext_lazy
from member.models import MemberInvitation
from rest_framework.decorators import api_view, renderer_classes
from django.shortcuts import render_to_response


def admin_bulk_add_member_invitation(request):
    bulk = [MemberInvitation() for i in range(50)]
    MemberInvitation.objects.bulk_create(bulk)
    url = reverse('admin:member_memberinvitation_changelist')
    messages.add_message(request, messages.INFO, ugettext_lazy('success created'))
    return HttpResponseRedirect(url)


def mp_home(request):
    data = None
    return render_to_response('index.html', data)
