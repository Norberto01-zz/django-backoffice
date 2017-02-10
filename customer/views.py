from rest_framework.viewsets import ModelViewSet
from customer.serializers import ChannelSerializer, AddressLineSerializer
from customer.models import Channel, CreditCard, AddressLine
from prepyme.serializers import CreditCardSerializer, PrepymeSerializer
from rest_framework.decorators import detail_route
from rest_framework.response import Response
from rest_framework import status
from rest_framework.decorators import list_route
from cms.models import Prepyme
from rest_framework import permissions
import pprint


class GenericCustomerViewSet(ModelViewSet):
    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance)
        data = serializer.data
        ent_status = status.HTTP_200_OK
        if hasattr(instance, 'profile_id'):
            if request.user.pk != instance.profile_id.pk:
                data = None
                ent_status = status.HTTP_404_NOT_FOUND

        return Response(data, status=ent_status)

 
class ChannelViewSet(GenericCustomerViewSet):
    queryset = Channel.objects.all()
    serializer_class = ChannelSerializer
    permission_classes = (permissions.AllowAny,)

    @list_route(methods=['post', 'get'], url_path='get-countries')
    def list_get_countries(self, request):
        countries = []
        if not request.GET.get('channel'):
            return Response(None, status=status.HTTP_404_NOT_FOUND)

        country_channel = self.filter_queryset(Channel.objects.filter(pk=request.GET['channel']))

        serializer = self.get_serializer(country_channel, many=True)
        for post in serializer.data[0]['channel_page']:
            countries.append({'id': int(post['post']['parent']['id']), 'title': post['post']['parent']['title']})
        uniq = [i for n, i in enumerate(countries) if i not in countries[n + 1:]]

        return Response(uniq, status=status.HTTP_200_OK)


class CreditCardViewSet(GenericCustomerViewSet):
    queryset = CreditCard.objects.filter(status_cc=True)
    serializer_class = CreditCardSerializer

    @detail_route(methods=['post', 'get'], url_path='get-cc')
    def get_my_cc(self, request, pk=None):
        instance = self.get_object()
        serializer = self.get_serializer(instance)
        return Response(serializer.data)

    def list(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset())

        my_node_list = []
        for instance in queryset:
            if hasattr(instance, 'profile_id'):
                if request.user.pk == instance.profile_id.pk:
                    my_node_list.append(instance)

        page = self.paginate_queryset(my_node_list)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        serializer = self.get_serializer(my_node_list, many=True)
        return Response(serializer.data)


class AddressLineViewSet(GenericCustomerViewSet):
    queryset = AddressLine.objects.all()
    serializer_class = AddressLineSerializer

    def list(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset())

        my_node_list = []
        for instance in queryset:
            if hasattr(instance, 'profile_id'):
                if request.user.pk == instance.profile_id.pk:
                    my_node_list.append(instance)

        page = self.paginate_queryset(my_node_list)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        serializer = self.get_serializer(my_node_list, many=True)
        return Response(serializer.data)
    # @list_route(methods=['post', 'get'], url_path='list-address-cc')
    # def list(self, request, *args, **kwargs):
    #     queryset = self.filter_queryset(self.get_queryset())