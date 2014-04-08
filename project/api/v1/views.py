from django.shortcuts import render
from api.models import Profile, CheckPoint, Mentor
from django.contrib.auth.models import User

from api.v1.serializers import UserSerializer
from api.v1.serializers import UserSignupSerializer
from api.v1.serializers import ProfileSerializer
from api.v1.serializers import CheckPointSerializer
from api.v1.serializers import MentorSerializer

from rest_framework import generics
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from django.shortcuts import get_object_or_404

from rest_framework.authentication import BasicAuthentication
from rest_framework.permissions import IsAuthenticated
from oauth2_provider.ext.rest_framework import TokenHasReadWriteScope, TokenHasScope
from django.views.decorators.csrf import csrf_exempt, csrf_protect


class UserList(generics.ListAPIView, generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer


class UserSignup(APIView):
    """
    Signup new user
    """
    def post(self, request, format=None):
        serializer = UserSignupSerializer(data=request.DATA)
        if serializer.is_valid():
            user = User.objects.create_user(
                serializer.init_data['email'],
                serializer.init_data['email'],
                serializer.init_data['password']
            )
            user.save()
            serialized_user = UserSignupSerializer(user)
            return Response(serialized_user.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)



class UserAccount(APIView):
    """
    User accaunt
    """
    authentication_classes = (BasicAuthentication,)
    permission_classes = (IsAuthenticated,)
    

    def put(self, request, format=None):
        user = User.objects.get(id=request.user.id)
        serializer = UserSerializer(user, data=request.DATA)
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
        profile = Profile.objects.get(user=request.user.id)
        serializer = ProfileSerializer(profile)
        return Response(serializer.data)

        
    def post(self, request, format=None):
        serializer = ProfileSerializer(data=request.DATA)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


    def put(self, request, format=None):
        profile = Profile.objects.get(user=request.user.id)
        serializer = ProfileSerializer(profile, data=request.DATA)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)



class UserCheckpoints(APIView):
	"""
	CR - user checpoints
	"""
	authentication_classes = (BasicAuthentication,)
	permission_classes = (IsAuthenticated,)
    

	def post(self, request, format=None):
		serializer = CheckPointSerializer(data=request.DATA)
		if serializer.is_valid():
			serializer.save()
			return Response(serializer.data, status=status.HTTP_201_CREATED)
		return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


	def get(self, request, format=None):
		checkpoint = CheckPoint.objects.filter(is_planned=True, user=request.user.id)
		serializer = CheckPointSerializer(checkpoint, many=True)
		return Response(serializer.data)



class UserCheckpointsPagination(APIView):
    authentication_classes = (BasicAuthentication,)
    permission_classes = (IsAuthenticated,)

    def get(self, request, offset, limit, format=None):
        offset = int(offset)
        limit = int(limit)
        checkpoint = CheckPoint.objects.filter(is_planned=True, user=request.user.id)[offset: limit]
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
        mentors = Mentor.objects.filter(user=request.user.id)
        serializer = MentorSerializer(mentors, many=True)
        return Response(serializer.data)