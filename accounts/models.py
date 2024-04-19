from django.contrib.auth.models import User
from django.db import models

from source.constants import CURRENCY_CHOICES, TENGE


class BaseModel(models.Model):
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Дата создания")
    modified_at = models.DateTimeField(auto_now=True, verbose_name="Дата изменения")

    class Meta:
        abstract = True


class BankAccount(BaseModel):
    user = models.OneToOneField(User, related_name='accounts', on_delete=models.CASCADE, verbose_name="Пользователь")
    account_number = models.CharField(unique=True, max_length=100, verbose_name="Номер счета", help_text="Уникальный номер счета")
    balance = models.DecimalField(default=0.0, max_digits=12, decimal_places=2, verbose_name="Баланс", help_text="Текущий баланс на счете")
    currency = models.CharField(choices=CURRENCY_CHOICES, blank=True, null=True, default=TENGE, max_length=30, verbose_name="Валюта", help_text="Тип валюты")
    first_name = models.CharField(max_length=130, blank=True, null=True, verbose_name="Имя", help_text="Имя владельца счета")
    last_name = models.CharField(max_length=130, blank=True, null=True, verbose_name="Фамилия", help_text="Фамилия владельца счета")

    class Meta:
        db_table = 'bank_accounts'
        verbose_name = "Банковский счет"
        verbose_name_plural = "Банковские счета"

    def __str__(self):
        return self.account_number

    def save(self, *args, **kwargs):
        if not self.account_number:
            from .utils import generate_unique_id
            self.account_number = generate_unique_id()
        super().save(*args, **kwargs)


class Transaction(BaseModel):
    reference_number = models.CharField(max_length=100, unique=True, verbose_name="Номер ссылки", help_text="Уникальный номер ссылки для транзакции")
    debit_account = models.CharField(null=True, blank=True, max_length=100, verbose_name="Дебетовый счет", help_text="Номер дебетового счета для транзакции")
    credit_account = models.CharField(null=True, blank=True, max_length=100, verbose_name="Кредитный счет", help_text="Номер кредитного счета для транзакции")
    amount = models.DecimalField(default=0.0, max_digits=12, decimal_places=2, verbose_name="Сумма", help_text="Сумма транзакции")
    is_successful = models.BooleanField(default=False, verbose_name="Успешная транзакция", help_text="Указывает, была ли транзакция успешной")

    class Meta:
        db_table = 'bank_transactions'
        verbose_name = "Транзакция"
        verbose_name_plural = "Транзакции"

    def __str__(self):
        return self.reference_number

    def save(self, *args, **kwargs):
        if not self.reference_number:
            from .utils import generate_unique_id
            self.reference_number = generate_unique_id()
        super().save(*args, **kwargs)
