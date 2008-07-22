
<div id="calendarcontainer{{event_form.instance.id|default_if_none:""}}">


<p class="event {% ifequal event_error_id event_form.instance.id %}invisible{% endifequal%}  {% if event.past %}past_event{% else %}event{% endif %}" id="calendar-view-{{event_form.instance.id|default_if_none:""}}">
    {% if not new %}
       <span class="event_date">{{ event.startDate|date:"D d.m.Y H:i" }} {% if event.endDate %} - {% if event.start_end_date_eq %} {{ event.endDate|date:"H:i" }} {% else %} {{ event.endDate|date:"D d.m.Y H:i" }} {% endif %} {% endif %}</span>       
      		{% if event.wikiPage %}<a href="/wiki/{{event.wikiPage}}"> {% endif %}{{ event.name }}{% if event.wikiPage %}</a>{% endif %}
		{% if event.teaser %}<span class="teaser">{{ event.teaser }}</span>{% endif %}
		{% if event.category %}<span class="category"> | <a href="/calendar/special/Category/{{ event.category }}/">{{ event.category }}</a></span>{% endif %}
		{% if event.location%}<span class="location"> | <a href="/calendar/special/Location/{{ event.location }}/">{{ event.location }}</a></span>{% endif %}

 {% endif %}
	{% if user.is_authenticated %}
        <a href='#' class="{%if not new %}hoverHidden{%endif%}" onclick="toggleView('calendar', '{% if not new %}{{event_form.instance.id|default_if_none:""}}{% endif %}', 1); return false;">{%if not new %}Edit{%else%}Create New Event{%endif%}</a>{% endif %}
	</p>
	{% if user.is_authenticated %}

    <div class="{% ifnotequal event_error_id event_form.instance.id %} invisible {% endifnotequal %} edit" id='calendar-edit-{% if not new %}{{event_form.instance.id|default_if_none:""}}{% endif %}'>
		<form id='calendar-form-{{event_form.instance.id|default_if_none:""}}' method="post" action="/calendar/{% if new %}new{%else%}{{event_form.instance.id|default_if_none:""}}/update{%endif%}/" onsubmit="return false;" onKeyPress="if(enter_pressed(event)){ submit_form($('calendar-form-{{event_form.instance.id|default_if_none:""}}'), $('eventcontainer{{event_form.instance.id|default_if_none:""}}')); }">
            <dl>

			<dt><label><b>Event Name</b>:* - Teaser:</label></dt>
			{% if event_form.name.errors %}
			   <dt> {{ event_form.name.errors }} </dt>
			{% endif %}
			<dd>
			  {{ event_form.name }} - <br/>
			  {{ event_form.teaser }}
            </dd>

			<dt><label><b>Wiki Page</b>:*</label></dt>
			{% if event_form.wikiPage.errors %}
			   <dt> {{ event_form.wikiPage.errors }} </dt>
			{% endif %}
			 <dd>  {{ event_form.wikiPage }} </dd>
		
			<dt><label><b>Start</b>:*</label></dt>
			{% if event_form.startDate.errors %}
			   <dt> {{ event_form.startDate.errors }} </dt>
			{% endif %}
			<dd> {{ event_form.startDate }} </dd>

			<dt><label>End:</label></dt>

            {% if event_form.endDate.errors %}
                <dt> {{ event_form.endDate.errors }} </dt>
	    {% endif %}
		 <dd> {{ event_form.endDate }}</dd>

            {% if event_form.category.errors %}
                <dt> {{ event_errors.category }} </dt>
	    {% endif %}
		<dd> {{ event_form.category }}</dd>

            {% if event_form.location.errors %}
                <dt> {{ event_form.location.errors }} </dt>
	    {% endif %}
 	    	<dd> {{ event_form.location }}</dd>

	    <dd> (*) -> required field </dd>
            <dt style="visibility: hidden">Submit:</dt>
            <dd style="text-align: right;">
			{% if not new %}

				<input type="button" value="Update" onclick="submit_form('calendar', '{{event_form.instance.id|default_if_none:""}}');">
				<input type="button" value="Delete" onclick="delete_entry('calendar','{{event_form.instance.id|default_if_none:""}}');"> 
			
            {% else %}
				<input type="button" value="Create" onclick="submit_form('calendar', '{{event_form.instance.id|default_if_none:""}}');">
            {% endif %}

			<a href="#" class="toggled" onclick="toggleView('calendar', '{% if not new %}{{event_form.instance.id|default_if_none:""}}{% endif %}', 0); return false;">Cancel</a>
            </dd>
            </dl>
		</form>
	</div>
	{% endif %}
</div>
