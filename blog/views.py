from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import YourModel
from .serializers import YourModelSerializer

class YourModelListCreateView(APIView):
    def get(self, request):
        your_models = YourModel.objects.all()
        serializer = YourModelSerializer(your_models, many=True)
        return Response(serializer.data)

    def post(self, request):
        serializer = YourModelSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class YourModelDetailView(APIView):
    def get(self, request, pk):
        your_model = YourModel.objects.get(pk=pk)
        serializer = YourModelSerializer(your_model)
        return Response(serializer.data)

    def put(self, request, pk):
        your_model = YourModel.objects.get(pk=pk)
        serializer = YourModelSerializer(your_model, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        your_model = YourModel.objects.get(pk=pk)
        your_model.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.authtoken.models import Token
from rest_framework.response import Response
from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny
from .serializers import UserLoginSerializer
from rest_framework.views import APIView
from .serializers import UserRegistrationSerializer
from rest_framework.permissions import IsAuthenticated
from .permissions import IsAdmin

class UserLoginView(ObtainAuthToken):
    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data,
                                           context={'request': request})
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data['user']
        token, created = Token.objects.get_or_create(user=user)
        return Response({'token': token.key, 'user_id': user.pk})

class UserRegistrationView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        serializer = UserRegistrationSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            return Response({'user_id': user.id}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class AdminOnlyView(APIView):
    permission_classes = [IsAuthenticated, IsAdmin]

    def get(self, request):
        return Response({"message": "This view is only accessible to admins."})
# Create your views here.

