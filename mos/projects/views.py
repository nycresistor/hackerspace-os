from django.http import HttpResponse
from django.template import RequestContext
from django.shortcuts import render_to_response
from mos.projects.models import Project
from django.db.backends.util import typecast_date
from django.db.backends.util import typecast_time
from django.contrib.auth.decorators import login_required

from forms import ProjectForm
import datetime

@login_required
def update_project(request, new, object_id=None):
    if not request.POST or not request.user.is_authenticated():
        return


    if not new:
        project_form = ProjectForm(request.POST,instance = Project.all.get(id=object_id))
    else:
        project_form = ProjectForm(request.POST)
 
    if project_form.is_valid():
        project = project_form.save(commit=False)
        
        if new:
            project.created_by = request.user 
    
    else :  #display error messages,if "name" field is empty no 
            #information where the error occured will be displayed!
        print project_form.errors
        return _get_latest(request,errors=project_form.errors,e_project_name=request.POST['name'])

    

    project.save()

    return _get_latest(request)


@login_required
def delete_project(request, object_id=None):
    if not request.POST or not object_id or not request.user.is_authenticated():
        return

    project = Project.all.get(id=object_id)

    #project.delete()
    project.deleted = True
    project.save()

    return _get_latest(request)

def _get_latest(request, current_project=None,errors=None,e_project_name=None):
    latest = Project.all.order_by('-created_at')[:5]
    return render_to_response('projects/overview.inc', 
                { 'project': current_project,
                  'latestprojects': latest,
                  'errors':errors,
                  'e_project_name' : e_project_name,
                }, context_instance=RequestContext(request)
        )
