import time

from rest_framework import serializers

from .models import BankAccount, Transaction


def generate_unique_id(prefix=''):
    unique_id = str(time.time()).split('.')
    return prefix + ''.join(unique_id)


def get_api_response(data={}, message='Успешный', success=True):
    return {
        'data': data,
        'success': success,
        'message': message
    }


class AccountValidator(object):
    error_messages = 'Неверный номер счета.'
    model = BankAccount

    def __init__(self):
        pass

    def __call__(self, value):
        try:
            self.model.objects.only('account_number').get(account_number=value)
        except self.model.DoesNotExist:
            raise serializers.ValidationError(self.error_messages)


def update_transactions(amount, debit_account='', credit_account='', is_successful=False):
    transaction_object = Transaction(**locals())
    transaction_object.save()
    return transaction_object
