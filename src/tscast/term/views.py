from django.shortcuts import render

# Create your views here.
from django.http.response import HttpResponseRedirect
from django.urls import reverse
from django.contrib import messages
from django.utils.translation import ugettext_lazy
from member.models import MemberInvitation
from rest_framework.decorators import api_view, renderer_classes
from django.shortcuts import render_to_response
from term.crontask import payment_status_update


def test_order_query_crontab(request):
    payment_status_update()
    return render_to_response('index.html', '')

