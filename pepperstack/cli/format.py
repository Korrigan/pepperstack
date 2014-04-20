"""
Formatting utils for pepperstack cli

"""

DEFAULT_INDENT = 2


def title(title, line='='):
    """
    Returns `title` underlined by `line` aligned

    """
    return '{title}\n{pad:{line}<{width}}\n'.format(title=title,
                                                    pad='',
                                                    line=line,
                                                    width=len(title))


def indent(string, indent=DEFAULT_INDENT):
    """
    Return `string` indented by `indent` spaces

    """
    sp = ' ' * indent
    spl = '\n' + sp
    return sp + spl.join(string.splitlines())


def pretty_print(obj, indent=DEFAULT_INDENT):
    """
    Returns a Yaml-like representation of `obj` indented with `indent` spaces

    """
    def _pprint(obj, cur_indent, prefix=''):
        string = ""
        if isinstance(obj, list):
            for e in obj:
                string += _pprint(e, cur_indent + indent, prefix='- ')
        elif isinstance(obj, dict):
            for k, v in obj.items():
                v_string = ""
                if isinstance(v, dict) or isinstance(v, list):
                    v_string = '\n' + _pprint(v, cur_indent + indent, prefix=indent * ' ')
                else:
                    v_string = ' ' + str(v) + '\n'
                string += '{0}{1}:{2}'.format(' ' * cur_indent, k, v_string)
        else:
            string += ' ' * (cur_indent - len(prefix)) + prefix + str(obj) + '\n'
        return string
    print _pprint(obj, 0)
    
