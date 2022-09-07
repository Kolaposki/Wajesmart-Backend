from django.shortcuts import render
from django.views.generic.base import TemplateView
from rest_framework.views import APIView
from django.http import HttpResponse, JsonResponse, HttpResponseBadRequest
from django.conf import settings


class IndexTemplateView(TemplateView):
    print("IndexTemplateView IndexTemplateView IndexTemplateView")

    def get_template_names(self):
        if settings.DEBUG:
            template_name = "index-dev.html"
        else:
            template_name = "index.html"
        return template_name
