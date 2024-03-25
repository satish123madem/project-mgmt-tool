from django.db import models

from Authentication import models as Authentication



class Status(models.Model):
    name = models.CharField(max_length=50, unique=True)


class Project(models.Model):

    name = models.CharField(max_length=100)
    description = models.TextField()
    created_by = models.ForeignKey(Authentication.User, on_delete=models.DO_NOTHING)
    created_on = models.DateTimeField(auto_now=True)
    last_modified = models.DateTimeField(null=True)
    start_date = models.DateTimeField(null=False)
    end_date = models.DateTimeField(null=False)
    status = models.ForeignKey(Status, on_delete=models.DO_NOTHING)
    is_deleted = models.BooleanField(default=False)


class Team(models.Model):
    name = models.CharField(max_length=50)
    users = models.ManyToManyField(Authentication.User)
    project = models.ForeignKey(Project, on_delete=models.DO_NOTHING, null=True)


PRIORITY_CHOICES = [ \
                        (1, "HIGH"), \
                        (2, "MEDIUM"),\
                        (3, "LOW") \
                   ]


class Task(models.Model):

    name = models.CharField(max_length=100)
    description = models.TextField()
    project = models.ForeignKey(Project, on_delete=models.DO_NOTHING, null=False)
    created_by = models.ForeignKey(Authentication.User, on_delete=models.DO_NOTHING, related_name="created_by")
    assigned_to = models.ForeignKey(Authentication.User, on_delete=models.DO_NOTHING, related_name="assigned_to")
    created_date = models.DateTimeField(auto_now=True)
    due_date = models.DateField()
    status = models.ForeignKey(Status, on_delete=models.DO_NOTHING)
    priority = models.IntegerField(choices=PRIORITY_CHOICES, default=2)

    
    