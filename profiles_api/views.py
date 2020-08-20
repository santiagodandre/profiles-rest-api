from rest_framework.views import APIView
# To return responses form API views 
from rest_framework.response import Response
# List of HTTP state codes that can be used when returning responses 
from rest_framework import status
from rest_framework import viewsets
# Generate a random token
from rest_framework.authentication import TokenAuthentication
from rest_framework import filters
# ObtainAuthToken & api_settings needed to create login api 
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.settings import api_settings
from rest_framework.permissions import IsAuthenticated

from profiles_api import serializers
from profiles_api import models
from profiles_api import permissions

# Create APIView Class

class HelloApiView(APIView):
    """ Test API View - Based on APIView """
    serializer_class = serializers.HelloSerializer

    # In APIView you add functions for a particular HTTP Method that you want to support on your endpoint  

    # get : retrieve a list of objects or an specific object
    # format is used to add a format sufix, to the end of the endpoint URL
    def get(self, request, format=None):
        """ Returns a list of APIViews features """
        an_apiview = [
            'Uses HTTP methods as functions (get, post, patch, put, delete)',
            'Is similar to a traditional Django view',
            'Gives you the most control over your app logic',
            'Its mapped manually to URLs',
        ]

        # Every function must return a Response object 
        # A response must contain a dictionary or a list 
        # It converts the Response object to a json 
        return Response({'message': 'Hello', 'an_apiview': an_apiview})

    def post(self, resquest):
        """ Create a Hello message with our name """
        serializer = self.serializer_class(data=resquest.data)
        # Validate the serializer
        if serializer.is_valid():
            name = serializer.validated_data.get('name') 
            message = f'Hello {name}'
            return Response({'message': message})
        else:
            # Return a 400 bad request 
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST )

    def put(self, request, pk=None):
        """ Handle updating an object """
        return Response({'method': 'PUT'})

    def patch(self, request, pk=None):
        """ Handle a partial update of an object """ 
        return Response({'method': 'PATCH'})
    
    def delete(self, request, pk=None):
        """ Delete an object """
        return Response({'method': 'DELETE'})

class HelloViewSet(viewsets.ViewSet):
    """ Test API View Sets  """

    serializer_class = serializers.HelloSerializer

    # In View Sets , you add functions that represents actions that you will perform on a typical API 

    # List a set of objects that the view set represents 
    def list(self, request):
        """ Return a Hello Message """
        a_viewset = [
            'Uses actions (list, crate, retrieve, update, partial_update)',
            'Automatically maps to URLs using Routers',
            'Provides more functionality with less code',
        ]
        return Response({'message': 'Hello', 'a_viewset': a_viewset})

    def create(self, request):
        """ Create a new hello message"""
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            name = serializer.validated_data.get('name')
            message = f'Hello {name}!'
            return Response({'message': message})
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def retrieve(self, request, pk=None):
        """ Handle getting an object by its id """
        return Response({'http_method': 'GET'})

    def update(self, request, pk=None):
        """ Handle updating an object  """
        return Response({'http_method': 'PUT'})

    def partial_update(self, request, pk=None):
        """ Handle updating part of an object """
        return Response({'http_method': 'PATCH'})

    def destroy(self, request, pk=None):
        """ Handle removing an object """
        return Response({'http_method': 'DELETE'})

# Usamos ModelViewset to handle models 
class UserProfileViewSet(viewsets.ModelViewSet):
    """ Handle creating and updating profiles """
    serializer_class = serializers.UserProfileSerializer
    queryset = models.UserProfile.objects.all()
    # Set how the user will uthenticate 
    authentication_classes = (TokenAuthentication, )
    # how the user gets permission to certain thing 
    permission_classes = (permissions.UpdateOnwProfile,)
    # Add filter backend
    filter_backends = (filters.SearchFilter, )
    # Specify the search fields
    search_fields = ('name', 'email')
    
class UserLoginApiView(ObtainAuthToken):
    """ Handle creating user authentication tokens """
    renderer_classes = api_settings.DEFAULT_RENDERER_CLASSES

class UserProfileFeedViewSet(viewsets.ModelViewSet):
    """ Handle creating reading and updating profile feed items """
    # Authenticate Requests 
    authentication_classes = (TokenAuthentication, )
    # Set serializer 
    serializer_class = serializers.ProfileFeedItemSerializer
    # Asign query set --> To manage all objects in our model 
    queryset = models.ProfileFeedItem.objects.all()
    permission_classes = (
        permissions.UpdateOwnStatus, 
        IsAuthenticated,
    )

    # Se la llama cada vez que hago un HTTP Post a nuestra vista
    # When a new object is created, django rest framework calls perform_create and passes the serializer
    # The serializer is a ModelSerializer, so it has a save function to save the content of the serializar into de db 
    # We override the save and pass a user_profile keyword
    def perform_create(self, serializer):
        """ Sets the user profile to the logged in user """
        serializer.save(user_profile=self.request.user)