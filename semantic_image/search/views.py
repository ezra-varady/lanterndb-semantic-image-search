from django.http import HttpResponse, Http404, JsonResponse
from django.template import loader
from django.db import connection
from .models import ImageTable

import mimetypes
import os


def index(request):
    template = loader.get_template('search_index.html')
    return HttpResponse(template.render({}, request))

def image(request, image_id):
    return HttpResponse(f'Image {image_id}')

def get_image(request, image_id):
    try:
        img = ImageTable.objects.get(id=image_id)
    except ImageTable.DoesNotExist:
        raise Http404('Image does not exist')
    
    with open(img.location, 'rb') as f:
        image_data = f.read()
    
    content_type, encoding = mimetypes.guess_type(img.location)
    
    return HttpResponse(image_data, content_type=content_type)

def get_topn(request):
    if request.method != 'POST':
        return Http404('This endpoint only accepts posts')
    query_string = request.POST.get('query_string')

    if query_string is None:
        return HttpResponseBadRequest("Missing 'query_string' parameter")

    with connection.cursor() as cursor:
        query = '''
        SELECT id FROM image_table
        ORDER BY v <-> clip_text(%s) ASC
        LIMIT 5
        '''
        cursor.execute(query, [query_string])
        rows = cursor.fetchall()

    ids = [row[0] for row in rows]
    return JsonResponse({'ids': ids})
