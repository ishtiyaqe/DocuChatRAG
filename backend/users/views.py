from rest_framework import viewsets
from django.contrib.auth import  authenticate
from django.core.exceptions import ValidationError
from .serializers import UserSerializer
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth import authenticate
from django.http import JsonResponse
from rest_framework_simplejwt.views import TokenObtainPairView
from django.contrib.auth.models import User


class LoginView(APIView):
    def post(self, request):
        username = request.data.get('username')
        password = request.data.get('password')
        user = authenticate(username=username, password=password)
        if user is not None:
            login(request, user)  # Logs the user in and creates a session
            return JsonResponse({'detail': 'Login successful'}, status=status.HTTP_200_OK)
        return JsonResponse({'detail': 'Invalid credentials'}, status=status.HTTP_401_UNAUTHORIZED)



class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer

from django.contrib.auth import authenticate
from django.contrib.auth import authenticate, login
from django.views.decorators.csrf import csrf_exempt
from rest_framework.settings import api_settings
from django.utils.decorators import method_decorator
from django.contrib.auth import get_user_model, login, logout
from rest_framework.authentication import SessionAuthentication
from rest_framework.decorators import permission_classes, authentication_classes

from rest_framework import status, permissions, views
from rest_framework.authentication import TokenAuthentication
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.authtoken.models import Token
from .serializers import *
from rest_framework.views import APIView
from rest_framework_simplejwt.authentication import JWTAuthentication
from django.contrib.auth.decorators import login_required

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated

class ProtectedView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        serializer = UserSerializer(request.user)
        # Return the serialized data as a JSON response
        return JsonResponse({'user': serializer.data}, status=200)


class UserLogout(APIView):
    permission_classes = [permissions.AllowAny]
    authentication_classes = [SessionAuthentication]

    def post(self, request):
        logout(request)
        return Response(status=status.HTTP_200_OK)




 
class MyAccountView(APIView):
    permission_classes = [IsAuthenticated]
    authentication_classes = [SessionAuthentication]

    def get(self, request, format=None):
        user = request.user

        # Fetch all search queries associated with the current user
        # search_queries = SearchQuery.objects.filter(user=user)

        # Serialize the search queries
        search_query_data = []
        # for query in search_queries:
        #     search_query_data.append({
        #         'id': query.id,
        #         'query': query.query,
        #         'status': query.status,
        #         # 'product': ProductSerializer(query.product).data if query.product else None,
        #     })

        # Serialize the user data
        user_serializer = UserSerializer(user)

        # Return the serialized data
        return Response({
            'user': user_serializer.data,
            # 'search_queries': search_query_data,
        })

    def delete(self, request, format=None):
        user = request.user
        query_id = request.data.get('query_id')

        if not query_id:
            return Response({"error": "Query ID is required"}, status=status.HTTP_400_BAD_REQUEST)

        # try:
        #     search_query = SearchQuery.objects.get(id=query_id, user=user)
        #     search_query.delete()
        #     return Response({"message": "Search query deleted successfully"}, status=status.HTTP_204_NO_CONTENT)
        # except SearchQuery.DoesNotExist:
        #     return Response({"error": "Search query not found"}, status=status.HTTP_404_NOT_FOUND)
        
  
    
  


from .validations import *

class UserRegister(APIView):
    permission_classes = (permissions.AllowAny,)

    def post(self, request):
        clean_data = custom_validation(request.data)
        serializer = UserRegisterSerializer(data=clean_data)
        if serializer.is_valid(raise_exception=True):
            user = serializer.create(clean_data)

   
            if user:
                return Response(serializer.data, status=status.HTTP_201_CREATED)
        
        return Response(status=status.HTTP_400_BAD_REQUEST)
    
@method_decorator(csrf_exempt, name='dispatch')
class UserLogin(APIView):
    permission_classes = (permissions.AllowAny,)
    authentication_classes = []  # Disable SessionAuthentication for login itself

    def post(self, request):
        username = request.data.get('username')
        password = request.data.get('password')

        if not username or not password:
            return Response({'error': 'Invalid input data'}, status=status.HTTP_400_BAD_REQUEST)

        user = authenticate(username=username, password=password)
        if user is not None:
            login(request, user)
            serializer = UserSerializer(user)
            return Response({
                'message': 'Login successful',
                'user': serializer.data
            }, status=status.HTTP_200_OK)
        else:
            return Response({'error': 'Invalid username or password'},
                            status=status.HTTP_401_UNAUTHORIZED)


from rest_framework import generics, status
from rest_framework.response import Response
from rest_framework.permissions import AllowAny
from django.contrib.auth import get_user_model
from rest_framework_simplejwt.tokens import RefreshToken
from .serializers import UserSerializer, TokenSerializer

User = get_user_model()

class RegisterView(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = (AllowAny,)

class ObtainTokenView(generics.GenericAPIView):
    permission_classes = (AllowAny,)

    def post(self, request, *args, **kwargs):
        username = request.data.get('username')
        password = request.data.get('password')
        user = User.objects.filter(username=username).first()

        if user and user.check_password(password):
            refresh = RefreshToken.for_user(user)
            serializer = TokenSerializer(data={
                'access': str(refresh.access_token),
                'refresh': str(refresh),
            })
            serializer.is_valid()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response({'detail': 'Invalid credentials'}, status=status.HTTP_400_BAD_REQUEST)
