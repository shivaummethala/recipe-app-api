# update views.py and add a view for managing our create user api
from rest_framework import generics, authentication, permissions
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.settings import api_settings

from user.serializers import UserSerializer, AuthTokenSerializer


class CreateUserView(generics.CreateAPIView):
    """Create a new user in the system"""
    serializer_class = UserSerializer


class CreateTokenView(ObtainAuthToken):
    """Create a new auth token for user"""
    serializer_class = AuthTokenSerializer
    # sets the renderer so we can view this endpoint in the browser with the browsable api
    # can also able to get the token with Postman
    renderer_classes = api_settings.DEFAULT_RENDERER_CLASSES
    # store the retrieved token in cookie or persistent storage to authenticate end points


class ManageUserView(generics.RetrieveUpdateAPIView):
    """Manage the authenticated user - update the user params like name, password etc.."""
    serializer_class = UserSerializer
    # use token authentication using authentication module
    # use permissions module for level of access that user has
    authentication_classes = (authentication.TokenAuthentication,)
    permission_classes = (permissions.IsAuthenticated,)

    def get_object(self):
        """Retrieve and return authentication users"""
        return self.request.user

    """when the get object is called the request, will have the user attached to it 
       because of the authentication classes that takes care of take getting the authenticated
       user and assigning it to request. This is a great feature of Django rest framework"""
