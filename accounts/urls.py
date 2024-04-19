from django.urls import path, re_path

from .views import BankAccountViewSet, TransactionViewSet

urlpatterns = [
    path('accounts/', BankAccountViewSet.as_view({'get': 'list', 'post': 'create'}), name="accounts_list_and_create"),
    re_path(r'^accounts/(?P<account_number>\w+)/$', BankAccountViewSet.as_view({'get': 'retrieve'}), name="accounts_retrieve"),
    path('transactions/', TransactionViewSet.as_view({'get': 'list'}), name="transactions_list"),
    re_path(r'^transactions/(?P<reference_number>\w+)/$', TransactionViewSet.as_view({'get': 'retrieve'}), name="transactions_retrieve"),
    path('transfers/', TransactionViewSet.as_view({'post': 'create'}), name="transactions_create"),
]
