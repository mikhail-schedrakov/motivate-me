from django.forms import widgets
from rest_framework import serializers
from api.models import Profile, CheckPoint, Mentor
from django.contrib.auth.models import User


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User


class ProfileSerializer(serializers.ModelSerializer):
    user = serializers.PrimaryKeyRelatedField()

    class Meta:
        model = Profile


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
	    depth = 2
	    fields = ('id',)


class MentorSerializer(serializers.ModelSerializer):
    user = serializers.PrimaryKeyRelatedField()

    class Meta:
        model = Mentor