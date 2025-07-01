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

        self.repo.create(**kwargs)

    def read(self, obj_id: int) -> dict[str: any]:
        pass

    def read_all(self) -> list[dict[str, any]]:
        pass

    def update(self, obj) -> None:
        pass

    def delete(self, obj_id: int) -> None:
        pass