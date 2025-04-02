from django.urls import path, include
from .views import RegisterView, LoginView, user_list, UserDetailView,MakeAdminView
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView



urlpatterns = [
    path('register/', RegisterView.as_view(), name='register'),
    path('login/', TokenObtainPairView.as_view(), name='login'), 
    # path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('usersz/', user_list),
    path("users/<int:user_id>/", UserDetailView.as_view(), name="user_detail"),
    path("make-admin/<int:user_id>/", MakeAdminView.as_view(), name="make-admin"),


]



# from django.urls import path, include
# from .views import RegisterView, LoginView, user_list
# from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView



# urlpatterns = [
#     path('register/', RegisterView.as_view(), name='register'),
#     path('login/', TokenObtainPairView.as_view(), name='login'), 
#     path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
#     path('usersz/', user_list),

# ]

