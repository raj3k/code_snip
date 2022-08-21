from django.template import Library, Node
from django.template.defaultfilters import stringfilter
from django.utils.safestring import mark_safe

from pygments import highlight
from pygments.formatters.html import HtmlFormatter
from pygments.lexers import get_lexer_by_name

register = Library()


class PygmentsCss(Node):
    def __init__(self, css_class=".highlight"):
        self.css_class = css_class

    def render(self, context):
        html_formatter = HtmlFormatter()
        styles = html_formatter.get_style_defs(self.css_class)
        return mark_safe(styles)


@register.tag
def pygments_css(parser, token):
    return PygmentsCss()


@register.filter
@stringfilter
def pygmentize(value, args):
    args = args.split(",")
    lexer_name = args[0]
    style = args[1]
    linenos = args[2]
    formatter = HtmlFormatter(style=style, linenos=linenos == "True")
    try:
        lexer = get_lexer_by_name(lexer_name)
    except ValueError:
        lexer = get_lexer_by_name('text')
    parsed = highlight(value, lexer, formatter)
    return mark_safe(parsed)

