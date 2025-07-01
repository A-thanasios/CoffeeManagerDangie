import segno

IBAN_PREFIX_LENGTH: int = 6
PAYMENT_COUNTRY: str = 'CZ'
COUNTRY_CONTROL_NUMBER: str = '123500'

"""
Generate QR code for SPAYD payment. Only Czech bank accounts are supported.
"""


def generate_qr_payment(target: str,
                        amount: str,
                        account_number: str, bank_number: str, prefix: str | None = None) -> None:
    iban = generate_iban(prefix, account_number, bank_number)
    print(iban)
    spayd_code = f"SPD*1.0*ACC:{iban}*AM:{amount}*CC:CZK"
    qr = segno.make_qr(spayd_code)
    qr.to_artistic(background='15-23-06-837_512.gif',
                   target=target,
                   scale=15,
                   dark=(75, 54, 33))


def generate_iban(prefix: str, account_number: str, bank_number: str) -> str:
    iban_prefix = generate_iban_prefix(prefix)
    control_number = 98 - (int(bank_number + iban_prefix + account_number + COUNTRY_CONTROL_NUMBER) % 97)

    return f"{PAYMENT_COUNTRY}{control_number}{bank_number}{iban_prefix}{account_number}"

def generate_iban_prefix(prefix: str | None = None) -> str:
    if not prefix:
        return '0' * IBAN_PREFIX_LENGTH
    return prefix.zfill(IBAN_PREFIX_LENGTH)
