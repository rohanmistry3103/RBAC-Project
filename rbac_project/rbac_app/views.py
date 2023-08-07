from django.contrib.auth import authenticate, login, logout
from django.http import JsonResponse
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework.authentication import TokenAuthentication
from rest_framework.exceptions import PermissionDenied
from .models import CustomUser, API, UserAPIAccess
from django.shortcuts import render, redirect
from rest_framework_simplejwt.tokens import RefreshToken



class LoginView(APIView):
    def get(self, request):
        return render(request, 'login.html')

    def post(self, request):
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request,user)
            token = user.tokens
            return render(request,'view_api.html', {'token': token})
        else:
            error_message = "INVALID CREDENTIALS"
            return render(request,'login.html',{'error':error_message})


class LogoutView(APIView):
    def get(self, request):
        user=CustomUser.objects.get(tokens=request.headers['Authorization'].split()[1])
        if user.role == "admin" or user.role == "user":
            logout(request)
            return render(request, 'logout.html')
    
    def post (self, request):
        return render(request, 'logout.html')
        

class SignupView(APIView):
    def get(self, request):
        return render(request, 'signup.html')

    def post(self, request):
        username = request.POST.get('username')
        password1 = request.POST.get('password1')
        password2 = request.POST.get('password2')
        role = request.POST.get('role')
        tokens = request.POST.get('tokens')

        if password1 != password2:
            return render(request, 'signup.html', {'error': 'Passwords do not match.'})

        user = CustomUser.objects.create_user(username=username, password=password1, role=role, tokens=tokens)
        if user is not None:
            refresh = RefreshToken.for_user(user)
            token = str(refresh.access_token)
            user.tokens = token
            user.save()
            # return Response({'token': token}, status=200)
            return redirect ('/login/')
        else:
            return Response({'error': 'Invalid credentials'}, status=401)


class ViewAPI(APIView):
    def get(self, request):
        apis = API.objects.all()
        return render(request, 'view_api.html', {'apis': apis})


class AddAPI(APIView):
    # authentication_classes= (TokenAuthentication,)
    # permission_classes = [IsAuthenticated]
    def get(self, request):
        return render(request, 'add_api.html')

    def post(self, request):
        user=CustomUser.objects.get(tokens=request.headers['Authorization'].split()[1])
        if user.role == 'admin' or user.role == 'user':
            api_name = request.data.get('name')

            if api_name:
                api = API.objects.create(name=api_name, user_id=user)
                return Response(f"API '{api.name}' added successfully.", status=201)
            else:
                return Response("Invalid data provided.", status=400)
        raise PermissionDenied()


class RemoveAPI(APIView):
    def get(self, request):
        return render(request, 'remove_api.html')

    def post(self, request):
        user=CustomUser.objects.get(tokens=request.headers['Authorization'].split()[1])
        if user.role == 'admin':
            try:
                api_id = request.data.get('api_id')
                r_api = API.objects.get(id=api_id)
                r_api.delete()
                return JsonResponse({"message": "API removed successfully"})
            except API.DoesNotExist:
                return Response("API not found.", status=404)
        else :
            return Response("You're not authorized")


class UpdateAPI(APIView):
    def get(self, request):
        return render(request, 'update_api.html')

    def post(self, request):
        user=CustomUser.objects.get(tokens=request.headers['Authorization'].split()[1])
        if user.role == 'admin' or user.role == 'user':
            try:
                api_id = request.data.get('api_Id')
                api = API.objects.get(id=api_id)
                api_name = request.data.get('name')

                if api_name:
                    api.name = api_name
                    api.save()
                    return Response(f"API '{api.name}' updated successfully.", status=200)
                else:
                    return Response("Invalid data provided.", status=400)
            except API.DoesNotExist:
                return Response("API not found.", status=404)
        raise PermissionDenied()


class ViewAllAPIs(APIView):
    def get(self, request):
            apis = API.objects.all()
            return render(request, 'view_all_apis.html', {'apis': apis})

    def post(self, request):
        user=CustomUser.objects.get(tokens=request.headers['Authorization'].split()[1])
        if user.role == 'admin':
            apis = API.objects.all()
            return redirect('/view_all_apis/', {'apis': apis})
        raise PermissionDenied()
    

class AddUser(APIView):
    # authentication_classes= (TokenAuthentication,)
    # permission_classes = [IsAuthenticated]
    def get(self, request):
        return render(request, 'add_user.html')

    def post(self, request):
        user=CustomUser.objects.get(tokens=request.headers['Authorization'].split()[1])
        if user.role == 'admin':
            username = request.data.get('username')
            password = request.data.get('password')
            role = request.data.get('role')
            tokens = request.POST.get('tokens')

            if username and password and role:
                user = CustomUser.objects.create_user(username=username, password=password, role=role, tokens=tokens)
                refresh = RefreshToken.for_user(user)
                token = str(refresh.access_token)
                user.tokens = token
                user.save()
                return Response(f"User '{user.username}' added successfully.", status=201)
            else:
                return Response("Invalid data provided.", status=400)


class RemoveUser(APIView):
    # permission_classes = [IsAuthenticated]
    def get(self, request):
        return render(request, 'remove_user.html')
    
    def post(self, request):
        user=CustomUser.objects.get(tokens=request.headers['Authorization'].split()[1])
        if user.role == 'admin':
            try:
                user_id = request.data.get('user_id')
                r_user = CustomUser.objects.get(id=user_id)
                r_user.delete()
                return Response("Successfully deleted")
            except CustomUser.DoesNotExist:
                return Response("User not found.", status=404)


class UpdateUser(APIView):
    def get(self, request):
        return render(request, 'update_user.html')

    def post(self, request):
        user=CustomUser.objects.get(tokens=request.headers['Authorization'].split()[1])
        if user.role == 'admin':
            try:
                user_id = request.data.get('user_Id')
                user = CustomUser.objects.get(id=user_id)
                user_name = request.data.get('username')
                user_password = request.data.get('password')
                user_role = request.data.get('role')

                if user_name and user_role:
                    user.username = user_name
                    if user_password:
                        user.set_password(user_password)
                    user.role = user_role
                    user.save()
                    return Response(f"User '{user.username}' updated successfully.", status=200)
                else:
                    return Response("Invalid data provided.", status=400)
            except CustomUser.DoesNotExist:
                return Response("User not found.", status=404)


class ViewAllUsers(APIView):
    def get(self, request):
            users = CustomUser.objects.all()
            return render(request, 'view_all_users.html', {'users': users})

    def post(self, request):
        user=CustomUser.objects.get(tokens=request.headers['Authorization'].split()[1])
        if user.role == 'admin':
            users = CustomUser.objects.all()
            return render(request, 'view_all_users.html', {'users': users})
        else :
            return Response("Not authorized !!" )


class ViewUserAPIMappings(APIView):
    def get(self, request):
        if request.user.role == 'admin' or request.user.role == 'user':
            mappings = UserAPIAccess.objects.all()
            return render(request, 'view_user_api_mappings.html', {'mappings': mappings})
        raise PermissionDenied()
        
    def post(self, request):
            mappings = UserAPIAccess.objects.all()
            return render(request, 'view_user_api_mappings.html', {'mappings': mappings})
    
