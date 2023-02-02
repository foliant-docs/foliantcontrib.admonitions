'''Preprocessor for admonitions'''

import re

from foliant.preprocessors.utils.preprocessor_ext import BasePreprocessorExt
from foliant.preprocessors.utils.preprocessor_ext import allow_fail


def pandoc(form: str,
           type_: str,
           title: str,
           lines: list):
    template = "{body}\n\n"
    header = title if title is not None else type_
    if header:
        template = '> **{header}**\n>\n' + template
    body = '\n'.join(['> ' + ln for ln in lines])
    return template.format(header=header, body=body)


def slate(form: str,
          type_: str,
          title: str,
          lines: list):
    type_to_class = {'error': 'warning',
                     'danger': 'warning',
                     'caution': 'warning',
                     'info': 'notice',
                     'note': 'notice',
                     'tip': 'notice',
                     'hint': 'notice', }
    template = '<aside class="{class_}">{body}</aside>\n\n'
    class_ = type_to_class.get(type_, type_)
    body = '\n'.join(lines)
    return template.format(class_=class_, body=body)


def hugo(form: str,
         type_: str,
         title: str,
         lines: list):
    type_to_form = {'!!!': 'standard',
                    '???': 'collapse',
                    '???+': 'collapse_plus'}
    form = type_to_form.get(form, form)
    template = '{pref} admonition form="{form}" type="{type_}" title="{title}" {suf}{body}\n\n{pref} /admonition {suf}\n\n'
    body = '\n'.join(lines)
    pref = '{{%'
    suf = '%}}'
    return template.format(form=form, type_=type_, title=title, body=body, pref=pref, suf=suf)


class Preprocessor(BasePreprocessorExt):
    backend_processors = {
        'pandoc': pandoc,
        'slate': slate,
        'hugo': hugo,
    }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.logger = self.logger.getChild('admonitions')

        self.logger.debug(f'Preprocessor inited: {self.__dict__}')
        self.pattern = re.compile(r'(?P<form>(\!{3})|(\?{3})|(\?{3}\+))\s(?P<type>\w+)(?: +"(?P<title>.*)")?\n(?P<content>(?:(?:    |\t).*\n|\n)+)')

    @allow_fail('Failed to process admonition. Skipping.')
    def _process_admonition(self, block):
        self.logger.debug(f'Found admonition: \n\n{block.group(0)}')
        form = block.group('form')
        type_ = block.group('type').lower()
        title = block.group('title')
        lines = []

        for ln in block.group('content').split('\n'):
            if not ln:
                # break
                lines.append('')
            if ln.startswith('    '):
                lines.append(ln[4:])
            else:  # starts with tab
                lines.append(ln[1:])

        # lines._process_admonition()

        while lines[-1] == '':  # remove empty lines at the end
            lines.pop()

        processor = self.backend_processors[self.context['backend']]
        return processor(form, type_, title, lines)

        self.context['target']

    def apply(self):
        if self.context['backend'] in self.backend_processors:
            self._process_tags_for_all_files(self._process_admonition)

        self.logger.info(f'Preprocessor applied')
