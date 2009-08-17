import json

from django.core.urlresolvers import reverse
from django.http import HttpResponse
from django.shortcuts import get_object_or_404
from django.shortcuts import render_to_response
from django.contrib.sites.models import Site

from django.views.generic.list_detail import object_detail, object_list
from django.views.generic.create_update import create_object, update_object

from factory.forms import BuildForm
from factory.models import Build, FabfileRecipe


def build_list_queryset(request, queryset, extra_context):
    """
    Create a new build    
    """
    return object_list(request, queryset=queryset,
                       template_name='factory/build_list.html',
                       context_processors=None,
                       extra_context=extra_context)
    
build_lists = {
    'all': lambda x : build_list_queryset(x, queryset=Build.objects.all(),
                                          extra_context={'list_name':'All builds'}),
    'success': lambda x : build_list_queryset(x, queryset=Build.objects.filter(success=True),
                                          extra_context={'list_name':'Successful builds'}),
    'no_success': lambda x : build_list_queryset(x, queryset=Build.objects.filter(success=False),
                                          extra_context={'list_name':'Not Successful builds'}),
    'executed': lambda x : build_list_queryset(x, queryset=Build.objects.filter(executed=True),
                                          extra_context={'list_name':'Excuted builds'}),
    'not_executed': lambda x : build_list_queryset(x, queryset=Build.objects.filter(executed=False),
                                          extra_context={'list_name':'Not yet executed builds'}),
}

def build_detail(request, object_id):
    """
    Display information related to the build which has
    id == object_id
    """
    return object_detail(request, queryset=Build.objects.all(),
                         object_id=object_id,
                         template_name='factory/build_detail.html',
                         context_processors=None)

def build_update(request, object_id):
    """
    Update information related to the build which has
    id == object_id    
    """
    return update_object(request, model=Build, object_id=object_id,
                form_class = BuildForm,
                template_name='factory/build_form.html',
                post_save_redirect=reverse("build_list_all"))

def build_create(request):
    """
    Create a new build    
    """
    return create_object(request, model=Build,
                  template_name='factory/build_form.html',
                  post_save_redirect=reverse("build_list_all"))
    
def build_oldest_not_executed(self):
    """
    Display information related to the oldest build not executed
    """
    qs = Build.objects.filter(executed=False).order_by("id")
    site = Site.objects.get_current()
    if qs.count() > 0:
        oldest_build_not_executed = qs[0]
        d={"name":oldest_build_not_executed.name,
           'task':oldest_build_not_executed.task,
           "post_back_url":"http://%s%s" %(site.domain,reverse("build_update",
                               kwargs={'object_id':oldest_build_not_executed.id})),
           "build_package_url":"http://%s%s" %(site.domain,
                                               oldest_build_not_executed.get_build_package_url())
        }
        json_string = json.dumps(d)
    else:
        json_string = json.dumps(False)
    return HttpResponse(json_string)