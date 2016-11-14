import requests
import logging
from django.utils.translation import ugettext_lazy as _
from rest_framework.authentication import TokenAuthentication
from rest_framework.authentication import SessionAuthentication
from rest_framework.exceptions import AuthenticationFailed

from rest_framework.exceptions import AuthenticationFailed

from .models import MemberToken
from .models import Member
from .models import SocialNetwork


logger = logging.getLogger('tscast.auth')


class MemberTokenAuthentication(TokenAuthentication):
    model = MemberToken

    def authenticate_credentials(self, key):
        try:
            token = self.model.objects.get(key=key)
        except self.model.DoesNotExist:
            raise AuthenticationFailed(_('Invalid token.'))

        if token.user.is_deleted:
            raise AuthenticationFailed(_('Member not exists.'))
        return (token.user, token)
