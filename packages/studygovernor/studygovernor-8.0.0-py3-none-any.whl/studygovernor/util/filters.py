import sys
import json
import inspect

import yaml
from markupsafe import Markup
from pygments import highlight
from pygments.lexers import YamlLexer, JsonLexer, PythonLexer
from pygments.formatters import HtmlFormatter



def register_filters(app):
    """ Special function that registers all member of this module ending in "_filter". """
    # Get the list of methods and excluded this very function.
    filters = [(name, obj) for name, obj in inspect.getmembers(sys.modules[__name__]) if inspect.isfunction(obj) and name.endswith("_filter")]
    # Loop over the found filter functions and register them in the app object as jinja filters.
    for filter_name, filter_obj in filters:
        filter_name = filter_name.replace("_filter", "")
        app.jinja_env.filters[filter_name] = filter_obj


def json_format_filter(s):
    """ Filter for pretty formatting json's. """
    try:
        s = json.dumps(json.loads(s), indent=2)
    except (ValueError, TypeError):
        s = str(s)

    return Markup(highlight(s, JsonLexer(), HtmlFormatter()))


def yaml_dump_filter(s):
    """ Filter for pretty formatting json's. """
    if not isinstance(s, str):
        try:
            s = yaml.safe_dump(s)
        except (ValueError, TypeError):
            s = str(s)

    return Markup(highlight(s, YamlLexer(), HtmlFormatter()))


def python_code_filter(s):
    if not isinstance(s, str):
        s = str(s)
    return Markup(highlight(s, PythonLexer(), HtmlFormatter()))



def hyphenate_filter(s):
    """ Filter for lowercasing and hyphenating a string. """
    try:
        return s.lower().strip().replace(" ", "-")
    except ValueError:
        return s