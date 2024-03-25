from django.contrib.auth.password_validation import validate_password

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import exceptions
from rest_framework.permissions import IsAuthenticated

from rest_framework_simplejwt.tokens import RefreshToken


## internal imports
from . import serializers
from Authentication import models as authentication

import json

class Auth(APIView):
    

    def post(self, request):
        """
        This endpoint wil be used to authenticate user

        allowed_methods : POST
        payload : 
            {
                "email" : "valid email id",
                "password" : "valid password"
            }

        expected outputs: 

        1. bad request      400      incorrect payload
        2. user not found   403      incorrect email id
        3. invalid password 403      incorrect password

        """
        data = request.data
        serializer = serializers.LoginSerializer(data=data)
        if not serializer.is_valid():
            err = serializer.errors
            raise exceptions.ValidationError(err, code=400)
        
        email, password = serializer.data.values()
        
        user = authentication.User.objects.filter(email=email, is_active=True)

        if not user.exists():
            raise exceptions.ValidationError({"error":"user not found!"}, code=403)
        
        user = user.first()

        pass_check = user.check_password(password)
        if not pass_check:
            err_obj = authentication.UserLogins.objects.create(user=user, login_status=False,payload=request.data )
            user.no_of_logins += 1
            user.save()
            err_obj.save()
            raise exceptions.PermissionDenied("invalid credentials")   

        # token generation on sucess
        refresh_token = RefreshToken.for_user(user)
        access_token = str(refresh_token.access_token)

        res = Response({
            'prj_access' : access_token
        }, status=200)
        res.set_cookie('prj_refresh',str(refresh_token))

        user.no_of_logins += 1
        user.save()
        login = authentication.UserLogins.objects.create(user=user, login_status=True)
        login.save()
        
        return res
    

class Register(APIView):

    
    def post(self, request, bulk=''):
        
        bulk_action = bulk=='bulk' or False

        if (not request.user.is_superuser) and (bulk):
            raise exceptions.PermissionDenied("Access restricted")
        
        serializer = serializers.RegisterSerilizer(data=request.data, many=bulk_action)
        if not serializer.is_valid():
            raise exceptions.ValidationError(serializer.errors)
        serializer.create(serializer.data)
        data = serializer.data

        return Response({"status":True, 'user': data.get('email')}, status=201)
    

class User(APIView):

    permission_classes = [IsAuthenticated]

    def get(self, request, args=''):

        users = authentication.User.objects.all()
        if args=='admin':
            print("it is here", request.user.role_id or (not request.user.is_superuser))
            if (not request.user.is_superuser) or (request.user.role_id != 1):
                raise exceptions.PermissionDenied({"error":"Access Denied"})
        
            serializer = serializers.BasicUserSerializer(users, many=True)
            return Response(serializer.data)
    
        user_id = request.user.id
        user = users.filter(id=user_id)

        serializer = serializers.BasicUserSerializer(user, many=True)
        # if serializer.is_valid(raise_exception=True):
        return Response(serializer.data)

    
    def put(self, request, args=''):

        user = request.user
        data = request.data
        password = data.get('password') or None

        if not password is None:
            data.pop('password')

        if not user.check_password(password):
            raise exceptions.PermissionDenied("Invalid Password")
        
        if 'role' in data.keys():
            data.pop('role')
        
        user_obj = authentication.User.objects.filter(id=user.id)
        user_obj.update(**data)
        serializer = serializers.BasicUserSerializer(user_obj, many=True)

        return Response(serializer.data, status=204)
    
    def patch(self, request):
        """
        this method is used to update the password alone. 
        payload : {
            'password' : 'current password',
            'new_password' : 'new passowrd',
            'conf_new_password' : 'new password'
        }
        """

        data = request.data
        password = data.get('password') or None
        new_password = data.get('new_password') or None
        conf_new_password = data.get('conf_new_password') or None

        if (password is None) or \
            (new_password is None) or \
            (conf_new_password is None):
            raise exceptions.ValidationError("invalid payload")
        
        user_id = request.user.id
        user_obj = authentication.User.objects.filter(id=user_id).first()

        if not user_obj.check_password(password):
            raise exceptions.ValidationError("invalid password")

        if user_obj.check_password(new_password):
            raise exceptions.ValidationError("old and new password should not be same")
        
        try:
            validate_password(new_password)
        except Exception as same_password:
            raise exceptions.ValidationError("password is common password")

        if new_password!=conf_new_password:
            raise exceptions.ValidationError("password and confirm password do not match!")

        # update if all above checks are done!
        user_obj.set_password(new_password)
        user_obj.save()
        return Response({"status":True, 'user':user_obj.email}, status=202)

    def delete(self, request):
        user_id = request.user.id
        user_obj = authentication.User.objects.filter(id=user_id).first()

        data = request.data

        password = data.get('password')

        if not user_obj.check_password(password):
            raise exceptions.ValidationError("invalid password")

        user_obj.is_active = False
        user_obj.save()
        return Response({"status":True, "detail" : "user is made inactive successfully!"}, status=204)

    
        
