from django.http import HttpResponse, Http404
from django.template import loader
from django.db import connection
from django.conf import settings
from .models import ImageTable

import os

# Create your views here.
def index(request):
    template = loader.get_template('insert_index.html')
    return HttpResponse(template.render({}, request))

def upload(request):
    if request.method != 'POST':
        return Http404('This endpoint only accepts posts')
    image = request.FILES.get('file')
    
    if image:
        image_dir = os.path.join(settings.MEDIA_ROOT, 'images')
        if not os.path.exists(image_dir):
            os.makedirs(image_dir)
        save_path = os.path.join(image_dir, image.name)

        with open(save_path, 'wb+') as destination:
            for chunk in image.chunks():
                destination.write(chunk)

        with connection.cursor() as cursor:
            query = '''
            INSERT INTO image_table (v, location)
            VALUES (clip_image(%s), %s)
            '''
            cursor.execute(query, [save_path, save_path])

    else:
        return HttpResponseBadRequest("Missing image")

    return HttpResponse('Success')
