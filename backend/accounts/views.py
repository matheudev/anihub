from rest_framework.views import APIView
from rest_framework import permissions
from django.contrib import auth
from userProfile.models import UserProfile
from .serializers import UserSerializer

from django.contrib.auth.models import User
from rest_framework.response import Response
from django.views.decorators.csrf import ensure_csrf_cookie, csrf_protect
from django.utils.decorators import method_decorator

@method_decorator(csrf_protect, name='dispatch')
class CheckAuthenticatedView(APIView):
    def get(self, request, format=None):
        user = self.request.user

        try:
            isAuthenticated = user.is_authenticated

            if isAuthenticated:
                return Response({ 'isAuthenticated': 'success' })
            else:
                return Response({ 'isAuthenticated': 'error' })
        except:
            return Response({ 'error': 'Something went wrong when checking authentication status' })

@method_decorator(csrf_protect, name='dispatch')
class SignupView(APIView):
    permission_classes = (permissions.AllowAny,)

    def post(self, request, format=None):
        data = self.request.data

        username = data['username']
        password = data['password']
        rePassword = data['rePassword']
        email = data['email']

        try:
            if password == rePassword:
                if User.objects.filter(username=username).exists():
                    return Response({'error': 'Username already exists'})
                else:
                    if len(password) < 6:
                        return Response({'error': 'Password must be at least 6 characters'})
                    else:
                        user = User.objects.create_user(username=username, password=password, email=email)
                        user.save()

                        user = User.objects.get(id=user.id)

                        user_profile = UserProfile(user=user, firstName='', lastName='')
                        user_profile.save()

                        return Response({'success': 'User created successfully'})
            else:
                return Response({'error': 'Passwords do not match'})
        except:
                return Response({'error': 'Something went wrong when registering account'})
        
@method_decorator(csrf_protect, name='dispatch')
class LoginView(APIView):
    permission_classes = (permissions.AllowAny,)

    def post(self, request, format=None):
        data = self.request.data

        username = data['username']
        password = data['password']

        try:
            user = auth.authenticate(username=username, password=password)

            if user is not None:
                auth.login(request, user)

                return Response({'success': 'User logged in', 'username': username})
            else:
                return Response({'error': 'Error logging in'})
        except:
            return Response({'error': 'Something went wrong when logging in'})

class LogoutView(APIView):
    def post(self, request, format=None):
        try:
            auth.logout(request)

            return Response({'success': 'User logged out'})
        except:
            return Response({'error': 'Something went wrong when logging out'})
    
@method_decorator(ensure_csrf_cookie, name='dispatch')      
class GetCSRFToken(APIView):
    permission_classes = (permissions.AllowAny,)

    def get(self, request, format=None):
        return Response({'success': 'CSRF cookie set'})
    
class GetUsersView(APIView):
    permission_classes = (permissions.AllowAny,)

    def get(self, request, format=None):
        users = User.objects.all()

        users = UserSerializer(users, many=True)
        return Response(users.data)