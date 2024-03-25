from rest_framework import serializers
from . import models

from Authentication import serializers as auth_serializers

class StatusSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = models.Status
        fields = '__all__'

class ProjectSerializer(serializers.ModelSerializer):

    class Meta:
        model = models.Project  
        fields = ['name', 'description', 'start_date', 'end_date', 'status' ]

    def create(self, validated_data, user_id):
        # owner = validated_data.pop('created_by')
        status = validated_data.pop('status')
        obj = self.Meta.model(**validated_data)
        obj.status_id = status
        obj.created_by_id = user_id
        obj.save()
        return obj

    
class ProjectViewSerializer(serializers.ModelSerializer):
    created_by = auth_serializers.BasicUserSerializer(required=False)
    status = StatusSerializer(required=False)

    class Meta:
        model = models.Project
        fields = ['name', 'description', 'created_by', 'start_date', 'end_date', 'status', 'is_deleted' ]

class TeamViewSerializer(serializers.ModelSerializer):
    users = auth_serializers.BasicUserSerializer(read_only=True, many=True)
    project = ProjectViewSerializer(required=False)

    class Meta:
        model = models.Team
        fields = ['id','name', 'project', 'users']


class TaskViewSerializer(serializers.ModelSerializer):
    project = ProjectViewSerializer(read_only=True)
    created_by = auth_serializers.UserSerializer(read_only=True)
    assigned_to = auth_serializers.UserSerializer(read_only=True)
    status = StatusSerializer(read_only=True)
    
    class Meta:
        model = models.Task
        fields = ['id','name', 'description', 'project', 'created_by', 'assigned_to', 'due_date', 'status', 'priority' ]

    def create(self, validated_data, req_data):
        print(validated_data, req_data)
        instance  = self.Meta.model(**validated_data)
        instance.assigned_to_id = req_data.get('assigned_to')
        instance.created_by_id = req_data.get('created_by')
        instance.project_id = req_data.get('project_id')
        instance.status_id = 1
        instance.save()
        return instance