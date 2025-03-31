from rest_framework import generics, status, permissions
from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.tokens import RefreshToken
from .models import User
from .serializers import UserSerializer, LoginSerializer
from django.http import JsonResponse


class RegisterView(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [permissions.AllowAny]

    def create(self, request, *args, **kwargs):
        try:
            return super().create(request, *args, **kwargs)
        except Exception as e:
            return Response(
                {"error": f"Registration failed: {str(e)}"},
                status=status.HTTP_400_BAD_REQUEST
            )


class LoginView(APIView):
    permission_classes = [permissions.AllowAny]

    def post(self, request):
        try:
            serializer = LoginSerializer(data=request.data)
            if serializer.is_valid():
                user = serializer.validated_data
                refresh = RefreshToken.for_user(user)
                return Response({
                    "refresh": str(refresh),
                    "access": str(refresh.access_token)
                })
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        except Exception as e:
            return Response(
                {"error": f"Login failed: {str(e)}"},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )


def user_list(request):
    try:
        users = User.objects.all().values()
        return JsonResponse(list(users), safe=False)
    except Exception as e:
        return JsonResponse({"error": f"Failed to fetch users: {str(e)}"}, status=500)
class UserDetailView(APIView):
    """Retrieve user details by user ID"""
    permission_classes = [permissions.AllowAny]  # Adjust as needed

    def get(self, request, user_id):
        try:
            user = User.objects.get(id=user_id)
            serializer = UserSerializer(user)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except User.DoesNotExist:
            return Response({"error": "User not found"}, status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            return Response({"error": f"Failed to fetch user details: {str(e)}"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)



#
# 
#  from rest_framework import generics, status, permissions
# from rest_framework import viewsets
# from rest_framework.response import Response
# from rest_framework.views import APIView
# from rest_framework_simplejwt.tokens import RefreshToken
# from .models import User
# from .serializers import UserSerializer, LoginSerializer
# from django.http import JsonResponse


# class RegisterView(generics.CreateAPIView):
#     queryset = User.objects.all()
#     serializer_class = UserSerializer
#     permission_classes = [permissions.AllowAny]

#     def create(self, request, *args, **kwargs):
#         try:
#             return super().create(request, *args, **kwargs)
#         except Exception as e:
#             return Response(
#                 {"error": f"Registration failed: {str(e)}"},
#                 status=status.HTTP_400_BAD_REQUEST
#             )


# class LoginView(APIView):
#     permission_classes = [permissions.AllowAny]

#     def post(self, request):
#         try:
#             serializer = LoginSerializer(data=request.data)
#             if serializer.is_valid():
#                 user = serializer.validated_data
#                 refresh = RefreshToken.for_user(user)
#                 return Response({
#                     "refresh": str(refresh),
#                     "access": str(refresh.access_token),
#                 })
#             return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

#         except Exception as e:
#             return Response(
#                 {"error": f"Login failed: {str(e)}"},
#                 status=status.HTTP_500_INTERNAL_SERVER_ERROR
#             )


# def user_list(request):
#     try:
#         users = User.objects.all().values()
#         return JsonResponse(list(users), safe=False)
#     except Exception as e:
#         return JsonResponse({"error": f"Failed to fetch users: {str(e)}"}, status=500)
