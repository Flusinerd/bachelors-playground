from my_vehicle_model.my_vehicle_model.RearTrunkService import RearTrunkService
from velocitas_sdk.model import Model


class Rear(Model):
    def __init__(self, parent):
        super().__init__(parent)
        self.service = RearTrunkService()
        self._isOpen = False

    @property
    def IsOpen(self):
        return self._isOpen

    @IsOpen.setter
    async def IsOpen(self, value):
        self._isOpen = value
        await self.service.SetIsOpen(value)

    @IsOpen.getter
    def IsOpen(self):
        return self._isOpen
