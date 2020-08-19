from rest_framework.views import APIView
# To return responses form API views 
from rest_framework.response import Response 

# Create APIView Class
class HelloApiView(APIView):
    """ Test API View - Based on APIView """

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