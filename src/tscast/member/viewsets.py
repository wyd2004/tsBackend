import uuid
import requests
from io import BytesIO
from PIL import Image
from hashlib import sha1

from django_filters import FilterSet
from django.urls import reverse
from django.core.files import File
from django.db.models import Count
from django.db.models import Q
from django.http.response import HttpResponseRedirect
from rest_framework import viewsets
from rest_framework import views
from rest_framework.decorators import api_view
from rest_framework.decorators import permission_classes as permission_decorator
from rest_framework.decorators import authentication_classes as authentication_decorator
from rest_framework.response import Response
from rest_framework.exceptions import NotFound
from rest_framework.exceptions import ValidationError
from rest_framework.exceptions import AuthenticationFailed
from rest_framework.permissions import BasePermission


from .models import PodcastAlbumSubscription
from .models import Member
from .models import MemberToken
from .models import SocialNetwork
from .models import MemberToken
from .models import MemberInvitation


from .serializers import PodcastAlbumSubscriptionSerializer
from .serializers import PodcastAlbumSubscribeSerializer
from .serializers import MemberSerializer


from podcast.viewsets import PodcastAlbumViewSet


from wechat.api import get_wechat_oauth_url
from wechat.api import get_user_info_access_token
from wechat.api import get_user_info


from .utils.permissions import OnlyMemberAccess



def wechat_oauth_post(request, format='json'):
    code = request.POST.get('code')
    if code:
        data = get_user_info_access_token(code)
        if data:
            access_token = data.get('access_token')
            openid = data.get('openid')
            user_info = get_user_info(access_token, openid)
            if user_info:
                try:
                    social_network = SocialNetwork.objects.get(identifier=openid, site='wechat')
                    member = social_network.member
                except SocialNetwork.DoesNotExist as error:
                    member = Member()
                    member.username = 'wechat_%s' % openid
                    member.nickname = user_info.get('nickname')
                    avatar_url = user_info.get('headimgurl')
                    if avatar_url:
                        response = requests.get(avatar_url, verify=False)
                        if response.ok:
                            bio = BytesIO(response.content)
                            image = Image.open(bio)
                            suffix = image.format.lower()
                            filename = sha1(response.content).hexdigest()
                            avatar = File(bio, '%s.%s' % (filename, suffix))
                        else:
                            avatar = None
                    else:
                        avatar = None
                    member.avatar = avatar
                    member.save()
                    social_network = SocialNetwork.objects.create(
                            member=member,
                            site='wechat',
                            identifier=openid,
                            nickname=user_info.get('nickname'),
                            avatar=avatar,
                            )
                token = MemberToken.objects.create(user=member)
                data ={
                    'member_id': member.id,
                    'token': token.key,
                    }
                response = Response(data)
            else:
                raise AuthenticationFailed
            return response
    raise AuthenticationFailed


@api_view(['GET', 'POST'])
@permission_decorator([])
def oauth(request, format='json'):
    if request.method == 'GET':
        url = get_wechat_oauth_url('http://vip.tangsuanradio.com/member/oauth/')
        response = HttpResponseRedirect(url)
    elif request.method == 'POST':
        response = wechat_oauth_post(request, format)
    return response


class InvitationActivatePermission(BasePermission):
    def has_permission(self, request, view):
        # if not type(request.user) is Member:
        #     return False
        if request.method in ['POST', 'PUT', 'HEAD', 'DELETED']:
            return False
        return True

    def has_object_permision(self, request, view, obj):
        if request.method in ['POST', 'PUT', 'HEAD', 'DELETED']:
            return False
        else:
            return True


# class WeChatCallbackAuth():
#     pass

@api_view(['GET'])
@permission_decorator([InvitationActivatePermission,])
# authentication_decorator([WeChatCallbackAuth,])
def invitation_activate(request, key, format='json'):
    if not type(request.user) is Member:
        url = reverse('api:invitation-activate', kwargs={'key':key})
        url = 'http://vip.tangsuanradio.com/%s' % url
        url = get_wechat_oauth_url(url)
        return HttpResponseRedirect(url)
    try:
        key = uuid.UUID(key, version=4)
    except ValueError as error:
        raise NotFound
    try:
        invitation = MemberInvitation.objects.get(key=key)
        if invitation.is_activated:
            raise NotFound
        else:
            invitation.user = request.user
            invitation.is_activated = True
            invitation.make_purchase()
            invitation.save()
        return Response('ok')
    except MemberInvitation.DoesNotExist as error:
        raise NotFound


class MemberViewSet(viewsets.ModelViewSet):
    model = Member
    serializer_class = MemberSerializer
    queryset = Member.objects.all()



class PodcastAlbumSubscriptionViewSet(viewsets.ModelViewSet):
    model = PodcastAlbumSubscription
    serializer_class = PodcastAlbumSubscriptionSerializer
    filter_fields = ('member_id',)

    def get_queryset(self):
        queryset = PodcastAlbumSubscription.objects.filter(is_deleted=False)
        if self.kwargs.has_key('member_id'):
            queryset = queryset.filter(member_id=self.kwargs['member_id'])
        return queryset


class PodcastAlbumSubscribePermission(BasePermission):
    def has_permission(self, request, view):
        if type(request.user) == Member:
            return True
        else:
            return False

    def has_object_permission(self, request, view, obj):
        return False


class PodcastAlbumSubscribeViewSet(viewsets.ModelViewSet):
    model = PodcastAlbumSubscription
    serializer_class = PodcastAlbumSubscribeSerializer
    permission_classes = (PodcastAlbumSubscribePermission,)


    def get_queryset(self):
        queryset = PodcastAlbumSubscription.objects.filter(is_deleted=False)
        return queryset

    def create(self, request, *args, **kwargs):
        obj = self.model.objects.filter(
                album_id=kwargs.get('album_id', 0),
                member=request.user,
                is_deleted=False
                ).last()
        if obj:
            data = self.serializer_class(instance=obj).data
            return Response(data)
        else:
            return super(PodcastAlbumSubscribeViewSet, self).create(request, *args, **kwargs)


    def destroy(self, request, *args, **kwargs):
        queryset = self.model.objects.filter(
                album_id=kwargs.get('album_id', 0),
                member=request.user,
                )
        for q in queryset:
            q.is_deleted = True
            q.save()
        return Response(status=204)


class MemberPurchasedAlbumViewSet(PodcastAlbumViewSet):
    def get_queryset(self):
        member_id=self.kwargs.get('member_id',)
        if member_id:
            try:
                member = Member.objects.get(id=member_id)
            except:
                raise NotFound
        privilege = member.privilege
        queryset = self.model.objects.filter(
                is_deleted=False,
                status='publish',
                ).filter(
                Q(id__in=privilege.episode_ids) |\
                Q(channel_id__in=privilege.channel_ids) |\
                Q(episodes__id__in=privilege.episode_ids)
                ).distinct()
        return queryset
