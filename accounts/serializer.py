from rest_framework import serializers

from source.constants import (CREDIT_TRANSFER_TYPE, DEBIT_TRANSFER_TYPE,
                              TRANSACTION_TYPES_CHOICES, TRANSFER_TRANSFER_TYPE)
from .models import BankAccount, Transaction
from .utils import AccountValidator, update_transactions


class BankAccountSerializer(serializers.ModelSerializer):
    class Meta:
        model = BankAccount
        exclude = ('id', 'user')


class CreateAccountSerializer(serializers.ModelSerializer):
    class Meta:
        model = BankAccount
        fields = ('balance', 'first_name', 'last_name',)

    def create(self, validated_data):
        account_object = BankAccount(**validated_data)
        account_object.save()
        return account_object


class TransactionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Transaction
        exclude = ('id',)


class CreateTransactionSerializer(serializers.Serializer):
    debit_account_number = serializers.CharField(
        allow_blank=True,
        required=False,
        max_length=100,
        validators=[AccountValidator()]
    )
    credit_account_number = serializers.CharField(
        allow_blank=True,
        required=False,
        max_length=100,
        validators=[AccountValidator()]
    )
    amount = serializers.DecimalField(
        max_digits=12,
        decimal_places=2,
        required=True
    )
    transaction_type = serializers.ChoiceField(
        choices=TRANSACTION_TYPES_CHOICES
    )

    def validate(self, attrs):
        if not attrs.get('debit_account_number') and not attrs.get('credit_account_number'):
            raise serializers.ValidationError(
                'Укажите либо номер дебетового счета, либо номер кредитного счета')

        if attrs.get('transaction_type') == DEBIT_TRANSFER_TYPE and not attrs.get('debit_account_number'):
            raise serializers.ValidationError({
                "debit_account_number": ["Укажите номер дебетового счета для списания"]
            })

        elif attrs.get('transaction_type') == CREDIT_TRANSFER_TYPE and not attrs.get('credit_account_number'):
            raise serializers.ValidationError({
                "credit_account_number": ["Укажите номер кредитного счета для зачисления"]
            })

        elif attrs.get('transaction_type') == TRANSFER_TRANSFER_TYPE and (
            not attrs.get('debit_account_number') or not attrs.get(
                'credit_account_number')
        ):
            raise serializers.ValidationError(
                'Укажите оба номера дебетового и кредитного счетов для перевода')

        return attrs

    def create(self, validated_data):
        is_successful = False
        message = ''
        if validated_data.get('transaction_type') == DEBIT_TRANSFER_TYPE:
            account_object = BankAccount.objects.get(
                account_number=validated_data.get('debit_account_number')
            )
            
            if account_object.balance >= validated_data.get('amount', 0):
                account_object.balance = account_object.balance - validated_data.get('amount', 0)
                account_object.save()
                is_successful = True

            if not is_successful:
                message = 'Недостаточно средств на счете'

            return update_transactions(
                debit_account=validated_data.get('debit_account_number'),
                amount=validated_data.get('amount'), is_successful=is_successful), message
        
        elif validated_data.get('transaction_type') == CREDIT_TRANSFER_TYPE:
            account_object = BankAccount.objects.get(
                account_number=validated_data.get('credit_account_number')
            )
            account_object.balance = account_object.balance + validated_data.get('amount', 0)
            account_object.save()

            return update_transactions(
                credit_account=validated_data.get('credit_account_number'),
                amount=validated_data.get('amount'), is_successful=True), message
        else:
            debit_account_object = BankAccount.objects.get(account_number=validated_data.get('debit_account_number'))
            credit_account_object = BankAccount.objects.get(account_number=validated_data.get('credit_account_number'))
            
            if debit_account_object.balance >= validated_data.get('amount', 0):
                debit_account_object.balance -= validated_data.get('amount', 0)
                credit_account_object.balance += validated_data.get('amount', 0)
                debit_account_object.save()
                credit_account_object.save()
                is_successful = True
            
            if not is_successful:
                message = 'Недостаточно средств на счете'
            
            return update_transactions(
                debit_account=validated_data.get('debit_account_number'),
                credit_account=validated_data.get('credit_account_number'),
                amount=validated_data.get('amount'), is_successful=is_successful), message
