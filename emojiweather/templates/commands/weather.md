{% spaceless %}

{% if location and forecast %}
#### Weather

**{{ location }}** for **Week of {% now 'F jS, Y' %}**

| Date                          |                | Conditions           | High            | Low            |
|:------------------------------|:---------------|:---------------------|----------------:|---------------:|{% for day in forecast %}
| {{ day.date|date:'l, M. j' }} | {{ day.icon }} | {{ day.conditions }} | {{ day.high }}° | {{ day.low }}° |{% endfor %}
{% endif %}

{% if alerts %}
##### Alerts :rotating_light:
{% for alert in alerts %}
- [{{ alert.title }}]({{ alert.uri }}) ({{ alert.time|date:'n/j P' }}–{{ alert.expires|date:'n/j P' }}): {{ alert.description|lower|capfirst|truncatechars:75 }}
{% endfor %}
{% endif %}

{% endspaceless %}