<div id='eventcontainer{{event.id}}'>
    <p class="event visible {% if event.past %}past_event{% else %}event{% endif %}" id='calendar-view-{{event.id}}'>
    {% if not new %} 
       <span class="event_date">{{ event.startDate|date:"D d.m.Y H:i" }} {% if event.endDate %} - {% if event.start_end_date_eq %} {{ event.endDate|date:"H:i" }} {% else %} {{ event.endDate|date:"D d.m.Y H:i" }} {% endif %} {% endif %} </span>      
      		{% if event.wikiPage %}<a href="/wiki/{{event.wikiPage}}"> {% endif %}{{ event.name }}{% if event.wikiPage %}</a>{% endif %}
		{% if event.teaser %}<span class="teaser">{{ event.teaser }}</span>{% endif %}
    {% endif %}
	{% if user.is_authenticated %}
        <a href='#' class="{%if not new %}hoverHidden{%endif%}" onclick="toggleView('calendar', '{% if not new %}{{event.id}}{% endif %}', 1); return false;">{%if not new %}Edit{%else%}Create New Event{%endif%}</a>{% endif %}
	</p>
	{% if user.is_authenticated %}
    <div class="invisible  edit" id='calendar-edit-{{event.id}}'>
		<form id='calendar-form-{{event.id}}' method="post" action="/cal/{% if new %}new{%else%}{{event.id}}/update{%endif%}/" onsubmit="return false;" onKeyPress="if(enter_pressed(event)){ 
			myform = $('calendar-form-{{event.id}}');
			new Ajax.Updater( $('eventcontainer{{event.id}}'), myform.readAttribute('action'), {
			  parameters: myform.serialize(true),
			});
			 }">
            <dl>

			<dt><label><b>Event Name</b>:* - Teaser:</label></dt>
			<dd>
			<input name='name' id="event-name-{{event.id}}" type="text" value='{{ event.name }}'/>
			<input name='teaser' id="event-teaser-{{event.id}}" type="text" value='{{ event.teaser }}'/>
            		</dd>

			<dt><label><b>Wiki Page</b>:*</label></dt>
			<dd><input name='wikiPage' id="event-wikiPage-{{event.id}}" type="text" value='{{ event.wikiPage }}'/></dd>
		
			<dt><label><b>Start</b>:*</label></dt>
			<dd><input name='startDate_0' class='vDateField' id="event-startDate-{{event.id}}" type='text' value='{{ event.startDate.date }}' />
			<input name='startDate_1' class='vTimeField' id="event-startTime-{{event.id}}" type='text' value='{{ event.startDate.time }}' />
            </dd>

			<dt><label>End:</label></dt>
			<dd><input name='endDate_0' class='vDateField' id="event-endDate-{{event.id}}" type='text' value='{{ event.endDate.date }}' />
			<input name='endDate_1' class='vTimeField' id="event-endTime-{{event.id}}" type='text' value='{{ event.endDate.time }}' />
            </dd>
	    <dd> (*) -> required field </dd>
            <dt style="visibility: hidden">Submit:</dt>
            <dd style="text-align: right;">
			{% if not new %}
				<input type="button" value="Update" onclick="myform = $('calendar-form-{{event.id}}');
				new Ajax.Updater( $('eventcontainer{{event.id}}'), myform.readAttribute('action'), {
				  parameters: myform.serialize(true),
				});
				"/>	
				<input type="button" value="Delete" onclick="myform = $('calendar-form-{{event.id}}');
				new Ajax.Updater( $('calendar-content'), '/cal/{{event.id}}/delete/', {
				  parameters: myform.serialize(true),
				});
				"/>
			{% else %}
				<input type="button" value="Create" onclick="myform = $('calendar-form-{{event.id}}');
				new Ajax.Updater( $('eventcontainer{{event.id}}'), myform.readAttribute('action'), {
				  parameters: myform.serialize(true),
				});
				"/>
			{% endif %}

			<a href="#" class="toggled" onclick="toggleView('calendar', '{{event.id}}', 0); return false;">Cancel</a>
            </dd>
            </dl>
		</form>
	</div>
	{% endif %}
</div>
