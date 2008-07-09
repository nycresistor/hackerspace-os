
<div id="eventcontainer{{event_form.instance.id|default_if_none:""}}">
<p class="event {% ifequal event_error_id event_form.instance.id %}invisible{% endifequal%}  {% if event.past %}past_event{% else %}event{% endif %}" id="calendar-view-{{event_form.instance.id|default_if_none:""}}">
    {% if not new %}
       <span class="event_date">{{ event.startDate|date:"D d.m.Y H:i" }} {% if event.endDate %} - {% if event.start_end_date_eq %} {{ event.endDate|date:"H:i" }} {% else %} {{ event.endDate|date:"D d.m.Y H:i" }} {% endif %} {% endif %}</span>       
		{% if event.wikiPage %}<a href="/wiki/{{event.wikiPage}}"> {% endif %}{{ event.name }}{% if event.wikiPage %}</a>{% endif %}
		{% if event.teaser %}<span class="teaser">{{ event.teaser }}</span>{% endif %}
    {% endif %}
	{% if user.is_authenticated %}
        <a href='#' class="{%if not new %}hoverHidden{%endif%}" onclick="toggleView('calendar', '{% if not new %}{{event_form.instance.id|default_if_none:""}}{% endif %}', 1); return false;">{%if not new %}Edit{%else%}Create New Event{%endif%}</a>{% endif %}
	</p>
	{% if user.is_authenticated %}

    <div class="{% ifnotequal event_error_id event_form.instance.id %} invisible {% endifnotequal %} edit" id='calendar-edit-{% if not new %}{{event_form.instance.id|default_if_none:""}}{% endif %}'>
		<form id='calendar-form-{{event_form.instance.id|default_if_none:""}}' method="post" action="/cal/{% if new %}new{%else%}{{event_form.instance.id|default_if_none:""}}/update{%endif%}/" onsubmit="return false;" onKeyPress="if(enter_pressed(event)){ 
			myform = $('calendar-form-{{event_form.instance.id|default_if_none:""}}');
                    new Ajax.Updater( $('eventcontainer{{event_form.instance.id|default_if_none:""}}'), myform.readAttribute('action'), {
                    parameters: myform.serialize(true),
            });
			 }">
            <dl>

			<dt><label><b>Event Name</b>:* - Teaser:</label></dt>
			{% if event_errors.name %}
			   <dt> {{ event_errors.name }} </dt>
			{% endif %}
			<dd>
			  {{ event_form.name }} - <br/>
			  {{ event_form.teaser }}
            </dd>

			<dt><label><b>Wiki Page</b>:*</label></dt>
			{% if event_errors.wikiPage %}
			   <dt> {{ event_errors.wikiPage }} </dt>
			{% endif %}
			 <dd>  {{ event_form.wikiPage }} </dd>
		
			<dt><label><b>Start</b>:*</label></dt>
			{% if event_errors.startDate %}
			   <dt> {{ event_errors.startDate }} </dt>
			{% endif %}
			<dd> {{ event_form.startDate }} </dd>

			<dt><label>End:</label></dt>

            {% if event_errors.endDate %}
                <dt> {{ event_errors.endDate }} </dt>
			{% endif %}
			<dd> {{ event_form.endDate }}</dd>

            {% if event_errors.category %}
                <dt> {{ event_errors.category }} </dt>
			{% endif %}
			<dd> {{ event_form.category }}</dd>

            {% if event_errors.location %}
                <dt> {{ event_errors.location }} </dt>
			{% endif %}
			<dd> {{ event_form.location }}</dd>

	    <dd> (*) -> required field </dd>
            <dt style="visibility: hidden">Submit:</dt>
            <dd style="text-align: right;">
			{% if not new %}

				<input type="button" value="Update" onclick="myform = $('calendar-form-{{event_form.instance.id|default_if_none:""}}');
                    myform = $('calendar-form-{{event_form.instance.id|default_if_none:""}}');
                    new Ajax.Updater( $('eventcontainer{{event_form.instance.id|default_if_none:""}}'), myform.readAttribute('action'), {
                      parameters: myform.serialize(true),
                    });
				"/>	
				<input type="button" value="Delete" onclick="myform = $('calendar-form-{{event_form.instance.id|default_if_none:""}}');
                    myform = $('calendar-form-{{event_form.instance.id|default_if_none:""}}');
                    new Ajax.Updater( $('calendar-content'), '/cal/{{event_form.instance.id|default_if_none:""}}/delete/', {
                    });
				"/>
            {% else %}
				<input type="button" value="Create" onclick="myform = $('calendar-form-{{event_form.instance.id|default_if_none:""}}');
                    myform = $('calendar-form-{{event_form.instance.id|default_if_none:""}}');
                    new Ajax.Updater( $('eventcontainer{{event_form.instance.id|default_if_none:""}}'), myform.readAttribute('action'), {
                      parameters: myform.serialize(true),
                    });
				"/>
            {% endif %}

			<a href="#" class="toggled" onclick="toggleView('calendar', '{{event_form.instance.id|default_if_none:""}}', 0); return false;">Cancel</a>
            </dd>
            </dl>
		</form>
	</div>
	{% endif %}
</div>
