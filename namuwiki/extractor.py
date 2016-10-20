import re
import urllib.parse

_patterns = {
    'macro': [
        r'\[\[br\]\]',
        r'\[\[(?:date|datetime|include|tableofcontents|목차|footnote|각주|wikicommons|youtube|nicovideo|html|navigation)(?:\([^\]]*\))?\]\]',
        r'\[br\]',
        r'\[(?:date|datetime|include|tableofcontents|목차|footnote|각주|wikicommons|youtube|nicovideo|html|navigation)(?:\([^\]]*\))?\]',
    ],
    'html': [
        r'\{\{\{\#\!html[ \t\n]*([\s\S]*?)\}\}\}',
        r'\[\[html[ \t]*\(([^\)]*)\)\]\]',
    ],
    'link': [
        r'\[\[(?:https?|ftp)[^ ]+?(?:[\| ]([^\]]*))?\]\]?', # URL
        r'\[(?!\*)(?:https?|ftp)[^ ]+?(?:[\| ]([^\]]*))?\]', # URL
        r'\[\[([a-z]+\:[^\" \n]+?)(?:[\| ]([^\]]*))?\]\]', # interwiki
        r'\[(?!\*)([a-z]+\:[^\" \n]+?)(?:[\| ]([^\]]*))?\]', # interwiki
        r'\[\[([a-z]+\:\".+?(?<!\\)\")(?:[\| ]?([^\]]*))?\]\]', # interwiki
        r'\[(?!\*)([a-z]+\:\".+?(?<!\\)\")(?:[\| ]?([^\]]*))?\]', # interwiki
        r'\[\[([^\|\#\]]+?)(?:\#[^|\]]+)?(?:\|([^\]]*))?\]\]', # document
        r'\[(?!\*)([^\|\#\]]+?)(?:\#[^|\]]+)?(?:\|([^\]]*))?\]', # document
        r'[a-z]+\:(?!//)([^\" \n]+)', # interwiki
        r'[a-z]+\:(?!//)\"(.+)(?<!\\)\"', # interwiki
    ],
    'special_markup': [
        # footnote
        r'^[ \t]*\[\*[^ ]*[ \t]*([^\[\]]*)\]', # at the beginning
        r'\[\*[^ ]*[ \t]*([^\[\]]*)\][ \t]*\.?[ \t]*$', # at the end
        # deletion
        r'^[ \t]*~~(?!~)(.*?)~~', # at the beginning
        r'~~(?!~)(.*?)~~[ \t]*\.?[ \t]*$', # at the end
        r'^[ \t]*--(?!-)(.*?)--', # at the beginning
        r'--(?!-)(.*?)--[ \t]*\.?[ \t]*$', # at the end
    ],
    'markup': [
        # heading
        r'^[ \t]*={1,}[ \t]*(.*?)[ \t]*={1,}[ \t]*$',
        # bold
        r"'''(?!')(.*?)'''",
        # italic
        r"''(?!')(.*?)''",
        # deletion
        r'~~(?!~)(.*?)~~', # in a sentence
        r'--(?!-)(.*?)--', # at a sentence
        # underline
        r'__(?!_)(.*?)__',
        # superscript
        r'\^\^(?!\^)(.*?)\^\^',
        r'\^(?!\^)(.*?)\^',
        # subscript
        r',,(?!,)(.*?),,',
        # horizontal ruler
        r'-{4,10}',
        # unordered list
        r'^[ \t]*\*[ \t]*(.*?)[ \t]*$',
        # ordered list
        r'^[ \t]*1\.[ \t]*(?:\#\d+)?[ \t]*(.*?)[ \t]*$',
        r'^[ \t]*A\.[ \t]*(?:\#\d+)?[ \t]*(.*?)[ \t]*$',
        r'^[ \t]*a\.[ \t]*(?:\#\d+)?[ \t]*(.*?)[ \t]*$',
        r'^[ \t]*I\.[ \t]*(?:\#\d+)?[ \t]*(.*?)[ \t]*$',
        r'^[ \t]*i\.[ \t]*(?:\#\d+)?[ \t]*(.*?)[ \t]*$',
        # text size
        r'\{\{\{\+\d+[ \t]*(.*?)[ \t]*\}\}\}',
        # text color
        r'\{\{\{\#(?:[0-9a-f]{6}|[a-z]+)[ \t]*(.*?)[ \t]*\}\}\}',
        # image
        r'(?:https?|ftp)?.*\.(?:png|gif|jpeg|jpg)(?:\?|&(?!>amp;))?.*\b',
        # attachment
        r'attachment:[ \t]*(?:[^ ]*\.(?:png|gif|jpeg|jpg)(?:\?|&(?!>amp;))?.*\b|".*\.(?:png|gif|jpeg|jpg)(?:\?|&(?!>amp;))?.*")',
        # table
        r'\|\|(?:<[^>]*>)*([^|\n]*)',
        r'\{\{\|([\s\S]*?)\|\}\}',
        # quote
        r'\>(.*)',
        # footnote in a sentence
        r'\[\*[^ ]*[ \t]*([^\[\]]*)\]',
        # plain text
        r'\{\{\{([\s\S]*?)\}\}\}',
        # math
        r'\$.*?\$',
        # title replacement
        r'\{\{\{[ \t]*\#title[ \t]*.*?\}\}\}',
        # redirect
        r'\#redirect[ \t]*.*',
        # comment
        r'\#\#.*',
    ],
}

for name in _patterns:
    _patterns[name] = list(map(lambda pattern: re.compile(pattern, re.IGNORECASE | re.MULTILINE), _patterns[name]))

def _strip_tags(source):
    return re.sub(r'<[^<]+?>', '', source)

def _clean_macro(content):
    content = _patterns['macro'][0].sub('\n', content)
    for pattern in _patterns['macro'][1:]:
        content = pattern.sub('', content)

    return content

def _clean_html(content):
    for pattern in _patterns['html']:
        content = pattern.sub(lambda match: match.groups('')[0], content)

    return _strip_tags(content)

def _clean_link(content):
    def replacement(match):
        groups = match.groups('')
        if len(groups) < 2:
            replacement = groups[0]
        else:
            replacement = groups[1] or groups[0]

        if replacement:
            if replacement == '../':
                replacement = ''

            replacement = replacement.replace('/', ' ')

        return urllib.parse.unquote_plus(replacement)

    for pattern in _patterns['link']:
        content = pattern.sub(replacement, content)

    return content

def _clean_special_markup(content):
    for pattern in _patterns['special_markup']:
        content = pattern.sub(lambda match: '\n' + match.group(1) + '\n', content)

    return content

def _clean_markup(content):
    def replacement(match):
        groups = match.groups('')
        return ' ' + groups[0] + ' ' if groups else ''

    for pattern in _patterns['markup']:
        content = pattern.sub(replacement, content)
    return content

def _clean_whitespace(content):
    def replacement(match):
        return match.group(1)

    # strip whitespace line by line
    content = re.sub(r'^[ \t]*(.*?)[ \t]*$', replacement, content, flags=re.MULTILINE)

    # remove repeated whitespaces
    previous_content = content
    while True:
        content = re.sub(r'(\s)\1', replacement, content)
        if previous_content == content:
            break

        previous_content = content

    return content

def extract_text(content):
    text = _clean_macro(content)
    text = _clean_html(text)
    text = _clean_link(text)
    text = _clean_special_markup(text)
    text = _clean_markup(text)
    text = _clean_whitespace(text)
    text = text.strip()

    return text
