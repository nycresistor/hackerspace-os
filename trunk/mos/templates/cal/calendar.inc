

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
	<p style="text-align: right"><a href="/cal">more...</a></p>
</div>
