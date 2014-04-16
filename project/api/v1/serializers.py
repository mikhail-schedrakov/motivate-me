from django.forms import widgets
from rest_framework import serializers
from api.models import Profile, CheckPoint, Mentor, CustomUser
from django.contrib.auth import get_user_model


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = get_user_model()
        fields = (
            'id',
            'email',
            'is_active',
            'create_date',
        )


class SignupUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = get_user_model()
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
        user = get_user_model()(
            email = attrs['email'], 
            is_active = False,
        )
        user.set_password(attrs['password'])
        return user


class CreateProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = Profile
        fields = (
            'age',
            'gender',
            'initial_weight',
            'height',
        )

    def restore_object(self, attrs, instance=None):
        profiel = Profile(
            age = attrs['age'], 
            gender = attrs['gender'],
            initial_weight = attrs['initial_weight'],
            height = attrs['height'],
            user = self.context['request'].user
        )
        return profiel


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
        fields = ('id',
                  'date',
                  'weight', 
                  'is_planned')

    def restore_object(self, attrs, instance=None):
        checkpoint = CheckPoint(
            date=attrs['date'], 
            weight=attrs['weight'],
            is_planned = attrs['is_planned'],
            user = self.context['request'].user
        )
        return checkpoint


class MentorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Mentor
        fields = (
            'id',
            'email',
        )

    def restore_object(self, attrs, instance=None):
        mentor = Mentor(
            email = attrs['email'],
            user = self.context['request'].user
        )
        return mentor