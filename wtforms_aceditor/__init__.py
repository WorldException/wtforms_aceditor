# -*-coding:utf8-*-
"""
Usage:

from wtforms_aceditor import AceEditor

class WorkFlowView(ModelView):
    # two variants 1
    form_extra_fields = {
        'config_yaml': TextAreaField('config_yaml', widget=AceEditor('yaml'))
    }
    # or 2
    form_args = {
        'config_yaml': {
            'widget': AceEditor('yaml')
        }
    }
"""
from html import escape
from wtforms.compat import text_type
from wtforms.widgets import html_params
from markupsafe import Markup
import os


TEMPLATE = u"""
    <div id="div_%(id)s">
    </div>
    <textarea id="%(id)s" name="%(id)s" hidden style="display: none">%(value)s</textarea>
"""

TEMPLATE_SCRIPT="""
    <script src="%(script_url)s" type="text/javascript" charset="utf-8"></script>
    <link rel="stylesheet" href="%(css_url)s">
"""

TEMPLATE_INIT="""
<script async="false">
(function(){
    let editor = ace.edit("div_%(id)s");
    editor.setOptions({
        %(options)s
    });
    let data_input = document.getElementById("%(id)s");
    editor.session.setValue(data_input.value);
    editor.session.on('change', function(data){
        data_input.value = editor.getSession().getValue();
    })
})();
</script>
"""

# https://github.com/ajaxorg/ace-builds.git
#ACE_SCRIPT_PATH = os.path.join(os.path.dirname(__file__), 'static', 'src-min')
#ACE_STATIC_URL = '/aceditor/static'


class AceEditor(object):
    
    default_options = dict(
        tabSize=2,
        theme='ace/theme/tomorrow_night_eighties',
        wrap=True,
        maxLines=200,
        autoScrollEditorIntoView=True
    )

    script_url_default = 'https://cdn.jsdelivr.net/npm/ace-builds@1.29.0/src-min-noconflict/ace.min.js'
    css_url_default = "https://cdn.jsdelivr.net/npm/ace-builds@1.29.0/css/ace.min.css"

    def __init__(self, lang='yaml', script_url='', css_url='', **options):
        """
        :param lang syntax scheme
        :param script_url ace.js location
        :param **options options aceditor
        """
        self.script_url = script_url if script_url else AceEditor.script_url_default        
        self.css_url = css_url if css_url else AceEditor.css_url_default

        self.lang = lang

        self.options = AceEditor.default_options.copy()
        self.options.update(options)
        self.options['mode'] = f'ace/mode/{lang}'
        self.options_str = self._make_options_str(self.options)

        self.template = TEMPLATE + TEMPLATE_SCRIPT + TEMPLATE_INIT

    def _make_options_str(self, options):
        if options:
            opts = []
            for k, v in options.items():
                if type(v) is str:
                    opts.append('{}: "{}"'.format(k, v))
                elif type(v) is bool:
                    opts.append('{}: {{}}'.format(k, str(v).lower()))
                else:
                    opts.append('{}: {}'.format(k, v))
            if opts:
                return ",\n".join(opts) + ","
        return ""

    def __call__(self, field, **kwargs):

        kwargs.setdefault('id', field.id)

        return Markup(self.template % dict(
            params=html_params(name=field.name, **kwargs),
            value=escape(text_type(field._value()), quote=False),
            id=kwargs.get('id'),
            script_url=self.script_url,
            css_url=self.css_url,
            lang=self.lang,
            options=self.options_str,
            theme=self.options['theme']
        ))

