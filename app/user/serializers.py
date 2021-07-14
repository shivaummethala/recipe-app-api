from django.contrib.auth import get_user_model, authenticate
from django.utils.translation import ugettext_lazy as _  # translate to required language
from rest_framework import serializers


class UserSerializer(serializers.ModelSerializer):
    """Serializer for the users object"""

    class Meta:
        model = get_user_model()
        # fields to be included in serializer and convert to and from json, when we make HTTP Post
        # and retrieve in view to save it to model
        fields = ('email', 'password', 'name')
        extra_kwargs = {'password': {'write_only': True, 'min_length': 5}}

    def create(self, validated_data):
        """Create a new user with encrypted password and return it"""
        return get_user_model().objects.create_user(**validated_data)

    def update(self, instance, validated_data):
        """Update a User, setting the password correctly and return it"""
        # instance is model instance that is linked to our model serializer that's going to be our user object.
        # The validated data is going to be these fields that have been through the validation and ready to update.
        # pop the old password from dictionary and replace with None
        password = validated_data.pop('password', None)
        user = super().update(instance, validated_data)

        if password:
            user.set_password(password)  # set new password
            user.save()
        return user


class AuthTokenSerializer(serializers.Serializer):
    """Serializer for the user authentication object"""
    email = serializers.CharField()  # by default it will trim the whitespace in email
    password = serializers.CharField(   # ignore trim whitespace in password
        style={'input_type': 'password'},
        trim_whitespace=False
    )

    def validate(self, attrs):
        """Validate and authenticate the user"""
        email = attrs.get('email')
        password = attrs.get('password')

        # to authenticate our request for token
        user = authenticate(
            request=self.context.get('request'),
            username=email,
            password=password
        )
        if not user:
            msg = _('Unable to authenticate with provided credentials')  # _ for translation to different languages
            raise serializers.ValidationError(msg, code='authentication')

        attrs['user'] = user
        # once validation is done, return attributes
        return attrs
