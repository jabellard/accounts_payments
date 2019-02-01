from django.conf.urls import url
from django.urls import include
from django.urls import path
from .views import openapi
from rest_framework.documentation import include_docs_urls


urlpatterns = [
    url(r'^coreapi/', include_docs_urls(
        title='textbin API',
        description='textbin API.',
        public=False,
        authentication_classes=[],
        permission_classes=[],
    ),
        name='docs_coreapi'
    ),
    url(r'^openapi/$', openapi, name='docs_openapi'),
]
