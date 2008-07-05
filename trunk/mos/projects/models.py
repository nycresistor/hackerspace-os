from django.db import models
import datetime
from django.contrib.auth.models import User

# Create your models here.

class ProjectManager(models.Manager):
    def get_query_set(self):
        return super(ProjectManager, self).get_query_set().filter(deleted=False)

class Project(models.Model):
    name = models.CharField(max_length=200)
    teaser = models.TextField(max_length=200, blank=True, null=True)
    wikiPage = models.CharField(max_length=200,blank=True,null=True)

    created_at = models.DateTimeField(default=datetime.datetime.now)
    created_by = models.ForeignKey(User)

    finished_at = models.DateField(blank=True,null=True)

    deleted = models.BooleanField(default=False)

    objects = models.Manager()
    all = ProjectManager()

    def __str__(self):
    	return '%s' % (self.name)

    class Admin:
    	pass
