<div id="calendar-content">

    <ul>
	{% for event in latestevents %}
		<li>{% include "cal/eventinfo.inc" %}</li>
	{% endfor %}
    </ul>

	{% with 1 as new %}
        {% with None as event %}
            {% include "cal/eventinfo.inc" %}
        {% endwith %}
	{% endwith %}
	{% if not all_events %} <p style="text-align: right"><a href="/cal/{% if location %}special/Location/{{location.name}}{% else %}{% if category %}special/Category/{{category.name}}{% endif %}{% endif %}">more...</a></p> {% endif %}
</div>
