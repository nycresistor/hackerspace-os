from django import template
from django.core.urlresolvers import get_mod_func
import mos.cal.forms

register = template.Library()

@register.tag
def print_form(parser,token):
    try:
        tagname, varname, formclass = token.split_contents()
        return FormNode(varname, formclass)
    except ValueError:
        raise template.TemplateSyntaxError, "%r tag requires arguments" % token.contents.split()[0]

class FormNode(template.Node):
    def __init__(self, varname, formclass):
        self.varname = template.Variable(varname)
        self.formclass = formclass

    def render(self, context):
        try:
            variable = self.varname.resolve(context)
        except template.VariableDoesNotExist:
            return 'variable does not exist here!'
        try:
            mod_name, classname = get_mod_func(self.formclass)
            formclass = getattr(__import__(mod_name, {}, {}, ['']), classname)
        except (ImportError, AttributeError):
            raise

        if variable:
            f = formclass(instance=variable)
        else:
            f = formclass()
        return f.as_p()
