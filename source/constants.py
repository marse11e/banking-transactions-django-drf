TENGE = 'Kzt'

CURRENCY_CHOICES = (
    ('Kzt', 'Tenge'),
    ('Kgs', 'Som'),
    ('Usd', 'Dollar'),
    ('Eur', 'Euro'),
    ('Rub', 'Ruble'),
)
CREDIT_TRANSFER_TYPE = 'credit'
DEBIT_TRANSFER_TYPE = 'debit'
TRANSFER_TRANSFER_TYPE = 'transfer'

TRANSACTION_TYPES_CHOICES = (
    (CREDIT_TRANSFER_TYPE, 'Credit'),
    (DEBIT_TRANSFER_TYPE, 'Debit'),
    (TRANSFER_TRANSFER_TYPE, 'Transfer'),
)
