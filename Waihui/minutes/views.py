from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse
import qrcode
from cStringIO import StringIO
from minutes.models import *


def index(request):
    return HttpResponse("This is Javy Chen Minutes!")


def generate_qrcode(request, data):
    img = qrcode.make(data)
    buf = StringIO()
    img.save(buf)
    image_stream = buf.getvalue()
    response = HttpResponse(image_stream, content_type="image/png")
    response['Last-Modified'] = 'Sun, 10 Jul 2016 12:05:03 GMT'
    response['Cache-Control'] = 'max-age=31536000'
    return response


def entry_detail(request, entry_id):
    entry = get_object_or_404(Entry, id=entry_id)
    return render(request, "entry_detail.html", locals())

def attend(request, entry_id):
    entry = get_object_or_404(Entry, id=entry_id)
    return render(request, "entry_detail.html", locals())