from django.shortcuts import render
from api.models import Profile, CheckPoint, Mentor
from django.contrib.auth.models import User

from api.v1.serializers import UserSerializer
from api.v1.serializers import CreateUserSerializer
from api.v1.serializers import UserSignupSerializer
from api.v1.serializers import ProfileSerializer
from api.v1.serializers import CheckPointSerializer
from api.v1.serializers import MentorSerializer

from rest_framework import status
from rest_framework import mixins
from rest_framework import generics
from rest_framework.views import APIView
from rest_framework.response import Response
from django.shortcuts import get_object_or_404
from rest_framework.renderers import JSONRenderer

from django.core.mail import send_mail
from rest_framework.permissions import IsAuthenticated
from rest_framework.authentication import BasicAuthentication
from oauth2_provider.ext.rest_framework import TokenHasReadWriteScope, TokenHasScope


class UserSignup(APIView):
    """
    Signup new user
    """
    def post(self, request, format=None):
        serializer = CreateUserSerializer(data=request.DATA)
        # import pdb; pdb.set_trace()
        if serializer.is_valid():
            serializer.save()
            user = User.objects.latest('id')
            serializer = UserSerializer(user)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class ProfileDetail(mixins.CreateModelMixin, APIView):
    authentication_classes = (BasicAuthentication,)
    permission_classes = (IsAuthenticated,)
    serializer_class = ProfileSerializer

    def pre_save(self, obj):
        obj.user = self.request.user

    def post(self, request, *args, **kwargs):
        return self.create(request, *args, **kwargs)

    def get(self, request, format=None):
        profile = get_object_or_404(Profile, user=request.user.id)
        serializer = ProfileSerializer(profile)
        return Response(serializer.data)

    def put(self, request, format=None):
        profile = Profile.objects.get(user=request.user.id)
        serializer = ProfileSerializer(profile, data=request.DATA)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class UserProfile(APIView):
    """
    CRU - user profile
    """
    authentication_classes = (BasicAuthentication,)
    permission_classes = (IsAuthenticated,)

    def get(self, request, format=None):
        profile = get_object_or_404(Profile, user=request.user.id)
        serializer = ProfileSerializer(profile)
        return Response(serializer.data)
            

    def put(self, request, format=None):
        profile = Profile.objects.get(user=request.user.id)
        serializer = ProfileSerializer(profile, data=request.DATA)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class CheckpointList(mixins.CreateModelMixin, 
                     mixins.RetrieveModelMixin, 
                     generics.GenericAPIView):
    """
    List checpoints
    """
    authentication_classes = (BasicAuthentication,)
    permission_classes = (IsAuthenticated,)
    serializer_class = CheckPointSerializer

    def get_queryset(self):
        user = self.request.user
        return CheckPoint.objects.filter(user=user)

    def pre_save(self, obj):
        obj.user = self.request.user

    def post(self, request, *args, **kwargs):
        return self.create(request, *args, **kwargs)        


class UserCheckpoints(APIView):
    """
    CR - user checpoints
    """
    authentication_classes = (BasicAuthentication,)
    permission_classes = (IsAuthenticated,)

    def post(self, request, format=None):
        serializer = CheckPointSerializer(data=request.DATA, context={'request': request})
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def get(self, request, format=None):
        checkpoint = CheckPoint.objects.filter(is_planned=False, user=request.user.id)
        serializer = CheckPointSerializer(checkpoint, many=True)
        return Response(serializer.data)


class UserCheckpointsPagination(APIView):
    authentication_classes = (BasicAuthentication,)
    permission_classes = (IsAuthenticated,)

    def get(self, request, offset, limit, format=None):
        offset = int(offset)
        limit = int(limit)
        checkpoint = CheckPoint.objects.filter(is_planned=False, user=request.user.id)[offset: limit]
        serializer = CheckPointSerializer(checkpoint, many=True)
        return Response(serializer.data)


class UserMentor(APIView):
    """
    CR - user mentors
    """
    authentication_classes = (BasicAuthentication,)
    permission_classes = (IsAuthenticated,)


    def post(self, request, format=None):
        serializer = MentorSerializer(data=request.DATA)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


    def get(self, request, format=None):
        # send_mail('Subject here', 'Here is the message.', 'mikhail.schedrakov@gmail.com',['mikhail.schedrakov@gmail.com'], fail_silently=False)

        mentors = Mentor.objects.filter(user=request.user.id)
        serializer = MentorSerializer(mentors, many=True)
        return Response(serializer.data)