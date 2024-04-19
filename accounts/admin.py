from django.contrib import admin
from .models import BankAccount, Transaction


@admin.register(BankAccount)
class BankAccountAdmin(admin.ModelAdmin):
    list_display = ('user', 'account_number', 'balance', 'currency', 'first_name', 'last_name')
    search_fields = ('user__username', 'account_number', 'first_name', 'last_name')
    list_filter = ('currency',)
    readonly_fields = ('created_at', 'modified_at')
    fieldsets = (
        (None, {
            'fields': ('user', 'account_number', 'balance', 'currency')
        }),
        ('Additional Info', {
            'fields': ('first_name', 'last_name')
        }),
        ('Important Dates', {
            'fields': ('created_at', 'modified_at'),
            'classes': ('collapse',),
        }),
    )


@admin.register(Transaction)
class TransactionAdmin(admin.ModelAdmin):
    list_display = ('reference_number', 'debit_account', 'credit_account', 'amount', 'is_successful')
    search_fields = ('reference_number', 'debit_account', 'credit_account')
    list_filter = ('is_successful',)
    readonly_fields = ('created_at', 'modified_at')
    fieldsets = (
        (None, {
            'fields': ('reference_number', 'debit_account', 'credit_account', 'amount', 'is_successful')
        }),
        ('Important Dates', {
            'fields': ('created_at', 'modified_at'),
            'classes': ('collapse',),
        }),
    )
