from django import template
from django.template import Template

register = template.Library()


@register.simple_tag(takes_context=True)
def course_box(context, count):
    output = ""
    iters = int(int(count) / 6)

    for i in range(iters):
        output += "<div class=\"box grey-text\">Course:</div>"

    return Template(output).render(context)
