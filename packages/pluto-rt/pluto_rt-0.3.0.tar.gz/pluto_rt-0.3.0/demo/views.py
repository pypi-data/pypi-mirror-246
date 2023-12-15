import random

from django.http import HttpResponse
from django.template import engines

from .tasks import sample_ops_function

TEMPLATE_STR = """
<html>
  <head>
    <title>Pluto RT Demo</title>
  </head>
  <body>
    <h1>Pluto RT Demo</h1>
    <div>
      {% include "pluto_rt/table_partial.html" %}
    </div>
  <script src="https://unpkg.com/htmx.org@1.9.9" integrity="sha384-QFjmbokDn2DjBjq+fM+8LUIVrAgqcNW2s0PjAxHETgRn9l4fvX31ZxDxvwQnyMOX" crossorigin="anonymous"></script>
  </body>
</html>
"""

def run_demo(request):
    """
    Real-time results display of demo report run
    """
    queue_name = f"testqueue_{random.randint(1000,9999)}"

    # kick off the long running task
    sample_ops_function.delay(queue_name)

    ctx = {
        "queue_name": queue_name,
        "num_per_gulp": 100,
        "interval_seconds": 3,
    }
    if request.GET.get("reverse"):
        ctx["reverse"] = True

    django_engine = engines["django"]
    template = django_engine.from_string(TEMPLATE_STR)
    return HttpResponse(template.render(ctx, request))
