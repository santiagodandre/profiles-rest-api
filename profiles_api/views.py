from rest_framework.views import APIView
# To return responses form API views 
from rest_framework.response import Response
# List of HTTP state codes that can be used when returning responses 
from rest_framework import status
from profiles_api import serializers

# Create APIView Class
class HelloApiView(APIView):
    """ Test API View - Based on APIView """
    serializer_class = serializers.HelloSerializer

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