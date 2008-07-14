from django.conf import settings

def custom_settings_main(request):

    """ 
    sets customizations specified in settings.py for the main page
    """

    return {'introduction_text' : settings.HOS_INTRODUCTION,
    	    'members' : settings.HOS_MEMBER_GALLERY,
	    'gallery' : settings.HOS_LOCATION_GALLERY,
	    'openlab' : settings.HOS_OPENLAB,
	    'calendar' : settings.HOS_CALENDAR,
	    'projects' : settings.HOS_PROJECTS,
	    'recent_changes' : settings.HOS_RECENT_CHANGES,
	    'metasense' : settings.HOS_METASENSE
    
    }

