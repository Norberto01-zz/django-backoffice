from django.http.response import JsonResponse, HttpResponseNotFound
from rest_framework.viewsets import ModelViewSet
import simplejson as json
import urllib
import pprint
from .serializers import (RatesImportSerializer, RatesCountrySerializer)
from .models import Pages
from rest_framework.decorators import detail_route, list_route
from rest_framework.response import Response
from rest_framework import status

pp = pprint.PrettyPrinter(depth=6)


def find_number(param):
    search_url = 'http://67.222.240.237/service/GetOporatorByNumber.php?number=' + param
    raw = urllib.request.urlopen(search_url)
    js = raw.readlines()
    return json.loads(js[0])


# class PhoneValView
def phone_val(request, number, iso, prefix):
    msn = str(number)+' >> '+str(iso)+' >> '+str(prefix)+' <h1>Objeto no encontrado</h1>'
    js_object = find_number(str(number))
    if (iso != js_object['iso_country']) or (prefix != js_object['prefix']):
        js_object = find_number(str(prefix)+str(number))
        if (iso != js_object['iso_country']) or (prefix != js_object['prefix']):
            return HttpResponseNotFound(js_object['iso_country']+' '+js_object['prefix']+' '+msn)
    return JsonResponse(js_object, safe=False)


class GenericRateViewSet(ModelViewSet):
    pass


#category = Rate Import
class RateImportViewSet(GenericRateViewSet):
    queryset = Pages.objects.filter(cat=2, live=1)
    serializer_class = RatesImportSerializer


# Category = Country
class RateCountryViewSet(GenericRateViewSet):
    queryset = Pages.objects.filter(cat=4, live=1)
    serializer_class = RatesCountrySerializer

    @detail_route(methods=['get'], url_path='get-country-amounts')
    def get_country_amounts(self, request, pk=None):
        if not request.GET.get('channel'):
            return Response(None, status=status.HTTP_404_NOT_FOUND)

        instance = Pages.objects.filter(parent=pk).values('related_channel_page')
        operators = []
        pp.pprint(instance)
        for item in instance:
            pp.pprint(item)
        return Response({'id':'HOLA'})


