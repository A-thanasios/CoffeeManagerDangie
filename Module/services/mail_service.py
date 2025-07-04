from bank import prefix, account_number, bank_number

from Infrastructure.utilities.mail_sending.auth2_gmail_send.gmail_send import send_email
from Module.Interfaces import CRUDService
from Module.model.purchase import Purchase


class MailService:
    def __init__(self, purchase_service: CRUDService, payment_service: CRUDService) -> None:
        self.purchase_service = purchase_service
        self.payment_service = payment_service

    def send_payment_mail(self, purchase_id: int) -> bool:
        purchase: Purchase = self.purchase_service.get_object(purchase_id)
        for settlement in purchase.purchase_settlements:
            amount = settlement.amount
            name = settlement.person.detail.name
            days_per_week = settlement.person.detail.days_per_week
            address_to = settlement.person.detail.e_mail
            try:
                message = self.create_message(name, amount, purchase.products)
                image_path = self.get_image_path(purchase_id, days_per_week)
                send_email(address_to, message, image_path)
            except Exception as e:
                print(e)
                return False
        else:
            return True



    @staticmethod
    def create_message(name, amount, products):
        return f"""Hi {name},\n please, pay {amount: .2f} CZK for your coffee.\n Please send it here: \n{(prefix + '-' if prefix else '') + account_number + '/' + bank_number}\n or use QR Code down bellow. \n We are drinking: {'\n'.join(product.brand_name for product in products)}\n Thanks!"""

    def get_image_path(self, purchase_id: int, days_per_week: int):
        return self.payment_service.read(purchase_id) + '/qr_' + str(days_per_week) + '.gif'