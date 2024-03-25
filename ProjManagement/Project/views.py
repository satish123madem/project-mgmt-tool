from django.db.models import Q

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import exceptions
from rest_framework.permissions import IsAuthenticated

from Authentication import models as authentication
from . import models
from . import serializers


class Project(APIView):
    
    permission_classes = [IsAuthenticated]

    def get_user_obj(self, request):
        user_id = request.user.id
        user = authentication.User.objects.filter(id=user_id)
        return user.first()

    def post(self, request):
        
        user = self.get_user_obj(request)
        role = user.role.id

        if not role==1:
            raise exceptions.PermissionDenied("Access denied to create project")
        
        data = request.data
        serializer = serializers.ProjectSerializer(data=data)
        if serializer.is_valid(raise_exception=True):
            serializer.create(serializer.data, user_id=user.id)
            return Response(serializer.data, status=201)

    def get(self, request, id=None):
        
        user = self.get_user_obj(request)
        if not id is None:
            query = models.Project.objects.filter(created_by=user,id=id)
            if not query.exists():
                raise exceptions.ValidationError({"error":"No such project with given id (created by you)"})
            
            query = query.first()
            serializer = serializers.ProjectViewSerializer(instance=query)
            return Response(serializer.data, status=200)

        query = models.Project.objects.filter(created_by=user)
        serializer = serializers.ProjectViewSerializer(query, many=True)
        return Response(serializer.data, status=200)
    
    def put(self, request, id=None):
        if not id is None:
            raise exceptions.NotFound("Endpoint not found")
        user = self.get_user_obj(request)
        data = request.data
        prj_id = data.get('id') or None
        updates = data.get('update')
        if prj_id is None:
            raise exceptions.ValidationError({"error":"provide project Id"})
        
        if updates is None:
            raise exceptions.ValidationError({"error":"provide updates for project"})

        data.pop('id')
        query = models.Project.objects.filter(created_by=user, id=prj_id)

        if not query.exists():
            raise exceptions.ValidationError({"error":"No such project with given id (created by you)"})
        
        query.update(**updates)
        return Response(query.values(), status=202)
    
    def delete(self, request, id=None):
        user = self.get_user_obj(request)
        prj_id = id
 
        if prj_id is None:
            raise exceptions.ValidationError({"error":"provide project Id"})

        query = models.Project.objects.filter(created_by=user, id=prj_id)
        
        if not query.exists():
            raise exceptions.ValidationError({"error":"No such project with given id (created by you)"})
        
        query.update(is_deleted=True)
        return Response({}, status=204)

class Team(APIView):
    
    permission_classes = [IsAuthenticated]

    def get_user_obj(self, request=None, id=None):

        user_id = id if not id is None else request.user.id 
        user = authentication.User.objects.filter(id=user_id)
        return user.first()
    
    def post(self, request, id=None, action=''):
        
        user = self.get_user_obj(request)
        if user.role.id!=1:
            raise exceptions.ValidationError("You are not authorized to create Team")
        
        data = request.data

        prj_id = data.get('project_id') or None
        name = data.get('name') or None
        users = data.get('users') or []

        if (prj_id is None) or (name is None):
            raise exceptions.ValidationError("project_id and name are required")
        
        project = models.Project.objects.filter(id=prj_id)
        
        if not project.exists():
            raise exceptions.ValidationError("project with given id does not exist")
        project = project.first()
        team = models.Team.objects.create(name=name,project=project)
        
        if len(users) > 0:
            users = authentication.User.objects.filter(id__in=users)
            team.users.add(*users)

        team.save()
        serializer = serializers.TeamViewSerializer(instance=team)
        return Response(serializer.data, status=201)
    
    def get(self, request, id=None, action=''):
        user = self.get_user_obj(request)
        if not id is None:
            query = models.Team.objects.filter(id=id, users__id=user.id)
            if not query.exists():
                raise exceptions.ValidationError({"error":"No such Team (that you are member) with given id."})
            
            query = query.first()
            serializer = serializers.TeamViewSerializer(instance=query)
            return Response(serializer.data, status=200)

        query = models.Team.objects.filter(users__id=user.id)
        serializer = serializers.TeamViewSerializer(query, many=True)
        return Response(serializer.data, status=200)
    
    def put(self, request , id=None, action=""):
        
        user = self.get_user_obj(request)
        if id is None:
            raise exceptions.NotFound("Endpoint not found ", 404)
            
        query = models.Team.objects.filter(id=id, users__id=user.id)
        if not query.exists():
            raise exceptions.ValidationError({"error":"No such Team (that you are member) with given id."})
    
        team = query.first()
        new_user_id = request.data.get('user_id') or None

        if new_user_id is None:
            raise exceptions.ValidationError("invalid user id")
        new_user = authentication.User.objects.filter(id=new_user_id)

        print(new_user, new_user_id, authentication.User.objects.all().values('id'),"-------")
        if not new_user.exists():
            raise exceptions.ValidationError("user not exists")
        if action=='add': 
            team.users.add(new_user.first())
            team.save()
        
            serializer = serializers.TeamViewSerializer(instance=team)
            return Response(serializer.data, status=202)
            
        
        elif(action=='remove'):
            if new_user.exists():
                team.users.remove(new_user.first())
            team.save()
                
            serializer = serializers.TeamViewSerializer(instance=team)
            return Response(serializer.data, status=202)
        else:
            raise exceptions.NotFound("Endpoint not found ", 404)

class Task(APIView):

    permission_classes = [IsAuthenticated]
    def post(self, request, id=None):

        user = request.user
        role = user.role.id
        if role!=1:
            raise exceptions.ValidationError("You do not have access to create task")
        
        data = request.data
        req_data = {
            'assigned_to' : request.data.get('assigned_to') or None,
            'created_by' : user.id,
            'project_id' : request.data.get('project_id') or None 
        }
        print(req_data)

        for key in req_data:
            if req_data[key] is None:
                raise exceptions.ValidationError(f"{key} is required to complete this request")
        serializer = serializers.TaskViewSerializer(data=data)
        if serializer.is_valid(raise_exception=True):
            serializer.create(serializer.data, req_data)
        return Response(serializer.data, status=201)
    
    def get(self, request, id=None):
        user = request.user
        query = models.Task.objects.all()
        if id is None:
            created_by_self = query.filter(created_by=user.id)
            assigned_to_self = query.filter(assigned_to=user.id)

            created_by_self = serializers.TaskViewSerializer(created_by_self, many=True)
            assigned_to_self = serializers.TaskViewSerializer(assigned_to_self, many=True)
            
            res = Response({
                'assigned_to_me' : assigned_to_self.data,
                'created_by_me' : created_by_self.data
            })
            return res
        
        tasks = query.filter(id=id)
        if not tasks.exists():
            raise exceptions.PermissionDenied("No such task exist")

        if (tasks.first().created_by.id==user.id) or (tasks.first().assigned_to.id==user.id):
            serializer = serializers.TaskViewSerializer(instance=tasks, many=True)
            # if serializer.is_valid(raise_exception=True):
            return Response(serializer.data, 200)
        raise exceptions.PermissionDenied("You do not have access here!")

    def put(self, request, id=None):
        user = request.user
        data = request.data
        

        if id is None:
            raise exceptions.NotFound("Endpoint Not Found")
        
        data = request.data
        tasks = models.Task.objects.filter(id=id).filter(Q(created_by=user) | Q(assigned_to=user))


        if not tasks.exists():
            raise exceptions.PermissionDenied("No such task exist")

        # if (tasks.first().created_by.id==user.id) or (tasks.first().assigned_to.id==user.id):
        tasks.update(**request.data)
        print(tasks, "-----------")

        serializer = serializers.TaskViewSerializer(tasks, many=True)
        # if serializer.is_valid(raise_exception=True):
        return Response(serializer.data, 200)
