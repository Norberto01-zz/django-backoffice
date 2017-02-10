import os

from rest_framework.viewsets import ModelViewSet
from .serializers import PrepymeSerializer, UserSerializer, GroupSerializer, LoginSerializer, ImageSerializer
from rest_framework.views import APIView
from rest_framework.generics import RetrieveAPIView, UpdateAPIView
from rest_framework.permissions import AllowAny, IsAuthenticated
from django.contrib.auth import get_user_model
from django.contrib.auth.models import Group
from django.contrib.auth import login, logout
from rest_framework import filters
from cms.models import Prepyme, PrepyImage
from business.models import Country
from django.views.decorators.csrf import ensure_csrf_cookie
from django.views.generic import TemplateView
from django.utils.decorators import method_decorator
from django.http import Http404
from django.views.static import serve
from django.conf import settings

from rest_framework.response import Response
from rest_framework import status
from django.http import HttpResponse
from rest_framework.renderers import JSONRenderer

import requests
import json
from django.views.decorators.csrf import csrf_exempt
from rest_framework.decorators import api_view
import pprint


class JSONResponse(HttpResponse):
    def __init__(self, data, **kwargs):
        content = JSONRenderer().render(data)
        kwargs['content_type'] = 'application/json'
        super(JSONResponse, self).__init__(content, **kwargs)


# @csrf_exempt
# def pinless(request):
#     return JSONResponse('Hola')
#
# @csrf_exempt
# def topup(request):
#     return JSONResponse('Hola')


class UserViewSet(ModelViewSet):
    serializer_class = UserSerializer
    queryset = get_user_model().objects.all()
    filter_backends = (filters.DjangoFilterBackend,)
    filter_fields = ('first_name', 'last_name',)


class GroupViewSet(ModelViewSet):
    """
    API endpoint that allows groups to be viewed or edited.
    """
    queryset = Group.objects.all()
    serializer_class = GroupSerializer


class PrepymeViewSet(ModelViewSet):
    # cat = Category.objects.filter(text='')
    queryset = Prepyme.objects.all()
    serializer_class = PrepymeSerializer
    """
    def list(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset())

        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)
    """


class MyAccountApiView(RetrieveAPIView, UpdateAPIView):
    serializer_class = UserSerializer
    queryset = get_user_model().objects
    permission_classes = (IsAuthenticated,)

    def get_object(self):
        return self.get_queryset().get(pk=self.request.user.id)

    def put(self, request, *args, **kwargs):
        return self.update(request, *args, **kwargs)


class LoginView(APIView):
    permission_classes = (AllowAny,)

    def post(self, request, format=None):
        serializer = LoginSerializer(data=request.data)
        if serializer.is_valid():
            login(request, serializer.validated_data['user'])
            return Response({}, status=status.HTTP_200_OK)
        return Response(None, status=status.HTTP_401_UNAUTHORIZED)


class LogoutView(APIView):
    permission_classes = (IsAuthenticated,)

    def post(self, request, format=None):
        logout(request)
        return Response(None, status=status.HTTP_204_NO_CONTENT)


class PinlessProcessView(APIView):
    permission_classes = (AllowAny,)

    def post(self, request):
        payload = {'accountId': request.POST['accountId'], 'amount': request.POST['amount']}
        tran_url = 'http://192.168.1.244/prepymerest/public/index.php/api/pinless'
        pin_data = requests.post(tran_url, json=payload)

        if 200 != pin_data.json()['responseCode']:
            return Response({
                'responseCode': pin_data.json()['responseCode'],
                'responseDescription': pin_data.json()['responseDescription']
            }, status=pin_data.json()['responseCode'])

        gen_url = 'http://192.168.1.244/prepymerest/public/index.php/api/pinless/%s/generate' % pin_data.json()[
            'transactionId']
        gen_data = requests.put(gen_url)

        if 200 != gen_data.json()['responseCode']:
            return Response({
                'responseCode': gen_data.json()['responseCode'],
                'responseDescription': gen_data.json()['responseDescription']
            }, status=gen_data.json()['responseCode'])

        return Response({
            'responseDescription': 'Everything is ok',
            'transactionId': pin_data.json()['transactionId'],
            'B2CTransactionId': gen_data.json()['B2CTransactionId']
        }, status=status.HTTP_200_OK)


class ProceedToPayView(APIView):
    permission_classes = (AllowAny,)

    def post(self, request):
        url = 'http://192.168.1.244/prepymerest/public/index.php/api/pinless/'
        payload = {'accountId': request.POST['accountId'], 'amount': request.POST['amount']}

        pp = pprint.PrettyPrinter(depth=6)
        if request.POST['type'] == 'topup':
            country_id = Country.objects.filter(iso3=str(request.POST['countryId'])).values()
            pp.pprint(country_id[0]['id'])
            payload = {
                "accountId": int(request.POST['accountId']),
                "amount": float(request.POST['amount']),
                "operatorId": int(request.POST['operatorId']),
                "countryId": country_id[0]['id'],
                "phoneNumber": str(request.POST['phoneNumber'])
            }
            url = 'http://192.168.1.244/prepymerest/public/index.php/api/topup/'
        proceed_data = requests.post(url, json=payload)

        # load_data = json.loads();

        pp.pprint(request.POST)
        pp.pprint(proceed_data.json())

        if 200 != proceed_data.json()['responseCode']:
            return Response({
                'responseCode': proceed_data.json()['responseCode'],
                'responseDescription': proceed_data.json()['responseDescription']
            }, status=proceed_data.json()['responseCode'])

        gen_url = url + '%s/generate' % proceed_data.json()['transactionId']
        gen_data = requests.put(gen_url)

        pp.pprint("GEN DATA!!!")
        pp.pprint(gen_url)
        pp.pprint(gen_data.json())

        if 200 != gen_data.json()['responseCode']:
            return Response({
                'responseCode': gen_data.json()['responseCode'],
                'responseDescription': gen_data.json()['responseDescription']
            }, status=gen_data.json()['responseCode'])

        return Response({
            'responseCode': status.HTTP_200_OK,
            'responseDescription': 'Everything is ok',
            'transactionId': proceed_data.json()['transactionId'],
            'generateData': gen_data.json()
        }, status=status.HTTP_200_OK)


class ImageViewSet(ModelViewSet):
    queryset = PrepyImage.objects.all()
    serializer_class = ImageSerializer


class EmberView(TemplateView):
    @method_decorator(ensure_csrf_cookie)
    def get(self, request, *args, **kwargs):
        if request.is_ajax():
            raise Http404()
        return super(EmberView, self).get(request, *args, **kwargs)


EMBER_DIST_PATH = os.path.join(settings.BASE_DIR, '..', 'frontend', 'dist')


def service_worker_view(request, filetype, buildhash):
    return serve(request, '{}-{}.js'.format(filetype, buildhash), EMBER_DIST_PATH)


def root_files_view(request, filename):
    return serve(request, filename, EMBER_DIST_PATH)
