import os
import sys

import expressionive
from expressionive.expressionive import htmltags as T

def page_text(page_contents, style_text, script_text):
    """Return the text of an expressionive page."""
    return expressionive.Serializer(expressionive.examples_vmap, 'utf-8').serialize(
        expressionive.HTML5Doc([expressionive.safe_unicode(style_text
                                                           + script_text),
                                page_contents],
                               head=T.head[T.meta(charset='utf-8'),
                                           T.meta(rel='stylesheet',
                                                  type_='text/css',
                                                  href="dashboard.css"),
                                           T.title["Personal dashboard"]]))

def file_contents(filename):
    """Return the contents of a file."""
    if os.path.isfile(filename):
        with open(filename) as instream:
            return instream.read()
    return f"File {filename} not found"

def tagged(tag, text):
    """Surround a some text with opening and closing HTML tags."""
    return "<" + tag + ">" + text + "</" + tag + ">"

def tagged_file_contents(tag, filename):
    """Return the contents of a file, wrapped with begin and end tags.
    Can be used to include stylesheets and scripts in web pages."""
    return tagged(tag, file_contents(filename))
