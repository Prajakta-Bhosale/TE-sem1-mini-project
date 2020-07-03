"""
from io import BytesIO
from django.http import HttpResponse
from django.template.loader import get_template,render_to_string
from django.template import RequestContext
from django.config import settings
import cStringIO as StringIO
import cgi
import os

from xhtml2pdf import pisa

def render_to_pdf(template_src, context_dict={}):
    
    template = get_template(template_src)
    html = template.render(context_dict)
    result = StringIO.StringIO()
    if no image:
        pdf = pisa.pisaDocument(StringIO.StringIO(html.encode("ISO-8859-1")), result)
    else:
        pdf = pisa.pisaDocument(StringIO.StringIO(html.encode("ISO-8859-1")), dest=result,link_callback=fetch_resources)
      
    if not pdf.err:
        return HttpResponse(result.getvalue(), mimetype='Event/pdf')
    return None

def fetch_resource(uri,rel):
    if os.sep == '\\':
        uri2 = os.sep.join(uri.split('/'))
    else:
        uri2 = uri
    path = '%s%s' % (settings.SITE_ROOT,uri2)
    return path

"""
from io import BytesIO
from django.http import HttpResponse
from django.template.loader import get_template

from xhtml2pdf import pisa

def render_to_pdf(template_src, context_dict={}):
    
    template = get_template(template_src)
    html = template.render(context_dict)
    result = BytesIO()
    pdf = pisa.pisaDocument(BytesIO(html.encode("ISO-8859-1")), result)
    if not pdf.err:
        return HttpResponse(result.getvalue(), content_type='Event/pdf')
    return None
