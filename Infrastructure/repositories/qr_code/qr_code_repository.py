import os
from datetime import datetime

from bank import account_number, bank_number, prefix

from Infrastructure.utilities.qr_paymnet_generator import spayd_payment_qr_code_generator

from Module.Interfaces import Repository
from Module import Purchase

QR_PAYMENT_DIR = "payment_qrs"

class QRCodeRepository(Repository):
    def create(self, purchase: Purchase) -> int | Exception:
        # loop settlements, from a person get a set of days and join in with an amount
        days_per_week = set()
        for settlement in purchase.purchase_settlements:
            days_per_week.add(
                tuple([settlement.person.detail.days_per_week,
                       settlement.amount]))

        # check if month dir exists, if not, create
        this_month = datetime.now().month
        month_dir = f"{self.db_path}/{QR_PAYMENT_DIR}/{this_month}"
        os.makedirs(month_dir, exist_ok=True)

        # inside month dir, create purchase(id) dir
        purchase_dir = f"{month_dir}/{purchase.id}"
        os.makedirs(purchase_dir, exist_ok=True)

        # loop the set, for every item create qr code
        # and save it to purchase dir with a number as name (days per week)
        for days_per_week, amount in days_per_week:
            self._operations.generate_qr_code(f"{purchase_dir}/{days_per_week}.gif",
                                              amount,
                                              account_number, bank_number, prefix)
        return purchase.id

    def read_by_id(self, purchase_id) -> str | None:
        """
        returns the path to the qr codes for the purchase with the given id
        if no purchase is found, returns None.
        """
        purchase: Purchase = self.aux_repo.read_by_id(purchase_id)
        if purchase:
            name = purchase.detail.name
            month = purchase.detail.date.month
            path = os.path.join(self.db_path, QR_PAYMENT_DIR, str(month), str(name))
            if os.path.exists(path):
                return path
            else:
                raise FileNotFoundError(f"No QR code found for purchase {purchase_id}")
        else:
            return None



    def read_by_other_id(self, other_id) -> object | Exception:
        raise NotImplementedError("Use read_by_id instead.")

    def read_all(self) -> list[object] | Exception:
        """
        Do you really wanna call me?
        'cause I am the destroyer of worlds
        """
        lst = []

        for month in os.listdir(os.path.join(self.db_path, QR_PAYMENT_DIR)):
            month_dir = os.path.join(self.db_path, QR_PAYMENT_DIR, month)
            for purchase in os.listdir(month_dir):
                purchase_dir = os.path.join(month_dir, purchase)
                for qr_code in os.listdir(purchase_dir):
                    lst.append(os.path.join(purchase_dir, qr_code))
        return lst

    def update(self, purchase_id) -> bool | Exception:
        try:
            self.delete_by_id(purchase_id)
            self.create(purchase_id)
            return True
        except IOError:
            return False

    def delete_by_id(self, purchase_id) -> bool | Exception:
        path = self.read_by_id(purchase_id)
        if path:
            os.remove(path)
            return True
        else:
            return False

    def _get_operations(self):
        return spayd_payment_qr_code_generator