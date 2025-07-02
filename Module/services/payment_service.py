from Module.Interfaces import CRUDService, Repository


class PaymentService(CRUDService):
    def __init__(self, repository: Repository):
        self.repo = repository

    def create(self, **kwargs) -> int | object:
        """
        kwargs: amount: str, account_number: str, bank_code: str
        """

        required_args = ['amount', 'account_number', 'bank_code']
        for arg in required_args:
            if arg not in kwargs:
                raise ValueError(f"Missing required argument: {arg}")
            if not isinstance(arg, str):
                try:
                   kwargs[arg] =  str(arg)
                except:
                    raise TypeError(f"Invalid argument type: {arg}")

        return self.repo.create(**kwargs)

    def read(self, purchase_id: int) -> dict[str: any]:
        """
        returns a dictionary with the given purchase id as a key and the qr_codes path as value, both str
        """
        if not isinstance(purchase_id, int):
            raise TypeError("Invalid argument type: purchase_id")
        return {str(purchase_id): self.repo.read_by_id(purchase_id)}

    def read_all(self) -> list[dict[str, any]]:
        raise NotImplementedError("Use read(purchase_id) instead.")

    def update(self, purchase_id) -> None:
        #TODO: Refactoring would be needed
        self.repo.update(purchase_id)

    def delete(self, purchase_id: int) -> None:
        #TODO: Refactoring would be needed
        self.repo.delete_by_id(purchase_id)