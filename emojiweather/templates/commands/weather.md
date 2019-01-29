{% spaceless %}

{% if error %}{{ error }}{% endif %}

{% if location and forecast %}

#### Weather in {{ location }} for the Week of {% now 'F dS, Y' %}

| Date                          |                | Summary           | High            | Low            |
|:------------------------------|:---------------|:------------------|----------------:|---------------:|
{% for day in forecast %}
| {{ day.date|date:'l, M. j' }} | {{ day.icon }} | {{ day.summary }} | {{ day.high }}° | {{ day.low }}° |
{% endfor %}
---

{% endif %}

{% if alerts %}
#### Alerts
{% for alert in alerts %}
- [{{ alert.title }}]({{ alert.uri }})
{% endfor %}
{% endif %}

{% endspaceless %}