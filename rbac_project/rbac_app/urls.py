from django.urls import path
from rest_framework_simplejwt import views as jwt_views
from .views import AddUser, RemoveUser, UpdateUser, AddAPI, RemoveAPI, UpdateAPI, ViewAPI,ViewAllUsers, ViewAllAPIs, ViewUserAPIMappings, LoginView, LogoutView, SignupView
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

urlpatterns = [
    path('login/', LoginView.as_view(), name='login'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('signup/', SignupView.as_view(), name='signup'),
    path('add-user/', AddUser.as_view(), name='add_user'),
    path('remove-user/', RemoveUser.as_view(), name='remove_user'),
    path('update-user/', UpdateUser.as_view(), name='update_user'),
    path('add-api/', AddAPI.as_view(), name='add_api'),
    path('remove-api/', RemoveAPI.as_view(), name='remove_api'),
    path('update-api/', UpdateAPI.as_view(), name='update_api'),
    path('view-api/', ViewAPI.as_view(), name='view_api'),
    path('view_all_users/', ViewAllUsers.as_view(), name='view_all_users'),
    path('view_all_apis/', ViewAllAPIs.as_view(), name='view_all_apis'),
    path('view_user_api_mappings/', ViewUserAPIMappings.as_view(), name='view_user_api_mappings'),
    path('api/token/', jwt_views.TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', jwt_views.TokenRefreshView.as_view(), name='token_refresh'),
]

