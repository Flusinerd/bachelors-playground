from my_vehicle_model.my_vehicle_model.Rear import Rear
from velocitas_sdk.model import Model


class Trunk(Model):
    def __init__(self, parent):
        super().__init__(parent)
        self.Rear = Rear(self)
