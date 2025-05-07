from module.interfaces.Provider import Provider


class PurchaseProvider(Provider):
    def __init__(self, purchase_service) -> None:
        self.purchase_service = purchase_service
    def get(self, item_id: str | list[str]) -> object:
        if item_id == []:
            return None

    def create(self) -> str:
        pass

    def update(self, item_id: str | list[str]) -> None:
        pass

    def delete(self, item_id: str | list[str]) -> None:
        pass