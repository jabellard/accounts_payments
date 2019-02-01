from django.http import HttpResponse
from django.conf import settings


def openapi(request):
    file_path = settings.BASE_DIR + '/apps/documentation/templates/openapi/openapi.html'
    html_string = 'No documentation.'
    try:
        with open(file_path, 'r') as html_file:
            html_string = html_file.read()
            return HttpResponse(html_string)
    except:
        return HttpResponse(html_string)
