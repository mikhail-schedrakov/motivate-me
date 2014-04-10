from django.forms import widgets
from rest_framework import serializers
from api.models import Profile, CheckPoint, Mentor
from django.contrib.auth.models import User


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = (
            'id',
            'username',
            'email',
            'is_active',
            'date_joined'
        )


class ProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = Profile
        fields = (
            'age',
            'gender',
            'initial_weight',
            'height',
        )  


class CheckPointSerializer(serializers.ModelSerializer):
    class Meta:
        model = CheckPoint
        fields = ('date',
                  'weight', 
                  'is_planned', 
                  'user')


class UserSignupSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        depth = 1
        fields = ('id',)


class MentorSerializer(serializers.ModelSerializer):
    user = serializers.PrimaryKeyRelatedField()

    class Meta:
        model = Mentor


class CreateUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = (
            'email',
            'password',
        )
        write_only_fields = (
            'password',
            'email',
        )


    def restore_object(self, attrs, instance=None):
        """
        Create new user instance
        """
        user = User(
            email=attrs['email'], 
            username=attrs['email'],
            is_active = False,
        )
        user.set_password(attrs['password'])
        return user