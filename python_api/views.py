from django.shortcuts import render
from rest_framework import viewsets
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.authentication import TokenAuthentication
from rest_framework import filters
from rest_framework.authtoken.serializers import AuthTokenSerializer
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from rest_framework.permissions import IsAuthenticated

from . import serializers
from . import models
from . import permissions

# Create your views here.

class HelloApiView(APIView):
  """Test API View"""

  serializer_class = serializers.HelloSerializer

  def get(self, request, format=None):

    an_apiview = [
      'get',
      'post',
      'put',
      'patch',
      'delete',
    ]

    return Response({
      'message': 'Hello',
      'an_apiview': an_apiview
    })

  def post(self, request):

    serializer = serializers.HelloSerializer(data=request.data)

    if serializer.is_valid():
      name = serializer.data.get('name')
      message = 'Hello {0}'.format(name)

      return Response({ 'message': message })
    else:

      return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

  def put(self, request, pk=None):

      return Response({ 'method': 'put' })

  def patch(self, request, pk=None):

      return Response({ 'method': 'patch' })

  def delete(self, request, pk=None):

      return Response({ 'method': 'delete' })


class HelloViewSet(viewsets.ViewSet):
  """Test API ViewSet"""

  serializer_class = serializers.HelloSerializer

  def list(self, request):

    a_viewset = [
      'list',
      'create',
      'retrieve',
      'update',
      'partial_update',
    ]

    return Response({
      'message': 'Hello',
      'a_viewset': a_viewset
    })

  def create(self, request):

    serializer = serializers.HelloSerializer(data=request.data)

    if serializer.is_valid():
      name = serializer.data.get('name')
      message = 'Hello {0}'.format(name)

      return Response({ 'message': message })
    else:

      return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

  def retrieve(self, request, pk=None):

      return Response({ 'method': 'get' })

  def update(self, request, pk=None):

      return Response({ 'method': 'put' })

  def partial_update(self, request, pk=None):

      return Response({ 'method': 'patch' })

  def destroy(self, request, pk=None):

      return Response({ 'method': 'delete' })


class UserViewSet(viewsets.ModelViewSet):
  """User ViewSet"""

  serializer_class = serializers.UserSerializer
  queryset = models.User.objects.all()
  authentication_classes = (TokenAuthentication,)
  permission_classes = (permissions.UpdateOwnProfile,)
  filter_backends = (filters.SearchFilter,)
  search_fields = ('name', 'email',)

class LoginViewSet(viewsets.ViewSet):
  """Checks email, password and returns an auth token"""

  serializer_class = AuthTokenSerializer

  def create(self, request):
    """Use the ObtainAuthToken APIView to validate and create a token"""

    return ObtainAuthToken.as_view()(request=request._request)


class UserProfileFeedViewSet(viewsets.ModelViewSet):
  """Handles creating and updating profile feed items"""

  authentication_classes = (TokenAuthentication,)
  serializer_class = serializers.ProfileFeedItemSerializer
  queryset = models.ProfileFeedItem.objects.all()
  permission_classes = (permissions.PostOwnStatus, IsAuthenticated)

  def perform_create(self, serializer):
    """Sets the user profile to the logged in user"""

    serializer.save(user_profile=self.request.user)
