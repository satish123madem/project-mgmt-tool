from rest_framework import serializers
from rest_framework.exceptions import ValidationError

from django.contrib.auth import password_validation
from django.contrib.auth.password_validation import validate_password

from . import models

class LoginSerializer(serializers.Serializer):
    email = serializers.EmailField()
    password = serializers.CharField(max_length=25)


class RoleSerializer(serializers.ModelSerializer):

    class Meta:
        model = models.Role
        fields = ['id', 'role']

class RegisterSerilizer(serializers.ModelSerializer):
    role = serializers.IntegerField()
    password = serializers.CharField(max_length=25)
    conf_password = serializers.CharField(max_length=25)

    class Meta:
        model = models.User
        fields = ['email', 'username', 'first_name', 'last_name', 'role', 'password', 'conf_password']

    def create(self, validated_data):
        print(validated_data)
        password = validated_data.pop('password')
        conf_password = validated_data.pop('conf_password')
        role = validated_data.pop('role')
        user = self.Meta.model(**validated_data)
        user.role_id = 3
        cmn_password_check = password_validation.CommonPasswordValidator()
        try:
            cmn_password_check = cmn_password_check.validate(password, models.User)
        except Exception as e:
            raise ValidationError({"error" : ",\n".join(e)})
        try:
            validate_password(password)
        except Exception as weak_password:
            raise ValidationError({"error": "weak password :" + " "  + ",\n".join(weak_password)})

        if password!=conf_password:
            raise ValidationError("password and confirm password do not match")
        
        user.set_password(password)
        user.save()
        return user

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.User
        fields = [ 'id', 'email', 'is_active' ]
        extra_kwargs = {
            'email' : { 'required' : False },
            'is_active' :  { 'required' : False }
        }

class BasicUserSerializer(serializers.ModelSerializer):
    role = RoleSerializer(required=False)

    class Meta:
        model = models.User
        fields = [ 'id', 'email', 'first_name', 'last_name', 'username', 'role', 'is_active' ]
        
