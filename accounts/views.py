from rest_framework import status, viewsets
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework_jwt.authentication import JSONWebTokenAuthentication
from rest_framework.authentication import (
    BasicAuthentication, 
    SessionAuthentication, 
    TokenAuthentication
)

from .utils import get_api_response
from .models import BankAccount, Transaction
from .serializer import (
    BankAccountSerializer, 
    CreateAccountSerializer, 
    CreateTransactionSerializer,
    TransactionSerializer
)


class BankAccountViewSet(viewsets.ModelViewSet):
    model = BankAccount
    serializer_class = BankAccountSerializer
    authentication_classes = (
        JSONWebTokenAuthentication, 
        SessionAuthentication, 
        BasicAuthentication, 
        TokenAuthentication,
    )
    permission_classes = (IsAuthenticated,)

    def get_serializer_class(self):
        serializer_action_classes = {
            'list': BankAccountSerializer,
            'retrieve': BankAccountSerializer,
            'create': CreateAccountSerializer
        }
        if hasattr(self, 'action'):
            return serializer_action_classes.get(self.action, self.serializer_class)
        return self.serializer_class

    def get_queryset(self):
        return self.model.objects.order_by('-created_at')

    def list(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset())

        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            response = self.get_paginated_response(serializer.data)
            response_data = get_api_response(data=response.data)
            return Response(response_data, status=status.HTTP_200_OK)

        serializer = self.get_serializer(queryset, many=True)
        response_data = get_api_response(data=serializer.data)
        return Response(response_data)

    def retrieve(self, request, *args, **kwargs):
        account_number = kwargs.get('account_number')
        try:
            account_object = self.model.objects.get(account_number=account_number)
        except self.model.DoesNotExist:
            response_data = get_api_response(message='Account does not exist', success=False)
            return Response(response_data, status=status.HTTP_404_NOT_FOUND)
        serializer = self.get_serializer(account_object)
        response_data = get_api_response(data=serializer.data)
        return Response(response_data, status=status.HTTP_200_OK)

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        account_object = serializer.save(user=request.user)
        response_data = get_api_response(data={'account_number': account_object.account_number})
        return Response(response_data, status=status.HTTP_201_CREATED)


class TransactionViewSet(viewsets.ModelViewSet):
    model = Transaction
    serializer_class = TransactionSerializer
    authentication_classes = (
        JSONWebTokenAuthentication, 
        SessionAuthentication, 
        BasicAuthentication, 
        TokenAuthentication
    )
    permission_classes = (IsAuthenticated,)

    def get_serializer_class(self):
        serializer_action_classes = {
            'list': TransactionSerializer,
            'retrieve': TransactionSerializer,
            'create': CreateTransactionSerializer,
        }
        if hasattr(self, 'action'):
            return serializer_action_classes.get(self.action, self.serializer_class)
        return self.serializer_class

    def get_queryset(self):
        return self.model.objects.order_by('-created_at')

    def list(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset())

        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            response = self.get_paginated_response(serializer.data)
            response_data = get_api_response(data=response.data)
            return Response(response_data, status=status.HTTP_200_OK)

        serializer = self.get_serializer(queryset, many=True)
        response_data = get_api_response(data=serializer.data)
        return Response(response_data)

    def retrieve(self, request, *args, **kwargs):
        reference_number = kwargs.get('reference_number')
        try:
            transaction_object = self.model.objects.get(reference_number=reference_number)
        except self.model.DoesNotExist:
            response_data = get_api_response(message='Transaction does not exist', success=False)
            return Response(response_data, status=status.HTTP_404_NOT_FOUND)
        serializer = self.get_serializer(transaction_object)
        response_data = get_api_response(data=serializer.data)
        return Response(response_data, status=status.HTTP_200_OK)

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        transaction_object, message = serializer.save(user=request.user)
        data = transaction_object.__dict__
        data.pop('_state', None)
        data.pop('id', None)
        response_data = get_api_response(data=data, message=message if message else 'Successful')
        return Response(response_data, status=status.HTTP_200_OK)
