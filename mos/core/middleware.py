"""
   django_playground.core.middleware
   inspired by : http://www.djangosnippets.org/snippets/799/

"""

import time

from django.db import connection
from django.utils.encoding import force_unicode

def human_readable_secs(time):
    """ converts (milli-)seconds into a nice string """

    msecs = ( time % 1 ) #get a value like this : 0.DIGITS AFTER POINT (ecample : 20.1 % 1 = 0.1
    msecs = int (msecs * 1000) # shift comma 3 digits leftside and remove part after the point


    if time > 1 :
    	secs = int (time / 1) # get seconds (example : time = 20.1 s -> 20.1 / 1 =~ 20.1 -> int (20.1) = 20 s
   	return '%(secs)d.%(msecs)d s' % {'secs' : secs,
				       'msecs' : msecs}
    
    return '%(msecs)d ms' % {'msecs' : msecs }

TAG = '<!-- footer_stats -->'
FOOTER_STAT_STRING = 'renderd in %(time)s - %(queries)s sql queries'

class SetFooter:
    """ 
    Sets some performance data (number of queries,...
    """
    
    def process_request(self, request):
        self.time_started = time.time()
	self.old_queries = len(connection.queries)

    def process_response(self, request, response):
        

	if 'text/html' not in response['Content-Type']:
            return response
        if request.is_ajax():
            return response
        if response.status_code != 200:
            return response
        
        
        queries = len(connection.queries) - self.old_queries

	stats = FOOTER_STAT_STRING % {'time' : human_readable_secs(time.time() - self.time_started),
								  'queries' : queries
								 }
        content = response.content
        response.content = force_unicode(content).replace(TAG, stats)
        
        return response

