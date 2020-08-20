from rest_framework import serializers
from profiles_api import models

class HelloSerializer(serializers.Serializer):
    """ Serializes a name field for testing our API View"""
    name = serializers.CharField(max_length=10)

class UserProfileSerializer(serializers.ModelSerializer):
    """ Serializes a user profile object """ 
    # Use a Meta class to configure the serializer according to a specific model

    class Meta:
        model = models.UserProfile
        # Provide a list of fields in our model we want to manage with our serializer
        fields = ('id', 'email', 'name', 'password')
        extra_kwargs = {
            'password': {
                'write_only': True,
                'style': {'input_type': 'password'}
            }
        }

    #Override the create function to hash the password 
    def create(self, validated_data):
        """ Create and return a new user """
        user = models.UserProfile.objects.create_user(
            email=validated_data['email'],
            name=validated_data['name'],
            password=validated_data['password']
        )

        return user 

class ProfileFeedItemSerializer(serializers.ModelSerializer):
    """ Serializes profile feed items """

    class Meta:
        model = models.ProfileFeedItem
        fields = ('id', 'user_profile', 'status_text', 'created_on')
        extra_kwargs = {'user_profile': {'read_only': True}}
        